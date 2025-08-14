from .database import engine, Base
from . import models
from .models import User, Staff, Admin, ActivityLog
from .auth import get_password_hash
from sqlalchemy.orm import sessionmaker

def init():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")
    
    # Create sample data
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if not existing_admin:
            # Create admin user
            admin_user = User(
                username="admin",
                email="admin@digitaltwin.com",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            # Create admin record
            admin_record = Admin(
                user_id=admin_user.id,
                privileges="full_access"
            )
            db.add(admin_record)
            
            # Create sample staff user
            staff_user = User(
                username="staff1",
                email="staff1@digitaltwin.com",
                hashed_password=get_password_hash("staff123"),
                role="staff",
                is_active=True
            )
            db.add(staff_user)
            db.commit()
            db.refresh(staff_user)
            
            # Create staff record
            staff_record = Staff(
                user_id=staff_user.id,
                department="IT"
            )
            db.add(staff_record)
            
            # Create sample regular user
            regular_user = User(
                username="user1",
                email="user1@digitaltwin.com",
                hashed_password=get_password_hash("user123"),
                role="user",
                is_active=True
            )
            db.add(regular_user)
            
            db.commit()
            print("Sample users created successfully!")
        else:
            print("Admin user already exists, skipping sample data creation.")
            
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init()