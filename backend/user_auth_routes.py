from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from models import User, UserCreate, UserRegister, UserLogin
from user_auth import (
    create_user_access_token, create_or_update_user,
    get_current_active_user, get_user_by_email,
    authenticate_user, create_user
)
from datetime import timedelta, datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Create router for user auth routes
user_auth_router = APIRouter(prefix="/user-auth", tags=["user-authentication"])
security = HTTPBearer()

@user_auth_router.post("/register")
async def register_user(user_data: UserRegister):
    """Register a new user with email and password"""
    try:
        # Create new user
        user = await create_user(user_data.email, user_data.password, user_data.name)
        
        # Create access token
        access_token_expires = timedelta(days=7)
        access_token = create_user_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 7 * 24 * 60 * 60,  # seconds
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "profile_picture": user.profile_picture,
                "email_verified": user.email_verified
            },
            "message": "Registration successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

@user_auth_router.post("/login")
async def login_user(user_data: UserLogin):
    """Login user with email and password"""
    try:
        # Authenticate user
        user = await authenticate_user(user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is inactive"
            )
        
        # Update last login
        from database import get_database
        db = await get_database()
        await db.users.update_one(
            {"email": user.email},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create access token
        access_token_expires = timedelta(days=7)
        access_token = create_user_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 7 * 24 * 60 * 60,  # seconds
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "profile_picture": user.profile_picture,
                "email_verified": user.email_verified
            },
            "message": "Login successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@user_auth_router.post("/google-login")
async def google_login(user_data: dict):
    """Handle Google OAuth login/registration"""
    try:
        # Validate required fields from Google OAuth
        required_fields = ["email", "name", "google_id"]
        for field in required_fields:
            if field not in user_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
        
        # Create or update user
        user = await create_or_update_user(user_data)
        
        # Create access token
        access_token_expires = timedelta(days=7)  # 7 days for users
        access_token = create_user_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 7 * 24 * 60 * 60,  # seconds
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "profile_picture": user.profile_picture
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during Google login: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@user_auth_router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "profile_picture": current_user.profile_picture,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }

@user_auth_router.post("/refresh")
async def refresh_user_token(current_user: User = Depends(get_current_active_user)):
    """Refresh user access token"""
    try:
        access_token_expires = timedelta(days=7)  # 7 days
        access_token = create_user_access_token(
            data={"sub": current_user.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 7 * 24 * 60 * 60  # seconds
        }
    except Exception as e:
        logger.error(f"Error refreshing user token: {str(e)}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@user_auth_router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_active_user)):
    """Logout user (client should delete token)"""
    return {"message": "Logged out successfully"}