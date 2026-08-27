from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from auth import decode_token
from models import User, UserRole
from typing import Optional

router = APIRouter(prefix="/admin", tags=["admin"])

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Get current user from token"""
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header"
        )
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

def require_admin(current_user: User = Depends(get_current_user)):
    """
    RBAC - Only admin users can access
    Check user role before allowing access (from lecture)
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/users")
def list_all_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """
    Admin only route - list all users
    """
    users = db.query(User).all()
    return {
        "admin": current_user.username,
        "total_users": len(users),
        "users": [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]
    }

@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """
    Admin only route - delete a user
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user.username} deleted"}

@router.patch("/users/{user_id}/role")
def change_user_role(user_id: int, role: str, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """
    Admin only route - change user role
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if role not in ["admin", "user", "mentor"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    user.role = role
    db.commit()
    
    return {"message": f"User role changed to {role}"}