from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import User
from database import get_database
import os
from dotenv import load_dotenv

load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days for users

security = HTTPBearer()

def create_user_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token for users"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "user"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email"""
    db = await get_database()
    user_data = await db.users.find_one({"email": email})
    if user_data:
        return User(**user_data)
    return None

async def get_user_by_google_id(google_id: str) -> Optional[User]:
    """Get user by Google ID"""
    db = await get_database()
    user_data = await db.users.find_one({"google_id": google_id})
    if user_data:
        return User(**user_data)
    return None

async def create_or_update_user(user_data: dict) -> User:
    """Create or update user from Google OAuth"""
    db = await get_database()
    
    # Try to find existing user by email or google_id
    existing_user = await db.users.find_one({
        "$or": [
            {"email": user_data["email"]},
            {"google_id": user_data["google_id"]}
        ]
    })
    
    if existing_user:
        # Update existing user
        update_data = {
            "name": user_data["name"],
            "profile_picture": user_data.get("profile_picture"),
            "last_login": datetime.utcnow()
        }
        if not existing_user.get("google_id") and user_data.get("google_id"):
            update_data["google_id"] = user_data["google_id"]
            
        await db.users.update_one(
            {"_id": existing_user["_id"]},
            {"$set": update_data}
        )
        
        # Return updated user
        updated_user_data = await db.users.find_one({"_id": existing_user["_id"]})
        return User(**updated_user_data)
    else:
        # Create new user
        user = User(**user_data)
        user_dict = user.dict()
        result = await db.users.insert_one(user_dict)
        return user

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token is for user
        if payload.get("type") != "user":
            raise credentials_exception
            
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Optional authentication - returns None if not authenticated
async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token is for user
        if payload.get("type") != "user":
            return None
            
        email: str = payload.get("sub")
        if email is None:
            return None
            
        user = await get_user_by_email(email=email)
        if user and user.is_active:
            return user
    except JWTError:
        pass
    
    return None