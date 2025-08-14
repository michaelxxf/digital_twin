from sqlalchemy.orm import Session
from . import models, activity
from typing import List, Dict, Optional
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    Get all users with pagination
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """
    Get user by ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user_status(db: Session, user_id: int, is_active: bool) -> models.User:
    """
    Activate or deactivate a user
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user_id,
        action="user_status_changed",
        details=f"User {'activated' if is_active else 'deactivated'}"
    )
    
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user (soft delete by setting is_active to False)
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user_id,
        action="user_deleted",
        details="User account deleted"
    )
    
    return True

def get_system_statistics(db: Session) -> Dict:
    """
    Get system statistics for admin dashboard
    """
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.is_active == True).count()
    admin_users = db.query(models.User).filter(models.User.role == "admin").count()
    staff_users = db.query(models.User).filter(models.User.role == "staff").count()
    
    # Get recent activities
    recent_activities = activity.get_all_activities(db, limit=10)
    
    # Get suspicious activities
    suspicious_activities = activity.get_suspicious_activities(db, limit=5)
    
    # Get today's activities
    today = datetime.now(UTC).date()
    today_start = datetime.combine(today, datetime.min.time(), tzinfo=UTC)
    today_end = datetime.combine(today, datetime.max.time(), tzinfo=UTC)
    today_activities = activity.get_activities_by_time_range(db, today_start, today_end)
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "staff_users": staff_users,
        "recent_activities": len(recent_activities),
        "suspicious_activities": len(suspicious_activities),
        "today_activities": len(today_activities)
    }

def get_security_alerts(db: Session, limit: int = 20) -> List[models.ActivityLog]:
    """
    Get security alerts and suspicious activities
    """
    return activity.get_suspicious_activities(db, limit)

def get_user_activity_summary(db: Session, user_id: int, days: int = 7) -> Dict:
    """
    Get activity summary for a specific user
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get activities for the last N days
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    user_activities = [a for a in activities if a.user_id == user_id]
    
    # Count activities by type
    activity_counts = {}
    for act in user_activities:
        activity_counts[act.action] = activity_counts.get(act.action, 0) + 1
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        },
        "total_activities": len(user_activities),
        "activity_breakdown": activity_counts,
        "recent_activities": user_activities[:10]
    }

def create_staff_user(db: Session, username: str, email: str, password: str, department: str) -> models.User:
    """
    Create a new staff user
    """
    from .auth import get_password_hash
    
    # Check if user already exists
    existing_user = db.query(models.User).filter(
        (models.User.username == username) | (models.User.email == email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Create user
    user = models.User(
        username=username,
        email=email,
        hashed_password=get_password_hash(password),
        role="staff",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create staff record
    staff_record = models.Staff(
        user_id=user.id,
        department=department
    )
    db.add(staff_record)
    db.commit()
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user.id,
        action="staff_user_created",
        details=f"Staff user created in department: {department}"
    )
    
    return user

def get_activity_analytics(db: Session, days: int = 30) -> Dict:
    """
    Get activity analytics for the admin dashboard
    """
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    
    # Group activities by date
    daily_activities = {}
    for act in activities:
        date_str = act.timestamp.date().isoformat()
        if date_str not in daily_activities:
            daily_activities[date_str] = 0
        daily_activities[date_str] += 1
    
    # Group activities by type
    activity_types = {}
    for act in activities:
        if act.action not in activity_types:
            activity_types[act.action] = 0
        activity_types[act.action] += 1
    
    return {
        "total_activities": len(activities),
        "daily_activities": daily_activities,
        "activity_types": activity_types,
        "period_days": days
    }
