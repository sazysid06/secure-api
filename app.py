import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import Base, init_db
from routes.users import router as users_router
from routes.posts import router as posts_router
from routes.admin import router as admin_router
from routes.auth import router as auth_router

settings = get_settings()

# Initialize database
init_db(settings.DATABASE_URL)

from database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="SecureAPI",
    description="Production-level authentication system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(admin_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "SecureAPI is running"}