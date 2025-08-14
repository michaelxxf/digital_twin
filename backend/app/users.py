from sqlalchemy.orm import Session
from . import models, activity
from typing import List, Dict, Optional
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException
from .auth import get_password_hash, verify_password

def get_user_profile(db: Session, user_id: int) -> Optional[models.User]:
    """
    Get user profile by ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user_profile(db: Session, user_id: int, email: str = None, username: str = None) -> models.User:
    """
    Update user profile information
    """
    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if email:
        # Check if email is already taken by another user
        existing_user = db.query(models.User).filter(
            models.User.email == email,
            models.User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = email
    
    if username:
        # Check if username is already taken by another user
        existing_user = db.query(models.User).filter(
            models.User.username == username,
            models.User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already in use")
        user.username = username
    
    db.commit()
    db.refresh(user)
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user_id,
        action="profile_updated",
        details="User profile information updated"
    )
    
    return user

def change_user_password(db: Session, user_id: int, current_password: str, new_password: str) -> bool:
    """
    Change user password
    """
    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user_id,
        action="password_changed",
        details="User password changed"
    )
    
    return True

def get_user_activities(db: Session, user_id: int, limit: int = 50) -> List[models.ActivityLog]:
    """
    Get user's activity history
    """
    return activity.get_user_activities(db, user_id, limit)

def get_user_statistics(db: Session, user_id: int, days: int = 30) -> Dict:
    """
    Get user statistics and activity summary
    """
    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get activities for the last N days
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    user_activities = [a for a in activities if a.user_id == user_id]
    
    # Calculate statistics
    total_activities = len(user_activities)
    login_activities = len([a for a in user_activities if "login" in a.action.lower()])
    file_activities = len([a for a in user_activities if "file" in a.action.lower()])
    system_activities = len([a for a in user_activities if "system" in a.action.lower()])
    
    # Group by day
    daily_activities = {}
    for act in user_activities:
        date_str = act.timestamp.date().isoformat()
        if date_str not in daily_activities:
            daily_activities[date_str] = 0
        daily_activities[date_str] += 1
    
    # Get most active day
    most_active_day = max(daily_activities.items(), key=lambda x: x[1]) if daily_activities else None
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        },
        "statistics": {
            "total_activities": total_activities,
            "login_activities": login_activities,
            "file_activities": file_activities,
            "system_activities": system_activities,
            "most_active_day": most_active_day,
            "period_days": days
        },
        "daily_activities": daily_activities
    }

def deactivate_user_account(db: Session, user_id: int) -> bool:
    """
    Deactivate user account (soft delete)
    """
    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user_id,
        action="account_deactivated",
        details="User account deactivated"
    )
    
    return True

def reactivate_user_account(db: Session, user_id: int) -> bool:
    """
    Reactivate user account
    """
    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user_id,
        action="account_reactivated",
        details="User account reactivated"
    )
    
    return True

def get_user_session_info(db: Session, user_id: int) -> Dict:
    """
    Get user session information and recent activity
    """
    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recent activities (last 24 hours)
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(hours=24)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    recent_activities = [a for a in activities if a.user_id == user_id]
    
    # Get last login
    login_activities = [a for a in recent_activities if "login" in a.action.lower()]
    last_login = login_activities[-1].timestamp if login_activities else None
    
    return {
        "user_id": user.id,
        "username": user.username,
        "is_active": user.is_active,
        "last_login": last_login,
        "recent_activities_count": len(recent_activities),
        "session_duration": "24 hours"  # This could be calculated based on actual session data
    }

def search_users(db: Session, query: str, limit: int = 20) -> List[models.User]:
    """
    Search users by username or email
    """
    return db.query(models.User).filter(
        (models.User.username.contains(query)) | (models.User.email.contains(query))
    ).limit(limit).all()

def get_users_by_role(db: Session, role: str, limit: int = 100) -> List[models.User]:
    """
    Get all users by role
    """
    return db.query(models.User).filter(models.User.role == role).limit(limit).all()

def get_active_users_count(db: Session) -> int:
    """
    Get count of active users
    """
    return db.query(models.User).filter(models.User.is_active == True).count()

def get_users_created_in_period(db: Session, days: int = 30) -> List[models.User]:
    """
    Get users created in the last N days
    """
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    return db.query(models.User).filter(
        models.User.created_at >= start_date,
        models.User.created_at <= end_date
    ).all()
