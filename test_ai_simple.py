#!/usr/bin/env python3
"""
Simple AI service test to debug the JSON parsing issue
"""

import asyncio
import aiohttp
import json

BACKEND_URL = "https://multi-footer.preview.emergentagent.com/api"
ADMIN_EMAIL = "kolashankar113@gmail.com"
ADMIN_PASSWORD = "Shankar@113"

async def test_ai_service():
    async with aiohttp.ClientSession() as session:
        # First login to get admin token
        login_data = {
            "username": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        async with session.post(f"{BACKEND_URL}/auth/login", json=login_data) as response:
            if response.status != 200:
                print("Failed to login")
                return
            
            data = await response.json()
            admin_token = data.get("access_token")
            print(f"✅ Admin login successful")
        
        # Test AI generate job with query parameter
        headers = {"Authorization": f"Bearer {admin_token}"}
        params = {"prompt": "Create a simple Python developer job"}
        
        async with session.post(f"{BACKEND_URL}/ai/generate-job", 
                               params=params, headers=headers) as response:
            print(f"AI Generate Job Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"✅ AI Generate Job successful: {data.get('message', 'OK')}")
            else:
                error_data = await response.text()
                print(f"❌ AI Generate Job failed: {error_data}")

if __name__ == "__main__":
    asyncio.run(test_ai_service())