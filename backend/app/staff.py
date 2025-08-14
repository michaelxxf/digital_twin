from sqlalchemy.orm import Session
from . import models, activity
from typing import List, Dict, Optional
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException

def get_staff_by_user_id(db: Session, user_id: int) -> Optional[models.Staff]:
    """
    Get staff record by user ID
    """
    return db.query(models.Staff).filter(models.Staff.user_id == user_id).first()

def get_all_staff(db: Session, skip: int = 0, limit: int = 100) -> List[models.Staff]:
    """
    Get all staff members with their user information
    """
    return db.query(models.Staff).join(models.User).offset(skip).limit(limit).all()

def get_staff_by_department(db: Session, department: str) -> List[models.Staff]:
    """
    Get all staff members in a specific department
    """
    return db.query(models.Staff).filter(models.Staff.department == department).all()

def update_staff_department(db: Session, user_id: int, new_department: str) -> models.Staff:
    """
    Update staff department
    """
    staff = get_staff_by_user_id(db, user_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    old_department = staff.department
    staff.department = new_department
    db.commit()
    db.refresh(staff)
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user_id,
        action="department_changed",
        details=f"Department changed from {old_department} to {new_department}"
    )
    
    return staff

def get_department_statistics(db: Session) -> Dict:
    """
    Get statistics by department
    """
    departments = db.query(models.Staff.department).distinct().all()
    department_stats = {}
    
    for dept in departments:
        dept_name = dept[0]
        staff_count = db.query(models.Staff).filter(models.Staff.department == dept_name).count()
        active_staff = db.query(models.Staff).join(models.User).filter(
            models.Staff.department == dept_name,
            models.User.is_active == True
        ).count()
        
        department_stats[dept_name] = {
            "total_staff": staff_count,
            "active_staff": active_staff
        }
    
    return department_stats

def get_staff_activity_summary(db: Session, user_id: int, days: int = 7) -> Dict:
    """
    Get activity summary for a staff member
    """
    staff = get_staff_by_user_id(db, user_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Get activities for the last N days
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    staff_activities = [a for a in activities if a.user_id == user_id]
    
    # Count activities by type
    activity_counts = {}
    for act in staff_activities:
        activity_counts[act.action] = activity_counts.get(act.action, 0) + 1
    
    return {
        "staff": {
            "id": staff.id,
            "user_id": staff.user_id,
            "department": staff.department
        },
        "total_activities": len(staff_activities),
        "activity_breakdown": activity_counts,
        "recent_activities": staff_activities[:10]
    }

def get_department_activities(db: Session, department: str, days: int = 7) -> List[models.ActivityLog]:
    """
    Get all activities from staff in a specific department
    """
    # Get all staff in the department
    staff_members = get_staff_by_department(db, department)
    staff_user_ids = [staff.user_id for staff in staff_members]
    
    if not staff_user_ids:
        return []
    
    # Get activities for the last N days
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    department_activities = [a for a in activities if a.user_id in staff_user_ids]
    
    return department_activities

def create_staff_member(db: Session, username: str, email: str, password: str, department: str) -> models.Staff:
    """
    Create a new staff member
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
    db.refresh(staff_record)
    
    # Log the activity
    activity.log_activity(
        db=db,
        user_id=user.id,
        action="staff_member_created",
        details=f"Staff member created in department: {department}"
    )
    
    return staff_record

def get_staff_performance_metrics(db: Session, user_id: int, days: int = 30) -> Dict:
    """
    Get performance metrics for a staff member
    """
    staff = get_staff_by_user_id(db, user_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Get activities for the last N days
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    staff_activities = [a for a in activities if a.user_id == user_id]
    
    # Calculate metrics
    total_activities = len(staff_activities)
    successful_activities = len([a for a in staff_activities if "success" in a.action.lower() or "completed" in a.action.lower()])
    failed_activities = len([a for a in staff_activities if "failed" in a.action.lower() or "error" in a.action.lower()])
    
    success_rate = (successful_activities / total_activities * 100) if total_activities > 0 else 0
    
    # Group by day
    daily_activities = {}
    for act in staff_activities:
        date_str = act.timestamp.date().isoformat()
        if date_str not in daily_activities:
            daily_activities[date_str] = 0
        daily_activities[date_str] += 1
    
    return {
        "staff_id": staff.id,
        "department": staff.department,
        "total_activities": total_activities,
        "successful_activities": successful_activities,
        "failed_activities": failed_activities,
        "success_rate": round(success_rate, 2),
        "daily_activities": daily_activities,
        "period_days": days
    }
