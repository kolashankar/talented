from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from models import AdminLogin, AdminCreate, AdminUser
from auth import (
    authenticate_admin, create_access_token, get_password_hash,
    get_current_active_admin
)
from database import get_database
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# Create router for auth routes
auth_router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@auth_router.post("/login")
async def login(admin_login: AdminLogin):
    """Authenticate admin and return access token"""
    try:
        admin = await authenticate_admin(admin_login.username, admin_login.password)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=1440)  # 24 hours
        access_token = create_access_token(
            data={"sub": admin.email}, expires_delta=access_token_expires
        )
        
        # Update last login
        from datetime import datetime
        db = await get_database()
        await db.admin_users.update_one(
            {"email": admin.email},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1440 * 60,  # seconds
            "user": {
                "username": admin.username,
                "email": admin.email,
                "is_superuser": admin.is_superuser
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@auth_router.post("/register")
async def register_admin(admin_data: AdminCreate, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Register a new admin user (requires existing admin)"""
    try:
        # Only superusers can create new admins
        if not current_admin.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only superusers can create new admin accounts"
            )
        
        db = await get_database()
        
        # Check if username already exists
        existing_admin = await db.admin_users.find_one({"username": admin_data.username})
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = await db.admin_users.find_one({"email": admin_data.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new admin user
        admin_user = AdminUser(
            username=admin_data.username,
            email=admin_data.email,
            hashed_password=get_password_hash(admin_data.password),
            is_superuser=admin_data.is_superuser
        )
        
        admin_dict = admin_user.dict()
        result = await db.admin_users.insert_one(admin_dict)
        
        if result.inserted_id:
            return {
                "message": "Admin user created successfully",
                "username": admin_user.username,
                "email": admin_user.email
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create admin user")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

@auth_router.get("/me")
async def get_current_user_info(current_admin: AdminUser = Depends(get_current_active_admin)):
    """Get current authenticated admin user information"""
    return {
        "username": current_admin.username,
        "email": current_admin.email,
        "is_superuser": current_admin.is_superuser,
        "is_active": current_admin.is_active,
        "created_at": current_admin.created_at,
        "last_login": current_admin.last_login
    }

@auth_router.post("/refresh")
async def refresh_token(current_admin: AdminUser = Depends(get_current_active_admin)):
    """Refresh access token"""
    try:
        access_token_expires = timedelta(minutes=1440)  # 24 hours
        access_token = create_access_token(
            data={"sub": current_admin.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1440 * 60  # seconds
        }
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@auth_router.get("/health")
async def auth_health():
    """Simple health check for auth endpoints"""
    return {"status": "healthy", "service": "auth"}