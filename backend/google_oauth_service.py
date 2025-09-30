import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import jwt
from models import User, UserCreate
from database import get_database

logger = logging.getLogger(__name__)

class GoogleOAuthService:
    def __init__(self):
        self.client_id = os.environ.get('GOOGLE_CLIENT_ID')
        self.client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            logger.warning("Google OAuth credentials not fully configured")

    def get_authorization_url(self) -> str:
        """Generate Google OAuth authorization URL"""
        try:
            if not self.client_id or not self.redirect_uri:
                raise ValueError("Google OAuth not properly configured")
            
            # Create OAuth 2.0 flow
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=['openid', 'email', 'profile']
            )
            
            flow.redirect_uri = self.redirect_uri
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            return authorization_url
            
        except Exception as e:
            logger.error(f"Error generating authorization URL: {str(e)}")
            raise

    async def exchange_code_for_tokens(self, authorization_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token and user info"""
        try:
            if not all([self.client_id, self.client_secret, self.redirect_uri]):
                raise ValueError("Google OAuth not properly configured")
            
            # Exchange authorization code for tokens
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': authorization_code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri
            }
            
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            tokens = token_response.json()
            
            # Verify ID token and get user info
            id_token_jwt = tokens.get('id_token')
            if not id_token_jwt:
                raise ValueError("No ID token received")
            
            # Verify the ID token
            idinfo = id_token.verify_oauth2_token(
                id_token_jwt, 
                google_requests.Request(), 
                self.client_id
            )
            
            # Extract user information
            user_info = {
                'google_id': idinfo.get('sub'),
                'email': idinfo.get('email'),
                'name': idinfo.get('name'),
                'profile_picture': idinfo.get('picture'),
                'email_verified': idinfo.get('email_verified', False)
            }
            
            return {
                'user_info': user_info,
                'access_token': tokens.get('access_token'),
                'refresh_token': tokens.get('refresh_token'),
                'expires_in': tokens.get('expires_in')
            }
            
        except Exception as e:
            logger.error(f"Error exchanging code for tokens: {str(e)}")
            raise

    async def verify_google_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify Google ID token and return user info"""
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                self.client_id
            )
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            # Return user info
            return {
                'google_id': idinfo.get('sub'),
                'email': idinfo.get('email'),
                'name': idinfo.get('name'),
                'profile_picture': idinfo.get('picture'),
                'email_verified': idinfo.get('email_verified', False)
            }
            
        except ValueError as e:
            logger.error(f"Invalid token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error verifying Google token: {str(e)}")
            return None

    async def create_or_get_user(self, user_info: Dict[str, Any]) -> User:
        """Create a new user or get existing user from Google OAuth info"""
        try:
            db = await get_database()
            
            # Check if user already exists
            existing_user = await db.users.find_one({
                "$or": [
                    {"google_id": user_info['google_id']},
                    {"email": user_info['email']}
                ]
            })
            
            if existing_user:
                # Update existing user with latest info
                update_data = {
                    "name": user_info.get('name', existing_user.get('name')),
                    "profile_picture": user_info.get('profile_picture', existing_user.get('profile_picture')),
                    "last_login": datetime.utcnow()
                }
                
                # Update Google ID if not set
                if not existing_user.get('google_id') and user_info.get('google_id'):
                    update_data['google_id'] = user_info['google_id']
                
                await db.users.update_one(
                    {"id": existing_user['id']},
                    {"$set": update_data}
                )
                
                # Return updated user
                updated_user = await db.users.find_one({"id": existing_user['id']})
                return User(**updated_user)
            else:
                # Create new user
                new_user_data = UserCreate(
                    email=user_info['email'],
                    google_id=user_info['google_id'],
                    name=user_info.get('name', ''),
                    profile_picture=user_info.get('profile_picture')
                )
                
                new_user = User(**new_user_data.dict())
                user_dict = new_user.dict()
                
                result = await db.users.insert_one(user_dict)
                if result.inserted_id:
                    return new_user
                else:
                    raise Exception("Failed to create user")
                    
        except Exception as e:
            logger.error(f"Error creating/getting user: {str(e)}")
            raise

    def generate_jwt_token(self, user: User) -> str:
        """Generate JWT token for user"""
        try:
            secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')
            expires_delta = timedelta(hours=24)
            
            payload = {
                'user_id': user.id,
                'email': user.email,
                'name': user.name,
                'exp': datetime.utcnow() + expires_delta,
                'iat': datetime.utcnow(),
                'type': 'user'
            }
            
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            return token
            
        except Exception as e:
            logger.error(f"Error generating JWT token: {str(e)}")
            raise

# Global instance
google_oauth = GoogleOAuthService()