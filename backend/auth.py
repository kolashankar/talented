from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import AdminUser
from database import get_database
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Use a simpler password context for now
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_admin_by_username_or_email(username_or_email: str) -> Optional[AdminUser]:
    """Get admin user by username or email"""
    try:
        db = await get_database()
        if db is None:
            logger.error("Database connection not available")
            return None

        admin_data = await db.admin_users.find_one({
            "$or": [
                {"username": username_or_email},
                {"email": username_or_email}
            ]
        })
        if admin_data:
            return AdminUser(**admin_data)
        return None
    except Exception as e:
        logger.error(f"Error getting admin by username/email: {str(e)}")
        return None

async def authenticate_admin(username_or_email: str, password: str) -> Optional[AdminUser]:
    """Authenticate admin user by username or email"""
    admin = await get_admin_by_username_or_email(username_or_email)
    if not admin:
        return None
    if not verify_password(password, admin.hashed_password):
        return None
    return admin

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AdminUser:
    """Get current authenticated admin user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if not credentials or not credentials.credentials:
            raise credentials_exception

        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception

    try:
        admin = await get_admin_by_username_or_email(username_or_email=email)
        if admin is None:
            raise credentials_exception

        if not admin.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )

        return admin
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current admin: {str(e)}")
        raise credentials_exception

async def get_current_active_admin(current_admin: AdminUser = Depends(get_current_admin)) -> AdminUser:
    """Get current active admin user"""
    if not current_admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_admin

async def create_default_admin():
    """Create default admin user with specified credentials"""
    try:
        db = await get_database()

        # Admin credentials from environment
        admin_email = os.getenv("ADMIN_EMAIL", "kolashankar113@gmail.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "Shankar@113")

        # Check if admin already exists
        existing_admin = await db.admin_users.find_one({"email": admin_email})

        if not existing_admin:
            # Create the specified admin user
            admin_user = AdminUser(
                username="admin",
                email=admin_email,
                hashed_password=get_password_hash(admin_password),
                is_active=True,
                is_superuser=True
            )

            admin_dict = admin_user.dict()
            await db.admin_users.insert_one(admin_dict)
            print(f"Admin created - email: {admin_email}")
        else:
            # Update password if admin exists but password might have changed
            hashed_password = get_password_hash(admin_password)
            await db.admin_users.update_one(
                {"email": admin_email},
                {"$set": {"hashed_password": hashed_password, "is_active": True}}
            )
            print(f"Admin password updated - email: {admin_email}")

    except Exception as e:
        print(f"Error creating/updating admin: {str(e)}")
        # Don't raise the error, just log it
        pass
