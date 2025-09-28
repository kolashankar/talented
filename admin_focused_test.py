#!/usr/bin/env python3
"""
Focused Admin Authentication System Test
Tests admin login, authentication, and basic admin endpoints
"""

import asyncio
import aiohttp
import json

BACKEND_URL = "https://fix-render-loop.preview.emergentagent.com/api"
ADMIN_EMAIL = "kolashankar113@gmail.com"
ADMIN_PASSWORD = "Shankar@113"

class AdminAuthTester:
    def __init__(self):
        self.session = None
        self.admin_token = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, message: str, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    async def test_admin_login(self):
        """Test admin login with correct credentials"""
        try:
            login_data = {
                "username": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }
            
            async with self.session.post(f"{BACKEND_URL}/auth/login", json=login_data) as response:
                if response.status == 200:
                    data = await response.json()
                    self.admin_token = data.get("access_token")
                    user_info = data.get("user", {})
                    token_type = data.get("token_type")
                    expires_in = data.get("expires_in")
                    
                    self.log_test("Admin Login", True, 
                                f"Login successful - User: {user_info.get('email')}, Token Type: {token_type}, Expires: {expires_in}s")
                    return True
                else:
                    error_data = await response.text()
                    self.log_test("Admin Login", False, 
                                f"Status: {response.status}", error_data)
                    return False
                    
        except Exception as e:
            self.log_test("Admin Login", False, f"Error: {str(e)}")
            return False
    
    async def test_admin_me_endpoint(self):
        """Test admin /me endpoint"""
        if not self.admin_token:
            self.log_test("Admin Me Endpoint", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            async with self.session.get(f"{BACKEND_URL}/auth/me", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_test("Admin Me Endpoint", True, 
                                f"User info retrieved - Email: {data.get('email')}, Username: {data.get('username')}, Superuser: {data.get('is_superuser')}")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Me Endpoint", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Admin Me Endpoint", False, f"Error: {str(e)}")
    
    async def test_admin_dashboard_stats(self):
        """Test admin dashboard stats endpoint"""
        if not self.admin_token:
            self.log_test("Admin Dashboard Stats", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            async with self.session.get(f"{BACKEND_URL}/admin/dashboard/stats", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    stats_count = len(data) if isinstance(data, dict) else 0
                    self.log_test("Admin Dashboard Stats", True, 
                                f"Dashboard stats retrieved - {stats_count} stat categories")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Dashboard Stats", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Admin Dashboard Stats", False, f"Error: {str(e)}")
    
    async def test_admin_jobs_endpoint(self):
        """Test admin jobs management endpoint"""
        if not self.admin_token:
            self.log_test("Admin Jobs Endpoint", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            async with self.session.get(f"{BACKEND_URL}/admin/jobs", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    jobs_count = len(data) if isinstance(data, list) else 0
                    self.log_test("Admin Jobs Endpoint", True, 
                                f"Jobs retrieved - {jobs_count} jobs found")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Jobs Endpoint", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Admin Jobs Endpoint", False, f"Error: {str(e)}")
    
    async def test_admin_internships_endpoint(self):
        """Test admin internships management endpoint"""
        if not self.admin_token:
            self.log_test("Admin Internships Endpoint", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            async with self.session.get(f"{BACKEND_URL}/admin/internships", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    internships_count = len(data) if isinstance(data, list) else 0
                    self.log_test("Admin Internships Endpoint", True, 
                                f"Internships retrieved - {internships_count} internships found")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Internships Endpoint", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Admin Internships Endpoint", False, f"Error: {str(e)}")
    
    async def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        try:
            invalid_credentials = [
                {"username": "admin", "password": "admin123"},
                {"username": "wrong@email.com", "password": "wrongpass"},
                {"username": ADMIN_EMAIL, "password": "wrongpass"}
            ]
            
            for creds in invalid_credentials:
                async with self.session.post(f"{BACKEND_URL}/auth/login", json=creds) as response:
                    if response.status == 401:
                        self.log_test(f"Invalid Login Test ({creds['username']})", True, 
                                    "Correctly rejected invalid credentials")
                    else:
                        self.log_test(f"Invalid Login Test ({creds['username']})", False, 
                                    f"Unexpected status: {response.status}")
                        
        except Exception as e:
            self.log_test("Invalid Credentials Test", False, f"Error: {str(e)}")
    
    async def test_unauthorized_access(self):
        """Test accessing protected endpoints without token"""
        protected_endpoints = [
            "/auth/me",
            "/admin/dashboard/stats",
            "/admin/jobs",
            "/admin/internships"
        ]
        
        for endpoint in protected_endpoints:
            try:
                async with self.session.get(f"{BACKEND_URL}{endpoint}") as response:
                    if response.status == 401:
                        self.log_test(f"Unauthorized Access ({endpoint})", True, 
                                    "Correctly rejected request without token")
                    else:
                        self.log_test(f"Unauthorized Access ({endpoint})", False, 
                                    f"Unexpected status: {response.status}")
                        
            except Exception as e:
                self.log_test(f"Unauthorized Access ({endpoint})", False, f"Error: {str(e)}")
    
    async def run_all_tests(self):
        """Run all admin authentication tests"""
        print("🔐 Admin Authentication System Test")
        print("=" * 50)
        
        # Test admin login
        await self.test_admin_login()
        
        # Test authenticated endpoints
        await self.test_admin_me_endpoint()
        await self.test_admin_dashboard_stats()
        await self.test_admin_jobs_endpoint()
        await self.test_admin_internships_endpoint()
        
        # Test security
        await self.test_invalid_credentials()
        await self.test_unauthorized_access()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 ADMIN AUTH TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n" + "=" * 50)

async def main():
    """Main test runner"""
    async with AdminAuthTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())