from fastapi import FastAPI
from database import Base, engine
import models
import item

Base.metadata.create_all(bind=engine)
app = FastAPI(title="FastAPI CRUD Example")
app.include_router(item.router)

@app.get("/")
def root():
    return {"message": "FastAPI CRUD running"}
