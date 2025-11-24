from pydantic import BaseModel

# ---- Item schemas ----
class ItemCreate(BaseModel):
    title: str
    description: str

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True 

# ---- User schemas ----
class UserCreate(BaseModel):
    name: str
    email: str
    password: str  # plaintext for now

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int