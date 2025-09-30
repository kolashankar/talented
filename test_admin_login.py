#!/usr/bin/env python3
"""
Test admin login functionality to verify which credentials work
"""
import requests
import json
import os

# Backend URL
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

def test_admin_login(username, password):
    """Test admin login with given credentials"""
    url = f"{API_BASE}/auth/login"
    
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        print(f"Testing login with: {username} / {password}")
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True, data
        else:
            print("❌ Login failed!")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Exception during login test: {e}")
        return False, None

def test_auth_me(token):
    """Test /auth/me endpoint with token"""
    url = f"{API_BASE}/auth/me"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print(f"\nTesting /auth/me with token...")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ /auth/me successful!")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True, data
        else:
            print("❌ /auth/me failed!")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Exception during /auth/me test: {e}")
        return False, None

def main():
    print("🎯 Testing Admin Login Functionality")
    print("=" * 50)
    
    # Test credentials from test_result.md
    credentials_to_test = [
        ("kolashankar113@gmail.com", "Shankar@113"),
        ("admin", "admin123"),
    ]
    
    for username, password in credentials_to_test:
        print(f"\n📝 Testing credentials: {username}")
        print("-" * 30)
        
        success, data = test_admin_login(username, password)
        
        if success and data and "access_token" in data:
            # Test /auth/me endpoint
            token = data["access_token"]
            test_auth_me(token)
            print(f"✅ Credentials {username} / {password} work correctly!")
            break
        else:
            print(f"❌ Credentials {username} / {password} failed")
    
    print("\n" + "=" * 50)
    print("Admin login test completed")

if __name__ == "__main__":
    main()