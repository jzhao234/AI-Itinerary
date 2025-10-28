from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user
from app.api import users

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)

@app.get("/")
def read_root(): 
    return {"message": "Backend is running!"}
