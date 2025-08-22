from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
from datetime import datetime, UTC
from . import activity
from sqlalchemy.orm import Session
from .database import SessionLocal

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "admin": [],
            "staff": []
        }

    async def connect(self, websocket: WebSocket, client_type: str):
        await websocket.accept()
        if client_type not in self.active_connections:
            self.active_connections[client_type] = []
        self.active_connections[client_type].append(websocket)

    def disconnect(self, websocket: WebSocket, client_type: str):
        if client_type in self.active_connections:
            if websocket in self.active_connections[client_type]:
                self.active_connections[client_type].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_type(self, message: str, client_type: str):
        if client_type in self.active_connections:
            for connection in self.active_connections[client_type]:
                try:
                    await connection.send_text(message)
                except:
                    # Remove dead connections
                    self.active_connections[client_type].remove(connection)

    async def broadcast_to_all(self, message: str):
        for client_type in self.active_connections:
            await self.broadcast_to_type(message, client_type)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, client_type: str = "users"):
    await manager.connect(websocket, client_type)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "activity_log":
                # Log activity to database
                db = SessionLocal()
                try:
                    activity.log_activity(
                        db=db,
                        user_id=message.get("user_id"),
                        action=message.get("action"),
                        details=message.get("details")
                    )
                    
                    # Broadcast to admins if it's a suspicious activity
                    if message.get("action") in [
                        "failed_login", "unauthorized_access", "suspicious_activity"
                    ]:
                        alert_message = {
                            "type": "security_alert",
                            "timestamp": datetime.now(UTC).isoformat(),
                            "user_id": message.get("user_id"),
                            "action": message.get("action"),
                            "details": message.get("details")
                        }
                        await manager.broadcast_to_type(
                            json.dumps(alert_message), "admin"
                        )
                        
                finally:
                    db.close()
                    
            elif message.get("type") == "system_status":
                # Broadcast system status updates
                await manager.broadcast_to_type(
                    json.dumps(message), "admin"
                )
                
            elif message.get("type") == "notification":
                # Send notifications to specific user types
                target_type = message.get("target", "all")
                if target_type == "all":
                    await manager.broadcast_to_all(json.dumps(message))
                else:
                    await manager.broadcast_to_type(json.dumps(message), target_type)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_type)

async def send_activity_update(activity_data: dict):
    """
    Send activity updates to all connected clients
    """
    message = {
        "type": "activity_update",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": activity_data
    }
    await manager.broadcast_to_all(json.dumps(message))

async def send_security_alert(alert_data: dict):
    """
    Send security alerts to admin clients
    """
    message = {
        "type": "security_alert",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": alert_data
    }
    await manager.broadcast_to_type(json.dumps(message), "admin")

async def send_system_notification(notification: str, target_type: str = "all"):
    """
    Send system notifications
    """
    message = {
        "type": "system_notification",
        "timestamp": datetime.now(UTC).isoformat(),
        "message": notification
    }
    if target_type == "all":
        await manager.broadcast_to_all(json.dumps(message))
    else:
        await manager.broadcast_to_type(json.dumps(message), target_type)
