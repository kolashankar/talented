#!/usr/bin/env python3
"""
Script to fix admin credentials and test login functionality
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent / "backend"))

async def fix_admin_credentials():
    """Fix admin credentials in the database"""
    try:
        # Import necessary modules
        from database import get_database
        from auth import get_password_hash
        from models import AdminUser

        print("🔧 Fixing admin credentials...")

        # Connect to database
        db = await get_database()
        if db is None:
            print("❌ Could not connect to database")
            return False

        # Admin credentials
        admin_email = "kolashankar113@gmail.com"
        admin_password = "Shankar@113"
        admin_username = "admin"

        # Hash the password
        hashed_password = get_password_hash(admin_password)

        # Check if admin already exists
        existing_admin = await db.admin_users.find_one({"email": admin_email})

        if existing_admin:
            print(f"📝 Updating existing admin: {admin_email}")

            # Update the existing admin
            result = await db.admin_users.update_one(
                {"email": admin_email},
                {
                    "$set": {
                        "username": admin_username,
                        "hashed_password": hashed_password,
                        "is_active": True,
                        "is_superuser": True
                    }
                }
            )

            if result.modified_count > 0:
                print("✅ Admin credentials updated successfully")
            else:
                print("⚠️  Admin credentials were already correct")
        else:
            print(f"➕ Creating new admin: {admin_email}")

            # Create new admin
            admin_user = AdminUser(
                username=admin_username,
                email=admin_email,
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=True
            )

            admin_dict = admin_user.dict()
            result = await db.admin_users.insert_one(admin_dict)

            if result.inserted_id:
                print("✅ Admin user created successfully")
            else:
                print("❌ Failed to create admin user")
                return False

        # Verify the admin can be found
        admin = await db.admin_users.find_one({"email": admin_email})
        if admin:
            print(f"✅ Admin verified in database:")
            print(f"   - Email: {admin['email']}")
            print(f"   - Username: {admin['username']}")
            print(f"   - Active: {admin['is_active']}")
            print(f"   - Superuser: {admin['is_superuser']}")
        else:
            print("❌ Admin not found after creation/update")
            return False

        return True

    except Exception as e:
        print(f"❌ Error fixing admin credentials: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_admin_login():
    """Test admin login functionality"""
    try:
        from auth import authenticate_admin

        print("\n🧪 Testing admin authentication...")

        # Test with email
        admin = await authenticate_admin("kolashankar113@gmail.com", "Shankar@113")
        if admin:
            print("✅ Login with email successful")
            print(f"   - Username: {admin.username}")
            print(f"   - Email: {admin.email}")
            print(f"   - Active: {admin.is_active}")
        else:
            print("❌ Login with email failed")
            return False

        # Test with username
        admin = await authenticate_admin("admin", "Shankar@113")
        if admin:
            print("✅ Login with username successful")
        else:
            print("❌ Login with username failed")

        return True

    except Exception as e:
        print(f"❌ Error testing admin login: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function"""
    print("🎯 Admin Credentials Fix & Test Script")
    print("=" * 50)

    # Initialize database connection
    try:
        from database import connect_to_mongo, close_mongo_connection
        await connect_to_mongo()
        print("✅ Connected to database")
    except Exception as e:
        print(f"❌ Failed to connect to database: {str(e)}")
        return

    # Fix credentials
    if await fix_admin_credentials():
        # Test login
        await test_admin_login()

    # Close database connection
    try:
        await close_mongo_connection()
        print("✅ Database connection closed")
    except Exception as e:
        print(f"⚠️  Error closing database: {str(e)}")

    print("\n" + "=" * 50)
    print("Script completed")

if __name__ == "__main__":
    asyncio.run(main())
