from pydantic import BaseModel
class ItemBase(BaseModel):
    title: str
    description: str
    
class ItemCreate(ItemBase):
    pass
class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True