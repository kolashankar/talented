#!/usr/bin/env python3
"""
Script to test and fix admin login functionality
"""
import asyncio
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

async def main():
    """Main function to test and fix admin login"""
    try:
        # Import after adding to path
        from database import connect_to_mongo, get_database, close_mongo_connection
        from auth import create_default_admin, authenticate_admin, get_password_hash
        from models import AdminUser
        
        print("🔧 Admin Login Fix Script")
        print("=" * 50)
        
        # Connect to database
        print("📡 Connecting to database...")
        await connect_to_mongo()
        print("✅ Connected to database")
        
        # Get database instance
        db = await get_database()
        
        # Check existing admin users
        print("\n📋 Checking existing admin users...")
        admin_users = await db.admin_users.find({}).to_list(length=None)
        print(f"Found {len(admin_users)} admin users:")
        
        for admin in admin_users:
            print(f"  - Username: {admin.get('username')}")
            print(f"    Email: {admin.get('email')}")
            print(f"    Active: {admin.get('is_active')}")
            print(f"    Superuser: {admin.get('is_superuser')}")
            print()
        
        # Test credentials
        test_email = "kolashankar113@gmail.com"
        test_password = "Shankar@113"
        
        print(f"🔐 Testing authentication with {test_email}...")
        
        # Try to authenticate
        admin = await authenticate_admin(test_email, test_password)
        
        if admin:
            print("✅ Authentication successful!")
            print(f"Admin found: {admin.username} ({admin.email})")
        else:
            print("❌ Authentication failed!")
            print("🔧 Attempting to fix...")
            
            # Create/update admin user
            await create_default_admin()
            
            # Test again
            print(f"🔐 Testing authentication again...")
            admin = await authenticate_admin(test_email, test_password)
            
            if admin:
                print("✅ Authentication successful after fix!")
                print(f"Admin found: {admin.username} ({admin.email})")
            else:
                print("❌ Authentication still failing!")
                
                # Manual fix - ensure admin exists with correct password
                print("🔧 Performing manual fix...")
                
                # Check if admin exists
                existing_admin = await db.admin_users.find_one({"email": test_email})
                
                if existing_admin:
                    # Update password
                    hashed_password = get_password_hash(test_password)
                    await db.admin_users.update_one(
                        {"email": test_email},
                        {"$set": {
                            "hashed_password": hashed_password,
                            "is_active": True,
                            "is_superuser": True
                        }}
                    )
                    print("✅ Updated existing admin password")
                else:
                    # Create new admin
                    admin_user = AdminUser(
                        username="admin",
                        email=test_email,
                        hashed_password=get_password_hash(test_password),
                        is_active=True,
                        is_superuser=True
                    )
                    
                    admin_dict = admin_user.dict()
                    await db.admin_users.insert_one(admin_dict)
                    print("✅ Created new admin user")
                
                # Final test
                print(f"🔐 Final authentication test...")
                admin = await authenticate_admin(test_email, test_password)
                
                if admin:
                    print("✅ Authentication successful after manual fix!")
                    print(f"Admin found: {admin.username} ({admin.email})")
                else:
                    print("❌ Authentication still failing - there may be a deeper issue")
        
        # Close database connection
        await close_mongo_connection()
        print("\n🎯 Admin login fix script completed")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
