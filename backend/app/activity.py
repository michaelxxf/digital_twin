from sqlalchemy.orm import Session
from . import models
from datetime import datetime, UTC
from typing import List, Optional

def log_activity(db: Session, user_id: int, action: str, details: Optional[str] = None):
    """
    Log user activity to the database
    """
    activity_log = models.ActivityLog(
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.now(UTC)
    )
    db.add(activity_log)
    db.commit()
    db.refresh(activity_log)
    return activity_log

def get_user_activities(db: Session, user_id: int, limit: int = 100) -> List[models.ActivityLog]:
    """
    Get activity logs for a specific user
    """
    return db.query(models.ActivityLog).filter(
        models.ActivityLog.user_id == user_id
    ).order_by(models.ActivityLog.timestamp.desc()).limit(limit).all()

def get_all_activities(db: Session, limit: int = 100) -> List[models.ActivityLog]:
    """
    Get all activity logs (for admin monitoring)
    """
    return db.query(models.ActivityLog).order_by(
        models.ActivityLog.timestamp.desc()
    ).limit(limit).all()

def get_activities_by_time_range(db: Session, start_time: datetime, end_time: datetime) -> List[models.ActivityLog]:
    """
    Get activities within a specific time range
    """
    return db.query(models.ActivityLog).filter(
        models.ActivityLog.timestamp >= start_time,
        models.ActivityLog.timestamp <= end_time
    ).order_by(models.ActivityLog.timestamp.desc()).all()

def get_activities_by_action(db: Session, action: str, limit: int = 100) -> List[models.ActivityLog]:
    """
    Get activities filtered by action type
    """
    return db.query(models.ActivityLog).filter(
        models.ActivityLog.action == action
    ).order_by(models.ActivityLog.timestamp.desc()).limit(limit).all()

def get_suspicious_activities(db: Session, limit: int = 50) -> List[models.ActivityLog]:
    """
    Get potentially suspicious activities
    """
    suspicious_actions = [
        "failed_login",
        "file_access_denied",
        "unauthorized_access_attempt",
        "multiple_failed_logins",
        "suspicious_file_access",
        "admin_action_attempted"
    ]
    
    return db.query(models.ActivityLog).filter(
        models.ActivityLog.action.in_(suspicious_actions)
    ).order_by(models.ActivityLog.timestamp.desc()).limit(limit).all()
