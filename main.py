from fastapi import FastAPI
from database import Base, engine
import models
from routers import item
from routers import registration
from routers import refresh
from routers import login
from routers import user


Base.metadata.create_all(bind=engine)
app = FastAPI(title="FastAPI CRUD Example")
app.include_router(item.router)
app.include_router(user.router)
app.include_router(registration.router)
app.include_router(login.router)
app.include_router(refresh.router)

@app.get("/")
def root():
    return {"message": "FastAPI CRUD running"}
