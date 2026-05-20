from fastapi import FastAPI
import os

# New Database Imports
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

app = FastAPI(title="PulseNotify API", version="0.1.0")

# --- Database Setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

class ItemCreate(BaseModel):
    name: str

# --- API Routes ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": os.getenv("APP_ENV", "development")}

@app.get("/")
def read_root():
    return {"message": "Welcome to PulseNotify – Your DevOps Journey Starts Here"}

@app.post("/items")
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.get("/items")
def list_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items