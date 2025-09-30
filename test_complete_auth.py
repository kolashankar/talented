#!/usr/bin/env python3
"""
Complete authentication test script for both admin and user authentication
"""
import asyncio
import sys
import os
import requests
import json
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Backend URL
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

def test_endpoint(method, url, data=None, headers=None):
    """Test an API endpoint"""
    try:
        print(f"🔗 {method.upper()} {url}")
        if data:
            print(f"📤 Data: {json.dumps(data, indent=2)}")
        
        if method.lower() == 'post':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.lower() == 'get':
            response = requests.get(url, headers=headers, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False, None
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            try:
                result = response.json()
                print(f"✅ Success: {json.dumps(result, indent=2)}")
                return True, result
            except:
                print(f"✅ Success: {response.text}")
                return True, response.text
        else:
            try:
                error = response.json()
                print(f"❌ Error: {json.dumps(error, indent=2)}")
            except:
                print(f"❌ Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, None

async def test_database_setup():
    """Test database setup and admin creation"""
    try:
        from database import connect_to_mongo, get_database, close_mongo_connection
        from auth import create_default_admin
        
        print("📡 Connecting to database...")
        await connect_to_mongo()
        print("✅ Connected to database")
        
        print("👤 Creating default admin...")
        await create_default_admin()
        print("✅ Admin setup completed")
        
        # Check admin users
        db = await get_database()
        admin_count = await db.admin_users.count_documents({})
        user_count = await db.users.count_documents({})
        
        print(f"📊 Admin users: {admin_count}")
        print(f"📊 Regular users: {user_count}")
        
        await close_mongo_connection()
        return True
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("\n🔐 Testing User Registration")
    print("=" * 50)
    
    test_user = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "name": "Test User"
    }
    
    success, result = test_endpoint(
        "POST", 
        f"{API_BASE}/user-auth/register", 
        test_user
    )
    
    if success and result and "access_token" in result:
        print("✅ User registration successful!")
        return result["access_token"]
    else:
        print("❌ User registration failed!")
        return None

def test_user_login():
    """Test user login"""
    print("\n🔐 Testing User Login")
    print("=" * 50)
    
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    success, result = test_endpoint(
        "POST", 
        f"{API_BASE}/user-auth/login", 
        login_data
    )
    
    if success and result and "access_token" in result:
        print("✅ User login successful!")
        return result["access_token"]
    else:
        print("❌ User login failed!")
        return None

def test_admin_login():
    """Test admin login"""
    print("\n🔐 Testing Admin Login")
    print("=" * 50)
    
    admin_data = {
        "username": "kolashankar113@gmail.com",
        "password": "Shankar@113"
    }
    
    success, result = test_endpoint(
        "POST", 
        f"{API_BASE}/auth/login", 
        admin_data
    )
    
    if success and result and "access_token" in result:
        print("✅ Admin login successful!")
        return result["access_token"]
    else:
        print("❌ Admin login failed!")
        return None

def test_protected_endpoints(user_token, admin_token):
    """Test protected endpoints"""
    print("\n🛡️ Testing Protected Endpoints")
    print("=" * 50)
    
    # Test user protected endpoint
    if user_token:
        print("\n👤 Testing user protected endpoint...")
        headers = {"Authorization": f"Bearer {user_token}"}
        success, result = test_endpoint(
            "GET", 
            f"{API_BASE}/user-auth/me", 
            headers=headers
        )
        if success:
            print("✅ User protected endpoint works!")
        else:
            print("❌ User protected endpoint failed!")
    
    # Test admin protected endpoint
    if admin_token:
        print("\n👑 Testing admin protected endpoint...")
        headers = {"Authorization": f"Bearer {admin_token}"}
        success, result = test_endpoint(
            "GET", 
            f"{API_BASE}/auth/me", 
            headers=headers
        )
        if success:
            print("✅ Admin protected endpoint works!")
        else:
            print("❌ Admin protected endpoint failed!")

def test_health_endpoints():
    """Test health check endpoints"""
    print("\n💚 Testing Health Endpoints")
    print("=" * 50)
    
    endpoints = [
        f"{API_BASE}/",
        f"{API_BASE}/health",
        f"{API_BASE}/auth/health"
    ]
    
    for endpoint in endpoints:
        success, result = test_endpoint("GET", endpoint)
        if success:
            print(f"✅ {endpoint} is healthy")
        else:
            print(f"❌ {endpoint} is not responding")

async def main():
    """Main test function"""
    print("🧪 Complete Authentication Test Suite")
    print("=" * 60)
    
    # Test database setup
    print("\n📊 Testing Database Setup")
    print("=" * 50)
    db_success = await test_database_setup()
    
    if not db_success:
        print("❌ Database setup failed. Cannot continue with API tests.")
        return
    
    # Test health endpoints first
    test_health_endpoints()
    
    # Test user authentication
    user_token = test_user_registration()
    if not user_token:
        user_token = test_user_login()
    
    # Test admin authentication
    admin_token = test_admin_login()
    
    # Test protected endpoints
    test_protected_endpoints(user_token, admin_token)
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"✅ Database Setup: {'✓' if db_success else '✗'}")
    print(f"✅ User Authentication: {'✓' if user_token else '✗'}")
    print(f"✅ Admin Authentication: {'✓' if admin_token else '✗'}")
    
    if user_token and admin_token:
        print("\n🎉 All authentication systems are working correctly!")
    else:
        print("\n⚠️ Some authentication systems need attention.")
    
    print("\n🚀 Ready to test frontend integration!")

if __name__ == "__main__":
    asyncio.run(main())
