from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import sessionLocal
import models, schemas

router = APIRouter(prefix="/items", tags=["items"])
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@router.get("/{item_id}" , response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}" , response_model=schemas.ItemResponse)
def update_item(item_id: int, update: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id). first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = update.title
    item.description = update.description
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item-id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail= "Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}