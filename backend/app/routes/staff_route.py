from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, database, auth, staff, activity
from ..schemas import UserOut, ActivityLog
from typing import List, Optional
from datetime import datetime, timedelta, UTC
from app.database import get_db
router = APIRouter(prefix="/staff", tags=["staff"])

def get_current_staff(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "staff":
        raise HTTPException(status_code=403, detail="Staff access required")
    return current_user

@router.get("/profile")
def get_staff_profile(
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get current staff member's profile"""
    staff_record = staff.get_staff_by_user_id(db, current_staff.id)
    if not staff_record:
        raise HTTPException(status_code=404, detail="Staff record not found")
    
    return {
        "user": current_staff,
        "staff_info": staff_record
    }

@router.put("/profile/department")
def update_department(
    new_department: str,
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Update staff department"""
    return staff.update_staff_department(db, current_staff.id, new_department)

@router.get("/department/stats")
def get_department_statistics(
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get statistics for staff's department"""
    staff_record = staff.get_staff_by_user_id(db, current_staff.id)
    if not staff_record:
        raise HTTPException(status_code=404, detail="Staff record not found")
    
    dept_stats = staff.get_department_statistics(db)
    return {
        "department": staff_record.department,
        "statistics": dept_stats.get(staff_record.department, {})
    }

@router.get("/activity/summary")
def get_staff_activity_summary(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get activity summary for current staff member"""
    return staff.get_staff_activity_summary(db, current_staff.id, days)

@router.get("/department/activities")
def get_department_activities(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get activities from staff in the same department"""
    staff_record = staff.get_staff_by_user_id(db, current_staff.id)
    if not staff_record:
        raise HTTPException(status_code=404, detail="Staff record not found")
    
    return staff.get_department_activities(db, staff_record.department, days)

@router.get("/performance/metrics")
def get_performance_metrics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get performance metrics for current staff member"""
    return staff.get_staff_performance_metrics(db, current_staff.id, days)

@router.get("/colleagues")
def get_department_colleagues(
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get all staff members in the same department"""
    staff_record = staff.get_staff_by_user_id(db, current_staff.id)
    if not staff_record:
        raise HTTPException(status_code=404, detail="Staff record not found")
    
    colleagues = staff.get_staff_by_department(db, staff_record.department)
    return {
        "department": staff_record.department,
        "colleagues": colleagues
    }

@router.get("/activities", response_model=List[ActivityLog])
def get_staff_activities(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get current staff member's activities"""
    return activity.get_user_activities(db, current_staff.id, limit)

@router.get("/activities/recent")
def get_recent_activities(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db),
    current_staff: models.User = Depends(get_current_staff)
):
    """Get recent activities for current staff member"""
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(hours=hours)
    
    activities = activity.get_activities_by_time_range(db, start_date, end_date)
    staff_activities = [a for a in activities if a.user_id == current_staff.id]
    
    return {
        "staff_id": current_staff.id,
        "period_hours": hours,
        "activities": staff_activities
    } 