from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

# Import database functions
from database import connect_to_mongo, close_mongo_connection

# Import routes
from admin_routes import admin_router
from ai_routes import ai_router, public_ai_router
from auth_routes import auth_router
from user_auth_routes import user_auth_router
from resume_routes import resume_router
from portfolio_routes import portfolio_router
from public_routes import public_router

# Import auth functions
from auth import create_default_admin

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(
    title="TalentD Clone API",
    description="Complete admin and user API for TalentD clone with AI capabilities",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Basic health check
@api_router.get("/")
async def root():
    return {"message": "TalentD Clone API is running", "status": "healthy"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# Include all route modules
api_router.include_router(auth_router)  # /api/auth/*
api_router.include_router(user_auth_router)  # /api/user-auth/*
api_router.include_router(admin_router)  # /api/admin/*
api_router.include_router(ai_router)     # /api/ai/*
api_router.include_router(public_ai_router)  # /api/public-ai/*
api_router.include_router(resume_router)  # /api/resume/*
api_router.include_router(portfolio_router)  # /api/portfolio/*
api_router.include_router(public_router)  # /api/public/*

# Include the main router in the app
app.include_router(api_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Configure as needed for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection and create default admin"""
    try:
        await connect_to_mongo()
        await create_default_admin()
        logger.info("Application started successfully")
        logger.info("Default admin credentials: username=admin, password=admin123")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection"""
    try:
        await close_mongo_connection()
        logger.info("Application shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)