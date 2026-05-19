from fastapi import FastAPI
import os

app = FastAPI(title="PulseNotify API", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": os.getenv("APP_ENV", "development")}

@app.get("/")
def read_root():
    return {"message": "Welcome to PulseNotify - Your Devops Journey Starts Here"}