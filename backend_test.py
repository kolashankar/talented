#!/usr/bin/env python3
"""
Comprehensive Backend Testing for TalentD Platform Phase 2
Tests all backend APIs including authentication, resume processing, and portfolio builder
"""

import asyncio
import aiohttp
import json
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime

# Test configuration
BACKEND_URL = "https://dsa-feature-hub.preview.emergentagent.com/api"
ADMIN_EMAIL = "kolashankar113@gmail.com"
ADMIN_PASSWORD = "Shankar@113"

class TalentDBackendTester:
    def __init__(self):
        self.session = None
        self.admin_token = None
        self.user_token = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, message: str, details: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    async def test_health_check(self):
        """Test basic health check endpoints"""
        try:
            # Test root endpoint
            async with self.session.get(f"{BACKEND_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_test("Health Check Root", True, f"API is running: {data.get('message', 'OK')}")
                else:
                    self.log_test("Health Check Root", False, f"Status: {response.status}")
            
            # Test health endpoint
            async with self.session.get(f"{BACKEND_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_test("Health Check Endpoint", True, f"Health status: {data.get('status', 'OK')}")
                else:
                    self.log_test("Health Check Endpoint", False, f"Status: {response.status}")
                    
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
    
    async def test_admin_authentication(self):
        """Test admin authentication with specified credentials"""
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
                    self.log_test("Admin Login", True, 
                                f"Login successful for {user_info.get('email', 'admin')}")
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
        """Test admin /me endpoint with authentication"""
        if not self.admin_token:
            self.log_test("Admin Me Endpoint", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            async with self.session.get(f"{BACKEND_URL}/auth/me", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_test("Admin Me Endpoint", True, 
                                f"Retrieved admin info: {data.get('email', 'N/A')}")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Me Endpoint", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Admin Me Endpoint", False, f"Error: {str(e)}")
    
    async def test_user_auth_me_endpoint(self):
        """Test user authentication /me endpoint (should fail without token)"""
        try:
            async with self.session.get(f"{BACKEND_URL}/user-auth/me") as response:
                if response.status in [401, 403]:  # Both are acceptable for unauthorized access
                    self.log_test("User Auth Me (No Token)", True, 
                                "Correctly rejected request without token")
                else:
                    self.log_test("User Auth Me (No Token)", False, 
                                f"Unexpected status: {response.status}")
                    
        except Exception as e:
            self.log_test("User Auth Me (No Token)", False, f"Error: {str(e)}")
    
    async def test_resume_upload_without_auth(self):
        """Test resume upload endpoint without authentication (should fail)"""
        try:
            # Create a simple test file
            test_resume_content = """
            John Doe
            Software Engineer
            Email: john.doe@example.com
            Phone: +91-9876543210
            
            Experience:
            - Software Developer at TechCorp (2022-2024)
            - Developed web applications using React and Node.js
            
            Skills:
            - JavaScript, Python, React, Node.js
            - MongoDB, PostgreSQL
            
            Education:
            - B.Tech Computer Science, ABC University (2018-2022)
            """
            
            # Try to upload without authentication
            data = aiohttp.FormData()
            data.add_field('resume_file', test_resume_content.encode(), 
                          filename='test_resume.txt', content_type='text/plain')
            data.add_field('target_role', 'Software Engineer')
            
            async with self.session.post(f"{BACKEND_URL}/resume/upload-analyze", data=data) as response:
                if response.status in [401, 403]:  # Both are acceptable for unauthorized access
                    self.log_test("Resume Upload (No Auth)", True, 
                                "Correctly rejected request without authentication")
                else:
                    error_data = await response.text()
                    self.log_test("Resume Upload (No Auth)", False, 
                                f"Unexpected status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Resume Upload (No Auth)", False, f"Error: {str(e)}")
    
    async def test_portfolio_templates(self):
        """Test portfolio templates endpoint (should be public)"""
        try:
            async with self.session.get(f"{BACKEND_URL}/portfolio/templates") as response:
                if response.status == 200:
                    data = await response.json()
                    template_count = len(data) if isinstance(data, list) else 0
                    self.log_test("Portfolio Templates", True, 
                                f"Retrieved {template_count} templates")
                else:
                    error_data = await response.text()
                    self.log_test("Portfolio Templates", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Portfolio Templates", False, f"Error: {str(e)}")
    
    async def test_ai_generate_content_with_admin_auth(self):
        """Test AI content generation with admin authentication"""
        if not self.admin_token:
            self.log_test("AI Generate Content", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            content_request = {
                "content_type": "job",
                "prompt": "Create a job posting for a Python developer position at a tech startup",
                "additional_context": {
                    "location": "Bangalore",
                    "experience": "2-4 years"
                }
            }
            
            async with self.session.post(f"{BACKEND_URL}/ai/generate-content", 
                                       json=content_request, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data.get("content", {})
                    self.log_test("AI Generate Content", True, 
                                f"Generated job content with title: {content.get('title', 'N/A')}")
                else:
                    error_data = await response.text()
                    self.log_test("AI Generate Content", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("AI Generate Content", False, f"Error: {str(e)}")
    
    async def test_ai_generate_job_content(self):
        """Test specific AI job generation endpoint"""
        if not self.admin_token:
            self.log_test("AI Generate Job", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            # The endpoint expects prompt as a query parameter or form data
            params = {"prompt": "Senior React Developer at fintech company"}
            
            async with self.session.post(f"{BACKEND_URL}/ai/generate-job", 
                                       params=params,
                                       headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data.get("content", {})
                    self.log_test("AI Generate Job", True, 
                                f"Generated job: {content.get('title', 'N/A') if isinstance(content, dict) else 'Generated successfully'}")
                else:
                    error_data = await response.text()
                    self.log_test("AI Generate Job", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("AI Generate Job", False, f"Error: {str(e)}")
    
    async def test_mock_google_user_auth(self):
        """Test user authentication with mock Google OAuth data"""
        try:
            # Mock Google OAuth user data
            google_user_data = {
                "email": "testuser@gmail.com",
                "name": "Test User",
                "google_id": "123456789",
                "profile_picture": "https://example.com/avatar.jpg"
            }
            
            async with self.session.post(f"{BACKEND_URL}/user-auth/google-login", 
                                       json=google_user_data) as response:
                if response.status == 200:
                    data = await response.json()
                    self.user_token = data.get("access_token")
                    user_info = data.get("user", {})
                    self.log_test("Mock Google User Auth", True, 
                                f"User authenticated: {user_info.get('email', 'N/A')}")
                    return True
                else:
                    error_data = await response.text()
                    self.log_test("Mock Google User Auth", False, 
                                f"Status: {response.status}", error_data)
                    return False
                    
        except Exception as e:
            self.log_test("Mock Google User Auth", False, f"Error: {str(e)}")
            return False
    
    async def test_resume_parse_with_user_auth(self):
        """Test resume parsing with user authentication"""
        if not self.user_token:
            self.log_test("Resume Parse (User Auth)", False, "No user token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            resume_text = """
            Jane Smith
            Full Stack Developer
            jane.smith@email.com | +91-9876543210 | Bangalore, India
            LinkedIn: linkedin.com/in/janesmith | GitHub: github.com/janesmith
            
            EXPERIENCE
            Senior Software Engineer | TechCorp | Jan 2022 - Present
            • Developed and maintained web applications using React, Node.js, and MongoDB
            • Led a team of 3 developers on multiple projects
            • Improved application performance by 40%
            
            Software Developer | StartupXYZ | Jun 2020 - Dec 2021
            • Built RESTful APIs using Express.js and PostgreSQL
            • Implemented authentication and authorization systems
            
            PROJECTS
            E-commerce Platform
            • Built a full-stack e-commerce application with React and Node.js
            • Integrated payment gateway and inventory management
            • Technologies: React, Node.js, MongoDB, Stripe API
            
            Task Management App
            • Developed a collaborative task management application
            • Real-time updates using Socket.io
            • Technologies: Vue.js, Express.js, PostgreSQL
            
            SKILLS
            Frontend: React, Vue.js, JavaScript, TypeScript, HTML, CSS
            Backend: Node.js, Express.js, Python, Django
            Databases: MongoDB, PostgreSQL, MySQL
            Tools: Git, Docker, AWS, Jenkins
            
            EDUCATION
            Bachelor of Technology in Computer Science
            ABC University | 2016 - 2020 | CGPA: 8.5/10
            
            CERTIFICATIONS
            • AWS Certified Developer Associate
            • MongoDB Certified Developer
            
            ACHIEVEMENTS
            • Winner of National Coding Competition 2019
            • Published research paper on Machine Learning applications
            """
            
            parse_request = {"resume_text": resume_text}
            
            async with self.session.post(f"{BACKEND_URL}/resume/parse", 
                                       json=parse_request, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    parsed_data = data.get("parsed_data", {})
                    personal = parsed_data.get("personal_details", {})
                    confidence = data.get("parsing_confidence", 0)
                    self.log_test("Resume Parse (User Auth)", True, 
                                f"Parsed resume for {personal.get('full_name', 'N/A')} with {confidence:.2f} confidence")
                else:
                    error_data = await response.text()
                    self.log_test("Resume Parse (User Auth)", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Resume Parse (User Auth)", False, f"Error: {str(e)}")
    
    async def test_portfolio_generation_with_user_auth(self):
        """Test portfolio generation with user authentication"""
        if not self.user_token:
            self.log_test("Portfolio Generation", False, "No user token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            
            # First get available templates
            async with self.session.get(f"{BACKEND_URL}/portfolio/templates") as response:
                if response.status != 200:
                    self.log_test("Portfolio Generation", False, "Could not fetch templates")
                    return
                    
                templates = await response.json()
                if not templates:
                    self.log_test("Portfolio Generation", False, "No templates available")
                    return
                
                template_id = templates[0]["id"]
            
            # Create portfolio generation request
            portfolio_request = {
                "template_id": template_id,
                "user_prompt": "Create a modern, professional portfolio for a full-stack developer",
                "resume_data": {
                    "personal_details": {
                        "full_name": "John Developer",
                        "email": "john@example.com",
                        "phone": "+91-9876543210",
                        "location": "Bangalore, India",
                        "linkedin": "linkedin.com/in/johndeveloper",
                        "github": "github.com/johndeveloper",
                        "bio": "Passionate full-stack developer with 3+ years of experience"
                    },
                    "education": [
                        {
                            "degree": "B.Tech Computer Science",
                            "institution": "ABC University",
                            "year": "2020",
                            "cgpa": "8.5"
                        }
                    ],
                    "experience": [
                        {
                            "title": "Software Engineer",
                            "company": "TechCorp",
                            "duration": "2021-2024",
                            "location": "Bangalore",
                            "description": ["Developed web applications", "Led team projects"]
                        }
                    ],
                    "projects": [
                        {
                            "name": "E-commerce Platform",
                            "description": "Full-stack e-commerce application",
                            "technologies": ["React", "Node.js", "MongoDB"],
                            "github_url": "https://github.com/johndeveloper/ecommerce"
                        }
                    ],
                    "skills": ["JavaScript", "React", "Node.js", "MongoDB", "Python"],
                    "certifications": ["AWS Certified Developer"],
                    "achievements": ["Winner of Coding Competition 2023"]
                },
                "additional_preferences": {
                    "theme": "modern",
                    "color_scheme": "blue"
                }
            }
            
            async with self.session.post(f"{BACKEND_URL}/portfolio/generate", 
                                       json=portfolio_request, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    live_url = data.get("live_url", "N/A")
                    self.log_test("Portfolio Generation", True, 
                                f"Portfolio generated successfully: {live_url}")
                else:
                    error_data = await response.text()
                    self.log_test("Portfolio Generation", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Portfolio Generation", False, f"Error: {str(e)}")
    
    async def test_user_portfolios_endpoint(self):
        """Test user portfolios listing endpoint"""
        if not self.user_token:
            self.log_test("User Portfolios List", False, "No user token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            
            async with self.session.get(f"{BACKEND_URL}/portfolio/my-portfolios", 
                                      headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    portfolio_count = len(data) if isinstance(data, list) else 0
                    self.log_test("User Portfolios List", True, 
                                f"Retrieved {portfolio_count} user portfolios")
                else:
                    error_data = await response.text()
                    self.log_test("User Portfolios List", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("User Portfolios List", False, f"Error: {str(e)}")
    
    async def test_footer_pages_endpoints(self):
        """Test footer pages endpoints"""
        try:
            # Test get all pages
            async with self.session.get(f"{BACKEND_URL}/pages/") as response:
                if response.status == 200:
                    data = await response.json()
                    pages = data.get("pages", [])
                    self.log_test("Footer Pages List", True, 
                                f"Retrieved {len(pages)} footer pages")
                    
                    # Test individual page access
                    if pages:
                        test_page = pages[0]
                        slug = test_page.get("slug", "")
                        if slug:
                            async with self.session.get(f"{BACKEND_URL}/pages/{slug}") as page_response:
                                if page_response.status == 200:
                                    page_data = await page_response.json()
                                    self.log_test("Footer Page by Slug", True, 
                                                f"Retrieved page: {page_data.get('page', {}).get('title', 'N/A')}")
                                else:
                                    self.log_test("Footer Page by Slug", False, 
                                                f"Status: {page_response.status}")
                else:
                    error_data = await response.text()
                    self.log_test("Footer Pages List", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Footer Pages", False, f"Error: {str(e)}")

    async def test_company_endpoints(self):
        """Test company profile endpoints"""
        try:
            # Test search companies
            async with self.session.get(f"{BACKEND_URL}/companies/") as response:
                if response.status == 200:
                    data = await response.json()
                    companies = data.get("companies", [])
                    total = data.get("total", 0)
                    self.log_test("Company Search", True, 
                                f"Retrieved {len(companies)} companies (total: {total})")
                    
                    # Test with search parameter
                    async with self.session.get(f"{BACKEND_URL}/companies/?search=tech") as search_response:
                        if search_response.status == 200:
                            search_data = await search_response.json()
                            self.log_test("Company Search with Filter", True, 
                                        f"Search results: {len(search_data.get('companies', []))}")
                        else:
                            self.log_test("Company Search with Filter", False, 
                                        f"Status: {search_response.status}")
                else:
                    error_data = await response.text()
                    self.log_test("Company Search", False, 
                                f"Status: {response.status}", error_data)
            
            # Test industry stats
            async with self.session.get(f"{BACKEND_URL}/companies/stats/industries") as response:
                if response.status == 200:
                    data = await response.json()
                    industries = data.get("industries", [])
                    self.log_test("Company Industry Stats", True, 
                                f"Retrieved {len(industries)} industry statistics")
                else:
                    error_data = await response.text()
                    self.log_test("Company Industry Stats", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Company Endpoints", False, f"Error: {str(e)}")

    async def test_dsa_endpoints(self):
        """Test DSA problem endpoints"""
        try:
            # Test get categories
            async with self.session.get(f"{BACKEND_URL}/dsa/categories") as response:
                if response.status == 200:
                    data = await response.json()
                    categories = data.get("categories", [])
                    self.log_test("DSA Categories", True, 
                                f"Retrieved {len(categories)} DSA categories")
                else:
                    error_data = await response.text()
                    self.log_test("DSA Categories", False, 
                                f"Status: {response.status}", error_data)
            
            # Test get problems
            async with self.session.get(f"{BACKEND_URL}/dsa/problems") as response:
                if response.status == 200:
                    data = await response.json()
                    problems = data.get("problems", [])
                    total = data.get("total", 0)
                    self.log_test("DSA Problems List", True, 
                                f"Retrieved {len(problems)} problems (total: {total})")
                else:
                    error_data = await response.text()
                    self.log_test("DSA Problems List", False, 
                                f"Status: {response.status}", error_data)
            
            # Test user progress (requires authentication)
            if self.user_token:
                headers = {"Authorization": f"Bearer {self.user_token}"}
                async with self.session.get(f"{BACKEND_URL}/dsa/progress", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        total_solved = data.get("total_solved", 0)
                        total_problems = data.get("total_problems", 0)
                        self.log_test("DSA User Progress", True, 
                                    f"User progress: {total_solved}/{total_problems} solved")
                    else:
                        error_data = await response.text()
                        self.log_test("DSA User Progress", False, 
                                    f"Status: {response.status}", error_data)
            else:
                self.log_test("DSA User Progress", False, "No user token available")
                    
        except Exception as e:
            self.log_test("DSA Endpoints", False, f"Error: {str(e)}")

    async def test_interaction_endpoints(self):
        """Test user interaction endpoints"""
        if not self.user_token:
            self.log_test("User Interactions", False, "No user token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            
            # Test like functionality
            test_content_id = "test-article-123"
            async with self.session.post(f"{BACKEND_URL}/interactions/article/{test_content_id}/like", 
                                       headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    liked = data.get("liked", False)
                    total_likes = data.get("total_likes", 0)
                    self.log_test("Like Content", True, 
                                f"Like toggled: {liked}, Total likes: {total_likes}")
                else:
                    error_data = await response.text()
                    self.log_test("Like Content", False, 
                                f"Status: {response.status}", error_data)
            
            # Test save functionality
            async with self.session.post(f"{BACKEND_URL}/interactions/article/{test_content_id}/save", 
                                       headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    saved = data.get("saved", False)
                    message = data.get("message", "")
                    self.log_test("Save Content", True, 
                                f"Save toggled: {saved}, Message: {message}")
                else:
                    error_data = await response.text()
                    self.log_test("Save Content", False, 
                                f"Status: {response.status}", error_data)
            
            # Test share functionality
            async with self.session.post(f"{BACKEND_URL}/interactions/article/{test_content_id}/share", 
                                       headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    share_url = data.get("share_url", "")
                    self.log_test("Share Content", True, 
                                f"Content shared: {share_url}")
                else:
                    error_data = await response.text()
                    self.log_test("Share Content", False, 
                                f"Status: {response.status}", error_data)
            
            # Test get saved items
            async with self.session.get(f"{BACKEND_URL}/interactions/saved", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    saved_items = data.get("saved_items", [])
                    self.log_test("Get Saved Items", True, 
                                f"Retrieved {len(saved_items)} saved items")
                else:
                    error_data = await response.text()
                    self.log_test("Get Saved Items", False, 
                                f"Status: {response.status}", error_data)
            
            # Test interaction status
            async with self.session.get(f"{BACKEND_URL}/interactions/article/{test_content_id}/status", 
                                      headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    liked = data.get("liked", False)
                    saved = data.get("saved", False)
                    total_likes = data.get("total_likes", 0)
                    self.log_test("Interaction Status", True, 
                                f"Status - Liked: {liked}, Saved: {saved}, Total likes: {total_likes}")
                else:
                    error_data = await response.text()
                    self.log_test("Interaction Status", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("User Interactions", False, f"Error: {str(e)}")

    async def test_existing_admin_endpoints(self):
        """Test existing admin endpoints to ensure they still work"""
        if not self.admin_token:
            self.log_test("Admin Endpoints", False, "No admin token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            # Test admin dashboard stats
            async with self.session.get(f"{BACKEND_URL}/admin/dashboard/stats", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_test("Admin Dashboard Stats", True, 
                                f"Retrieved dashboard statistics")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Dashboard Stats", False, 
                                f"Status: {response.status}", error_data)
            
            # Test admin jobs endpoint
            async with self.session.get(f"{BACKEND_URL}/admin/jobs", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    jobs = data.get("jobs", []) if isinstance(data, dict) else data
                    self.log_test("Admin Jobs List", True, 
                                f"Retrieved {len(jobs) if isinstance(jobs, list) else 'N/A'} jobs")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Jobs List", False, 
                                f"Status: {response.status}", error_data)
            
            # Test admin internships endpoint
            async with self.session.get(f"{BACKEND_URL}/admin/internships", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    internships = data.get("internships", []) if isinstance(data, dict) else data
                    self.log_test("Admin Internships List", True, 
                                f"Retrieved {len(internships) if isinstance(internships, list) else 'N/A'} internships")
                else:
                    error_data = await response.text()
                    self.log_test("Admin Internships List", False, 
                                f"Status: {response.status}", error_data)
                    
        except Exception as e:
            self.log_test("Admin Endpoints", False, f"Error: {str(e)}")

    async def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting TalentD Platform Backend Tests")
        print("=" * 60)
        
        # Basic connectivity tests
        await self.test_health_check()
        
        # Admin authentication tests
        await self.test_admin_authentication()
        await self.test_admin_me_endpoint()
        
        # User authentication tests
        await self.test_user_auth_me_endpoint()
        await self.test_mock_google_user_auth()
        
        # NEW: Test new API endpoints
        print("\n🔍 Testing New API Endpoints...")
        await self.test_footer_pages_endpoints()
        await self.test_company_endpoints()
        await self.test_dsa_endpoints()
        await self.test_interaction_endpoints()
        
        # Test existing functionality
        print("\n🔄 Testing Existing Functionality...")
        await self.test_existing_admin_endpoints()
        
        # Resume processing tests
        await self.test_resume_upload_without_auth()
        await self.test_resume_parse_with_user_auth()
        
        # Portfolio builder tests
        await self.test_portfolio_templates()
        await self.test_portfolio_generation_with_user_auth()
        await self.test_user_portfolios_endpoint()
        
        # AI service tests
        await self.test_ai_generate_content_with_admin_auth()
        await self.test_ai_generate_job_content()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
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
        
        print("\n" + "=" * 60)

async def main():
    """Main test runner"""
    async with TalentDBackendTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())