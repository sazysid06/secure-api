import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, engine
from models import User, UserRole, Base
from config import get_settings
from auth import hash_password
from sqlalchemy.orm import sessionmaker

settings = get_settings()

# Initialize database
init_db(settings.DATABASE_URL)

# Import engine again after init_db
from database import engine, SessionLocal

# Create tables
Base.metadata.create_all(bind=engine)

# Create admin user
db = SessionLocal()

# Check if admin exists
admin = db.query(User).filter(User.email == "admin@example.com").first()
if not admin:
    admin_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin_user)
    db.commit()
    print("✅ Admin user created: admin@example.com / admin123")
else:
    print("✅ Admin user already exists")

db.close()