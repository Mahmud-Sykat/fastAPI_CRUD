from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
import schemas

router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# CREATE
# -------------------------
@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):

    db.execute(
        text("INSERT INTO items (title, description) VALUES (:title, :description)"),
        {"title": item.title, "description": item.description}
    )
    db.commit()

    # Get last inserted item
    row = db.execute(
        text(
            "SELECT id, title, description FROM items WHERE title = :title ORDER BY id DESC LIMIT 1"
        ),
        {"title": item.title}
    ).mappings().first()  # <-- Use mappings().first()

    return dict(row)


# -------------------------
# GET ALL ITEMS
# -------------------------
@router.get("/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):

    rows = db.execute(text("SELECT id, title, description FROM items")).mappings().all()  # <-- Use mappings().all()
    return [dict(r) for r in rows]


# -------------------------
# GET SINGLE ITEM
# -------------------------
@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):

    row = db.execute(
        text("SELECT id, title, description FROM items WHERE id = :id"),
        {"id": item_id}
    ).mappings().first()  # <-- Use mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    return dict(row)


# -------------------------
# UPDATE
# -------------------------
@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, update: schemas.ItemCreate, db: Session = Depends(get_db)):

    # Check if exists
    check = db.execute(
        text("SELECT id FROM items WHERE id = :id"),
        {"id": item_id}
    ).mappings().first()  # <-- Use mappings().first()

    if not check:
        raise HTTPException(status_code=404, detail="Item not found")

    db.execute(
        text("UPDATE items SET title = :title, description = :description WHERE id = :id"),
        {"id": item_id, "title": update.title, "description": update.description}
    )
    db.commit()

    # Get updated item
    row = db.execute(
        text("SELECT id, title, description FROM items WHERE id = :id"),
        {"id": item_id}
    ).mappings().first()  # <-- Use mappings().first()

    return dict(row)


# -------------------------
# DELETE
# -------------------------
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):

    # Check if exists
    check = db.execute(
        text("SELECT id FROM items WHERE id = :id"),
        {"id": item_id}
    ).mappings().first()  # <-- Use mappings().first()

    if not check:
        raise HTTPException(status_code=404, detail="Item not found")

    db.execute(
        text("DELETE FROM items WHERE id = :id"),
        {"id": item_id}
    )
    db.commit()

    return {"message": "Item deleted successfully"}
