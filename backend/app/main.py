from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from . import database, init_db
from .routes import user_route, admin_route, staff_route, activity_route
from .websocket import websocket_endpoint, manager
import json

app = FastAPI(title="Digital Twin System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include all routers
app.include_router(user_route.router)
app.include_router(admin_route.router)
app.include_router(staff_route.router)
app.include_router(activity_route.router)

# WebSocket endpoints
@app.websocket("/ws/{client_type}")
async def websocket_route(websocket: WebSocket, client_type: str):
    await websocket_endpoint(websocket, client_type)

@app.get("/")
def read_root():
    return {
        "message": "Digital Twin System Backend Running",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "auth": "/token",
            "users": "/register",
            "admin": "/admin",
            "staff": "/staff",
            "activity": "/activity",
            "websocket": "/ws/{client_type}"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db.init()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

