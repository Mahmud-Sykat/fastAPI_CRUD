from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
import schemas

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# CREATE USER
# -------------------------
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Check for duplicate email
    existing_user = db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": user.email}
    ).mappings().first()  # Use mappings().first() for dict-like row

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert new user (only once!)
    db.execute(
        text("INSERT INTO users (name, email, password) VALUES (:name, :email, :password)"),
        user.dict()
    )
    db.commit()

    # Get the inserted user
    user_row = db.execute(
        text("SELECT id, name, email FROM users WHERE email = :email"),
        {"email": user.email}
    ).mappings().first()

    return dict(user_row)


# -------------------------
# GET ALL USERS
# -------------------------
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT id, name, email FROM users")
    ).mappings().all()
    return [dict(r) for r in rows]


# -------------------------
# GET SINGLE USER
# -------------------------
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_row = db.execute(
        text("SELECT id, name, email FROM users WHERE id = :id"),
        {"id": user_id}
    ).mappings().first()

    if not user_row:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user_row)


# -------------------------
# UPDATE USER
# -------------------------
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):

    exists = db.execute(
        text("SELECT id FROM users WHERE id = :id"),
        {"id": user_id}
    ).mappings().first()

    if not exists:
        raise HTTPException(status_code=404, detail="User not found")

    db.execute(
        text("""
            UPDATE users
            SET name = :name,
                email = :email,
                password = :password
            WHERE id = :id
        """),
        {"id": user_id, **user.dict()}
    )
    db.commit()

    updated_user = db.execute(
        text("SELECT id, name, email FROM users WHERE id = :id"),
        {"id": user_id}
    ).mappings().first()

    return dict(updated_user)


# -------------------------
# DELETE USER
# -------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    exists = db.execute(
        text("SELECT id FROM users WHERE id = :id"),
        {"id": user_id}
    ).mappings().first()

    if not exists:
        raise HTTPException(status_code=404, detail="User not found")

    db.execute(
        text("DELETE FROM users WHERE id = :id"),
        {"id": user_id}
    )
    db.commit()

    return {"message": "User deleted successfully"}
