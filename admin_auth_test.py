#!/usr/bin/env python3
"""
Quick test to determine which admin credentials work
"""

import asyncio
import aiohttp
import json

BACKEND_URL = "https://dsa-feature-hub.preview.emergentagent.com/api"

async def test_admin_credentials():
    """Test different admin credential combinations"""
    
    # Different credential combinations to test
    credentials_to_test = [
        {"username": "admin", "password": "admin123", "description": "Backend log credentials"},
        {"username": "kolashankar113@gmail.com", "password": "Shankar@113", "description": "Environment/test_result.md credentials"},
        {"username": "admin", "password": "Shankar@113", "description": "Username from code + env password"},
    ]
    
    async with aiohttp.ClientSession() as session:
        print("🔐 Testing Admin Authentication Credentials")
        print("=" * 50)
        
        for i, creds in enumerate(credentials_to_test, 1):
            print(f"\n{i}. Testing {creds['description']}:")
            print(f"   Username: {creds['username']}")
            print(f"   Password: {creds['password']}")
            
            try:
                login_data = {
                    "username": creds["username"],
                    "password": creds["password"]
                }
                
                async with session.post(f"{BACKEND_URL}/auth/login", json=login_data) as response:
                    if response.status == 200:
                        data = await response.json()
                        user_info = data.get("user", {})
                        print(f"   ✅ SUCCESS - Logged in as: {user_info.get('email', 'N/A')}")
                        
                        # Test the /me endpoint with this token
                        token = data.get("access_token")
                        if token:
                            headers = {"Authorization": f"Bearer {token}"}
                            async with session.get(f"{BACKEND_URL}/auth/me", headers=headers) as me_response:
                                if me_response.status == 200:
                                    me_data = await me_response.json()
                                    print(f"   ✅ /auth/me endpoint working - User: {me_data.get('email', 'N/A')}")
                                    
                                    # Test admin dashboard stats endpoint
                                    async with session.get(f"{BACKEND_URL}/admin/dashboard/stats", headers=headers) as stats_response:
                                        if stats_response.status == 200:
                                            stats_data = await stats_response.json()
                                            print(f"   ✅ Admin dashboard stats working - Found {len(stats_data)} stats")
                                        else:
                                            print(f"   ⚠️  Admin dashboard stats failed - Status: {stats_response.status}")
                                else:
                                    print(f"   ❌ /auth/me endpoint failed - Status: {me_response.status}")
                        
                        return creds  # Return working credentials
                        
                    else:
                        error_text = await response.text()
                        print(f"   ❌ FAILED - Status: {response.status}")
                        if response.status == 401:
                            print(f"   📝 Error: Invalid credentials")
                        else:
                            print(f"   📝 Error: {error_text}")
                            
            except Exception as e:
                print(f"   ❌ ERROR - {str(e)}")
        
        print("\n" + "=" * 50)
        return None

async def main():
    working_creds = await test_admin_credentials()
    if working_creds:
        print(f"\n🎉 WORKING CREDENTIALS FOUND:")
        print(f"   Username: {working_creds['username']}")
        print(f"   Password: {working_creds['password']}")
        print(f"   Description: {working_creds['description']}")
    else:
        print("\n❌ NO WORKING CREDENTIALS FOUND")
        print("   Check backend logs and database for issues")

if __name__ == "__main__":
    asyncio.run(main())