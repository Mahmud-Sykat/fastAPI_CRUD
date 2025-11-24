from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import text
import schemas, auth_utils

router = APIRouter(prefix="/login", tags=["login"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Token)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": user.email}
    ).mappings().first()

    if not db_user or not auth_utils.verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth_utils.create_access_token({"sub": db_user["email"]})
    refresh_token = auth_utils.create_refresh_token({"sub": db_user["email"]})

    return {"access_token": access_token, "refresh_token": refresh_token}
