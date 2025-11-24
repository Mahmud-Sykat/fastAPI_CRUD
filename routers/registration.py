from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import text
import schemas, auth_utils

router = APIRouter(prefix="/register", tags=["registration"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check existing email
    existing_user = db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": user.email}
    ).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth_utils.hash_password(user.password)

    db.execute(
        text("INSERT INTO users (name, email, password) VALUES (:name, :email, :password)"),
        {"name": user.name, "email": user.email, "password": hashed_password}
    )
    db.commit()

    new_user = db.execute(
        text("SELECT id, name, email FROM users WHERE email = :email"),
        {"email": user.email}
    ).mappings().first()

    return dict(new_user)
