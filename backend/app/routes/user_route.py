from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from ..routes.admin_route import extract_domain
from .. import models, database, auth, schemas
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db

router = APIRouter()

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.UserOut)
def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    if user.role not in ["admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    # --- Prevent duplicate admin organisation domains ---
    if user.role == "admin":
        new_admin_domain = extract_domain(user.email)
        # Find any admin with the same domain
        existing_admins = db.query(models.User).filter(
            (models.User.role == "admin")
        ).all()
        for admin_user in existing_admins:
            if extract_domain(admin_user.email) == new_admin_domain:
                raise HTTPException(
                    status_code=400,
                    detail="An admin for this organisation domain already exists. contact yur admin to add you as a staff"
                )
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.role == "admin":
        admin_exists = db.query(models.Admin).filter(models.Admin.user_id == new_user.id).first()
        if not admin_exists:
            new_admin = models.Admin(user_id=new_user.id, privileges="full_access")
            db.add(new_admin)
            db.commit()

    return new_user