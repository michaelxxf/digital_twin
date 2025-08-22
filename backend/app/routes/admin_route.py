from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from .. import models, database, auth, admin, activity
from ..schemas import UserOut, ActivityLog
from typing import List, Optional
from datetime import datetime, timedelta, UTC
from app.database import get_db
import re
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

class StaffCreate(BaseModel):
    username: str
    email: str
    password: str
    department: str

def extract_domain(email: str) -> str:
    """Extract domain from email address."""
    return email.split('@')[-1].lower()

def get_current_admin(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/dashboard/stats")
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get admin dashboard statistics"""
    return admin.get_system_statistics(db)

@router.get("/users", response_model=List[UserOut])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get all users in the admin's organisation (by email domain) with pagination"""
    admin_domain = extract_domain(current_admin.email)
    all_users = admin.get_all_users(db, skip=skip, limit=limit)
    filtered_users = [user for user in all_users if extract_domain(user.email) == admin_domain]
    return filtered_users

@router.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get specific user by ID (only if in admin's organisation)"""
    user = admin.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    admin_domain = extract_domain(current_admin.email)
    if extract_domain(user.email) != admin_domain:
        raise HTTPException(status_code=403, detail="Access denied")
    return user

@router.put("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Activate or deactivate a user in admin organisation"""
    user = admin.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    admin_domain = extract_domain(current_admin.email)
    if extract_domain(user.email) != admin_domain:
        raise HTTPException(status_code=403, detail="Access denied")
    return admin.update_user_status(db, user_id, is_active)

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Delete a user (soft delete)"""
    return admin.delete_user(db, user_id)

@router.get("/security/alerts")
def get_security_alerts(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get security alerts and suspicious activities"""
    return admin.get_security_alerts(db, limit)

@router.get("/users/{user_id}/activity")
def get_user_activity_summary(
    user_id: int,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get activity summary for a specific user (only if in admin's organisation)"""
    user = admin.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    admin_domain = extract_domain(current_admin.email)
    if extract_domain(user.email) != admin_domain:
        raise HTTPException(status_code=403, detail="Access denied")
    return admin.get_user_activity_summary(db, user_id, days)

@router.post("/staff/create")
def create_staff_user(
    staff: StaffCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Create a new staff user (must match admin's email domain)"""
    admin_domain = extract_domain(current_admin.email)
    user_domain = extract_domain(staff.email)
    if user_domain != admin_domain:
        raise HTTPException(status_code=400, detail="Email domain must match admin's organisation domain")
    return admin.create_staff_user(db, staff.username, staff.email, staff.password, staff.department)

@router.get("/analytics/activities")
def get_activity_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get activity analytics for admin dashboard"""
    return admin.get_activity_analytics(db, days)

@router.get("/activities", response_model=List[ActivityLog])
def get_all_activities(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get all activity logs"""
    return activity.get_all_activities(db, limit)

@router.get("/activities/suspicious")
def get_suspicious_activities(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get suspicious activities"""
    return activity.get_suspicious_activities(db, limit)

@router.get("/activities/time-range")
def get_activities_by_time_range(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get activities within a time range"""
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        return activity.get_activities_by_time_range(db, start, end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@router.get("/system/status")
def get_system_status(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """Get system status and health"""
    stats = admin.get_system_statistics(db)
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "statistics": stats,
        "active_connections": 0,  # This would be implemented with WebSocket tracking
        "system_uptime": "24 hours"  # This would be calculated from actual uptime
    } 