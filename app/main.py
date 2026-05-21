# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from app.database import engine, SessionLocal, Base
from app.models import Item

# Create all tables (will be replaced by Alembic later)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PulseNotify API", version="0.1.0")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": os.getenv("APP_ENV", "development")}

@app.get("/")
def read_root():
    return {"message": "Welcome to PulseNotify – Your DevOps Journey Starts Here"}

class ItemCreate(BaseModel):
    name: str

@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()