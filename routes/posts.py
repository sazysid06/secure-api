from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from auth import decode_token
from models import User
from typing import Optional

router = APIRouter(prefix="/posts", tags=["posts"])

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """
    Dependency to extract and verify JWT token from Authorization header
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required in Authorization header"
        )
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Use: Bearer <token>"
        )
    
    # Decode JWT (from lecture - signature verification)
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.get("/my-posts")
def get_my_posts(current_user: User = Depends(get_current_user)):
    """
    Protected route - requires valid JWT token
    Only authenticated users can access
    """
    return {
        "message": f"Hello {current_user.username}",
        "user_id": current_user.id,
        "posts": []
    }

@router.post("/create-post")
def create_post(title: str, content: str, current_user: User = Depends(get_current_user)):
    """
    Protected route - create a post
    Only authenticated users can create posts
    """
    return {
        "message": "Post created",
        "user_id": current_user.id,
        "title": title,
        "content": content
    }