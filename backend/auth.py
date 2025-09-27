from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import AdminUser
from database import get_database
import os
from dotenv import load_dotenv

load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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

async def get_admin_by_username(username: str) -> Optional[AdminUser]:
    """Get admin user by username"""
    db = await get_database()
    admin_data = await db.admin_users.find_one({"username": username})
    if admin_data:
        return AdminUser(**admin_data)
    return None

async def authenticate_admin(username: str, password: str) -> Optional[AdminUser]:
    """Authenticate admin user"""
    admin = await get_admin_by_username(username)
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
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    admin = await get_admin_by_username(username=username)
    if admin is None:
        raise credentials_exception
    
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    
    return admin

async def get_current_active_admin(current_admin: AdminUser = Depends(get_current_admin)) -> AdminUser:
    """Get current active admin user"""
    if not current_admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_admin

async def create_default_admin():
    """Create default admin user if none exists"""
    db = await get_database()
    admin_count = await db.admin_users.count_documents({})
    
    if admin_count == 0:
        default_admin = {
            "username": "admin",
            "email": "admin@talentd.local",
            "hashed_password": get_password_hash("admin123"),
            "is_active": True,
            "is_superuser": True,
            "created_at": datetime.utcnow()
        }
        
        await db.admin_users.insert_one(default_admin)
        print("Default admin created - username: admin, password: admin123")