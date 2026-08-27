from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserSignup, UserLogin, TokenResponse
from models import User
from database import get_db
from auth import hash_password, verify_password, create_access_token, create_refresh_token
from cache import set_cache

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", response_model=dict)
def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    User signup endpoint
    - Check if email exists
    - Hash password
    - Store in database
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password (from lecture)
    hashed_pwd = hash_password(user_data.password)
    
    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    
    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "message": "User created successfully"
    }

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint
    - Verify email exists
    - Verify password (from lecture)
    - Generate JWT tokens
    - Cache token in Redis
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password (lecture concept)
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    # Cache token in Redis (skip for now)
    # set_cache(f"user:{user.id}:access_token", {"token": access_token}, expire_seconds=1800)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800
    )