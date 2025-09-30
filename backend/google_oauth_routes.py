from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from typing import Dict, Any
from google_oauth_service import google_oauth
from models import User
import logging

logger = logging.getLogger(__name__)

# Create router for Google OAuth routes
oauth_router = APIRouter(prefix="/auth/google", tags=["google-oauth"])

@oauth_router.get("/login")
async def google_login():
    """Redirect to Google OAuth authorization page"""
    try:
        authorization_url = google_oauth.get_authorization_url()
        return {"authorization_url": authorization_url}
        
    except Exception as e:
        logger.error(f"Error initiating Google login: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to initiate Google login")

@oauth_router.get("/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        # Get authorization code from query parameters
        authorization_code = request.query_params.get('code')
        if not authorization_code:
            raise HTTPException(status_code=400, detail="Authorization code not found")
        
        # Exchange code for tokens and user info
        token_data = await google_oauth.exchange_code_for_tokens(authorization_code)
        user_info = token_data['user_info']
        
        # Create or get user
        user = await google_oauth.create_or_get_user(user_info)
        
        # Generate JWT token
        jwt_token = google_oauth.generate_jwt_token(user)
        
        # In a real application, you might redirect to frontend with token
        # For now, return the token and user info
        return {
            "success": True,
            "user": user.dict(),
            "token": jwt_token,
            "message": "Login successful"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling Google callback: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@oauth_router.post("/verify-token")
async def verify_google_token(request: Dict[str, Any]):
    """Verify Google ID token directly (for frontend integration)"""
    try:
        id_token = request.get('id_token')
        if not id_token:
            raise HTTPException(status_code=400, detail="ID token is required")
        
        # Verify token and get user info
        user_info = await google_oauth.verify_google_token(id_token)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Create or get user
        user = await google_oauth.create_or_get_user(user_info)
        
        # Generate JWT token using user_auth module for consistency
        from user_auth import create_user_access_token
        from datetime import timedelta
        
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
            "message": "Google login successful"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying Google token: {str(e)}")
        raise HTTPException(status_code=500, detail="Token verification failed")

@oauth_router.post("/logout")
async def google_logout():
    """Handle Google OAuth logout"""
    try:
        # In a real application, you might invalidate the token
        # For now, just return success message
        return {
            "success": True,
            "message": "Logged out successfully"
        }
        
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(status_code=500, detail="Logout failed")

@oauth_router.get("/user-info")
async def get_google_user_info(access_token: str):
    """Get user info from Google using access token"""
    try:
        import requests
        
        # Get user info from Google API
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers=headers
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        user_info = response.json()
        return {
            "success": True,
            "user_info": user_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user info")