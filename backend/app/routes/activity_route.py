from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, database, auth, activity
from ..schemas import ActivityLog
from typing import List, Optional
from datetime import datetime, timedelta, UTC
from pydantic import BaseModel
from app.database import get_db

router = APIRouter(prefix="/activity", tags=["activity"])

class ActivityLogRequest(BaseModel):
    user_id: int
    action: str
    details: Optional[str] = None

@router.post("/log")
def log_activity(
    activity_data: ActivityLogRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Log a new activity"""
    # Verify the user is logging their own activity or is admin
    if current_user.role != "admin" and current_user.id != activity_data.user_id:
        raise HTTPException(status_code=403, detail="Can only log your own activities")
    
    return activity.log_activity(
        db=db,
        user_id=activity_data.user_id,
        action=activity_data.action,
        details=activity_data.details
    )

@router.get("/user/{user_id}", response_model=List[ActivityLog])
def get_user_activities(
    user_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get activities for a specific user"""
    # Verify the user is requesting their own activities or is admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Can only view your own activities")
    
    return activity.get_user_activities(db, user_id, limit)

@router.get("/all", response_model=List[ActivityLog])
def get_all_activities(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get all activities (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return activity.get_all_activities(db, limit)

@router.get("/suspicious")
def get_suspicious_activities(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get suspicious activities (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return activity.get_suspicious_activities(db, limit)

@router.get("/time-range")
def get_activities_by_time_range(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get activities within a time range"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        return activity.get_activities_by_time_range(db, start, end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@router.get("/by-action")
def get_activities_by_action(
    action: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get activities filtered by action type"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return activity.get_activities_by_action(db, action, limit)

@router.get("/recent")
def get_recent_activities(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get recent activities"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(hours=hours)
    
    return activity.get_activities_by_time_range(db, start_date, end_date)

@router.get("/summary")
def get_activity_summary(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get activity summary statistics"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    
    # Group by action type
    action_counts = {}
    for act in activities:
        action_counts[act.action] = action_counts.get(act.action, 0) + 1
    
    # Group by day
    daily_counts = {}
    for act in activities:
        date_str = act.timestamp.date().isoformat()
        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
    
    return {
        "total_activities": len(activities),
        "period_days": days,
        "action_breakdown": action_counts,
        "daily_breakdown": daily_counts
    } 