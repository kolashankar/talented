import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import google.generativeai as genai
import requests
import cloudinary
from cloudinary import uploader
from models import (
    JobCreate, InternshipCreate, ArticleCreate, 
    RoadmapCreate, DSAProblemCreate, DSADifficulty,
    AIFormFillerRequest, AIFormFillerResponse, ImageGenerationRequest, ImageGenerationResponse
)

logger = logging.getLogger(__name__)

# Initialize Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('REACT_APP_CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

class AIAgentService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision') if GEMINI_API_KEY else None

    async def generate_job_content(self, prompt: str = None, job_type: str = "software") -> Dict[str, Any]:
        """Generate realistic job posting content using AI"""
        try:
            if not prompt:
                prompt = f"Generate a realistic {job_type} job posting"
            
            system_prompt = f"""
            Generate a realistic and detailed job posting for a {job_type} position. 
            Return ONLY a valid JSON object with the following structure:
            {{
                "title": "Job title",
                "company": "Company name", 
                "description": "Detailed job description (2-3 paragraphs)",
                "requirements": ["requirement1", "requirement2", ...],
                "responsibilities": ["responsibility1", "responsibility2", ...],
                "location": "City, Country",
                "salary_min": 50000,
                "salary_max": 80000,
                "salary_currency": "INR", 
                "job_type": "full-time",
                "experience_level": "experienced",
                "skills_required": ["skill1", "skill2", ...],
                "benefits": ["benefit1", "benefit2", ...],
                "tags": ["tag1", "tag2", ...],
                "company_logo": "https://example.com/logo.jpg"
            }}
            
            Make it realistic with current industry standards. Use Indian companies and locations.
            """
            
            response = self.model.generate_content(f"{system_prompt}\n\nSpecific request: {prompt}")
            
            # Clean and parse JSON response
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            job_data = json.loads(content)
            
            # Add expiration date (30 days from now)
            job_data["expiration_date"] = (datetime.utcnow() + timedelta(days=30)).isoformat()
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error generating job content: {str(e)}")
            # Return fallback data
            return {
                "title": "Software Developer",
                "company": "Tech Solutions Ltd",
                "description": "We are looking for a skilled software developer to join our team.",
                "requirements": ["Bachelor's degree in Computer Science", "2+ years experience"],
                "responsibilities": ["Develop software applications", "Write clean code"],
                "location": "Bangalore, India",
                "salary_min": 600000,
                "salary_max": 1200000,
                "salary_currency": "INR",
                "job_type": "full-time",
                "experience_level": "experienced",
                "skills_required": ["Python", "JavaScript", "React"],
                "benefits": ["Health insurance", "Flexible hours"],
                "tags": ["tech", "software", "development"],
                "expiration_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            }

    async def generate_internship_content(self, prompt: str = None, field: str = "technology") -> Dict[str, Any]:
        """Generate realistic internship content using AI"""
        try:
            if not prompt:
                prompt = f"Generate a realistic {field} internship posting"
            
            system_prompt = f"""
            Generate a realistic and detailed internship posting for a {field} position.
            Return ONLY a valid JSON object with the following structure:
            {{
                "title": "Internship title",
                "company": "Company name",
                "description": "Detailed internship description (2-3 paragraphs)",
                "requirements": ["requirement1", "requirement2", ...],
                "responsibilities": ["responsibility1", "responsibility2", ...],
                "location": "City, Country", 
                "stipend": 15000,
                "duration": "3 months",
                "duration_months": 3,
                "skills_required": ["skill1", "skill2", ...],
                "benefits": ["benefit1", "benefit2", ...],
                "is_remote": false,
                "is_paid": true,
                "tags": ["tag1", "tag2", ...],
                "company_logo": "https://example.com/logo.jpg"
            }}
            
            Make it realistic for students/new graduates. Use Indian companies and locations.
            """
            
            response = self.model.generate_content(f"{system_prompt}\n\nSpecific request: {prompt}")
            
            # Clean and parse JSON response
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            internship_data = json.loads(content)
            
            # Add expiration date (60 days from now)
            internship_data["expiration_date"] = (datetime.utcnow() + timedelta(days=60)).isoformat()
            
            return internship_data
            
        except Exception as e:
            logger.error(f"Error generating internship content: {str(e)}")
            # Return fallback data
            return {
                "title": "Software Development Intern",
                "company": "StartupXYZ",
                "description": "Join our team as a software development intern and gain hands-on experience.",
                "requirements": ["Currently pursuing Computer Science degree", "Basic programming knowledge"],
                "responsibilities": ["Assist in software development", "Learn new technologies"],
                "location": "Mumbai, India",
                "stipend": 20000,
                "duration": "3 months", 
                "duration_months": 3,
                "skills_required": ["Python", "JavaScript", "HTML/CSS"],
                "benefits": ["Mentorship", "Certificate", "Flexible timing"],
                "is_remote": False,
                "is_paid": True,
                "tags": ["internship", "software", "learning"],
                "expiration_date": (datetime.utcnow() + timedelta(days=60)).isoformat()
            }

    async def generate_article_content(self, prompt: str = None, topic: str = "technology") -> Dict[str, Any]:
        """Generate realistic article content using AI"""
        try:
            if not prompt:
                prompt = f"Generate a detailed article about {topic}"
            
            system_prompt = f"""
            Generate a comprehensive and informative article about {topic}.
            Return ONLY a valid JSON object with the following structure:
            {{
                "title": "Article title",
                "slug": "article-slug",
                "excerpt": "Brief article summary (1-2 sentences)",
                "content": "Full article content in markdown format (800-1200 words)",
                "author": "Author Name",
                "category": "Category name",
                "tags": ["tag1", "tag2", ...],
                "reading_time_minutes": 5,
                "seo_meta_title": "SEO optimized title",
                "seo_meta_description": "SEO meta description",
                "featured_image": "https://example.com/image.jpg"
            }}
            
            Make the content engaging, informative, and well-structured with proper headings.
            """
            
            response = self.model.generate_content(f"{system_prompt}\n\nSpecific request: {prompt}")
            
            # Clean and parse JSON response
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            article_data = json.loads(content)
            
            # Add expiration date (90 days from now for articles)
            article_data["expiration_date"] = (datetime.utcnow() + timedelta(days=90)).isoformat()
            
            return article_data
            
        except Exception as e:
            logger.error(f"Error generating article content: {str(e)}")
            # Return fallback data
            return {
                "title": "Introduction to Modern Technology",
                "slug": "introduction-to-modern-technology",
                "excerpt": "Explore the latest trends in technology and their impact on society.",
                "content": "# Introduction to Modern Technology\n\nTechnology continues to evolve at an unprecedented pace...",
                "author": "Tech Writer",
                "category": "Technology",
                "tags": ["technology", "innovation", "trends"],
                "reading_time_minutes": 6,
                "seo_meta_title": "Introduction to Modern Technology - Latest Trends",
                "seo_meta_description": "Discover the latest technology trends and their impact on our daily lives.",
                "expiration_date": (datetime.utcnow() + timedelta(days=90)).isoformat()
            }

    async def generate_roadmap_content(self, prompt: str = None, skill: str = "programming") -> Dict[str, Any]:
        """Generate realistic roadmap content using AI"""
        try:
            if not prompt:
                prompt = f"Generate a learning roadmap for {skill}"
            
            system_prompt = f"""
            Generate a comprehensive learning roadmap for {skill}.
            Return ONLY a valid JSON object with the following structure:
            {{
                "title": "Roadmap title",
                "slug": "roadmap-slug", 
                "description": "Detailed roadmap description (2-3 paragraphs)",
                "difficulty_level": "beginner",
                "estimated_completion_time": "6 months",
                "tags": ["tag1", "tag2", ...],
                "prerequisites": ["prerequisite1", "prerequisite2", ...],
                "steps": [
                    {{
                        "title": "Step title",
                        "description": "Step description",
                        "resources": ["resource1", "resource2"],
                        "estimated_duration": "2 weeks",
                        "prerequisites": ["prerequisite"],
                        "order": 1
                    }}
                ],
                "featured_image": "https://example.com/roadmap.jpg"
            }}
            
            Include 8-12 progressive steps with realistic timelines and resources.
            """
            
            response = self.model.generate_content(f"{system_prompt}\n\nSpecific request: {prompt}")
            
            # Clean and parse JSON response
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            roadmap_data = json.loads(content)
            
            return roadmap_data
            
        except Exception as e:
            logger.error(f"Error generating roadmap content: {str(e)}")
            # Return fallback data
            return {
                "title": "Full Stack Developer Roadmap",
                "slug": "full-stack-developer-roadmap",
                "description": "A comprehensive guide to becoming a full stack developer.",
                "difficulty_level": "intermediate",
                "estimated_completion_time": "8 months", 
                "tags": ["programming", "web development", "full stack"],
                "prerequisites": ["Basic programming knowledge", "HTML/CSS basics"],
                "steps": [
                    {
                        "title": "Frontend Fundamentals",
                        "description": "Learn HTML, CSS, and JavaScript basics",
                        "resources": ["MDN Web Docs", "freeCodeCamp"],
                        "estimated_duration": "4 weeks",
                        "prerequisites": [],
                        "order": 1
                    }
                ]
            }

    async def generate_dsa_problem(self, prompt: str = None, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate realistic DSA problem using AI"""
        try:
            if not prompt:
                prompt = f"Generate a {difficulty} DSA problem"
            
            system_prompt = f"""
            Generate a realistic Data Structures and Algorithms problem with {difficulty} difficulty.
            Return ONLY a valid JSON object with the following structure:
            {{
                "title": "Problem title",
                "slug": "problem-slug",
                "description": "Detailed problem description with examples", 
                "difficulty": "{difficulty}",
                "category_id": "arrays", 
                "topic_id": "sorting",
                "chapter_id": "basic-sorting",
                "companies": ["Google", "Microsoft", "Amazon"],
                "tags": ["tag1", "tag2", ...],
                "constraints": ["constraint1", "constraint2", ...],
                "examples": [
                    {{
                        "input": "Input example",
                        "output": "Output example",
                        "explanation": "Explanation"
                    }}
                ],
                "test_cases": [
                    {{
                        "input": "test input",
                        "expected_output": "expected output",
                        "explanation": "test explanation"
                    }}
                ],
                "hints": ["hint1", "hint2", ...],
                "solution_approach": "High-level solution approach",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(1)"
            }}
            
            Make it a realistic coding interview question with proper examples and test cases.
            """
            
            response = self.model.generate_content(f"{system_prompt}\n\nSpecific request: {prompt}")
            
            # Clean and parse JSON response
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            problem_data = json.loads(content)
            
            return problem_data
            
        except Exception as e:
            logger.error(f"Error generating DSA problem: {str(e)}")
            # Return fallback data
            return {
                "title": "Two Sum Problem",
                "slug": "two-sum-problem",
                "description": "Given an array of integers and a target sum, find two numbers that add up to the target.",
                "difficulty": difficulty,
                "category_id": "arrays",
                "topic_id": "hashing",
                "chapter_id": "basic-hashing",
                "companies": ["Google", "Facebook", "Amazon"],
                "tags": ["arrays", "hashing", "easy"],
                "constraints": ["Array length >= 2", "Exactly one solution exists"],
                "examples": [
                    {
                        "input": "nums = [2,7,11,15], target = 9",
                        "output": "[0,1]",
                        "explanation": "nums[0] + nums[1] = 2 + 7 = 9"
                    }
                ],
                "test_cases": [
                    {
                        "input": "[2,7,11,15], 9",
                        "expected_output": "[0,1]",
                        "explanation": "First example test case"
                    }
                ],
                "hints": ["Use a hash map for O(n) solution", "Store indices as values"],
                "solution_approach": "Use hash map to store complements",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)"
            }

    async def generate_company_logo(self, company_name: str) -> Optional[str]:
        """Generate or find a logo for the company using AI/API"""
        try:
            # For demo purposes, return a placeholder logo
            # In production, you might use image generation APIs or logo databases
            placeholder_url = f"https://ui-avatars.com/api/?name={company_name.replace(' ', '+')}&background=random&size=200"
            return placeholder_url
            
        except Exception as e:
            logger.error(f"Error generating company logo: {str(e)}")
            return None

    async def upload_image_to_cloudinary(self, image_url: str, public_id: str = None) -> Optional[str]:
        """Upload an image to Cloudinary and return the URL"""
        try:
            result = uploader.upload(
                image_url,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            return result.get('secure_url')
            
        except Exception as e:
            logger.error(f"Error uploading to Cloudinary: {str(e)}")
            return None

    async def generate_mindmap_content(self, topic: str) -> Dict[str, Any]:
        """Generate mindmap structure for a given topic"""
        try:
            prompt = f"""
            Generate a mindmap structure for the topic: {topic}
            Return ONLY a valid JSON object with the following structure:
            {{
                "central_topic": "Main topic",
                "branches": [
                    {{
                        "name": "Branch name",
                        "subtopics": ["subtopic1", "subtopic2", ...],
                        "color": "#color_code"
                    }}
                ]
            }}
            
            Include 5-8 main branches with 3-5 subtopics each.
            """
            
            response = self.model.generate_content(prompt)
            
            # Clean and parse JSON response
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            mindmap_data = json.loads(content)
            return mindmap_data
            
        except Exception as e:
            logger.error(f"Error generating mindmap: {str(e)}")
            return {
                "central_topic": topic,
                "branches": [
                    {
                        "name": "Fundamentals",
                        "subtopics": ["Basic concepts", "Core principles"],
                        "color": "#FF6B6B"
                    }
                ]
            }

    async def fill_form(self, request: AIFormFillerRequest) -> AIFormFillerResponse:
        """AI-powered form filling with image and logo generation"""
        try:
            form_data = {}
            generated_images = {}
            generated_logos = {}
            
            if request.content_type == "job":
                form_data = await self.generate_job_content(request.user_prompt)
            elif request.content_type == "internship":
                form_data = await self.generate_internship_content(request.user_prompt)
            elif request.content_type == "article":
                form_data = await self.generate_article_content(request.user_prompt)
            elif request.content_type == "roadmap":
                form_data = await self.generate_roadmap_content(request.user_prompt)
            elif request.content_type == "dsa":
                form_data = await self.generate_dsa_problem(request.user_prompt)
            else:
                raise ValueError(f"Unsupported content type: {request.content_type}")

            # Generate images if requested
            if request.generate_images:
                generated_images = await self._generate_content_images(form_data, request.content_type)
            
            # Generate logos if requested
            if request.generate_logos:
                generated_logos = await self._generate_logos(form_data, request.content_type)

            return AIFormFillerResponse(
                form_data=form_data,
                generated_images=generated_images,
                generated_logos=generated_logos,
                confidence_score=0.9,
                suggestions=["Review generated content for accuracy", "Customize as needed"]
            )

        except Exception as e:
            logger.error(f"Form filling error: {str(e)}")
            raise

    async def _generate_content_images(self, form_data: Dict[str, Any], content_type: str) -> Dict[str, str]:
        """Generate relevant images for the content"""
        images = {}
        
        try:
            # Generate featured image
            if content_type == "job":
                images['featured_image'] = await self._search_image(f"{form_data.get('title', 'job')} {form_data.get('company', 'company')}")
                images['company_banner'] = await self._search_image(f"{form_data.get('company', 'company')} office workplace")
            
            elif content_type == "internship":
                images['featured_image'] = await self._search_image(f"internship {form_data.get('title', 'intern')} learning")
                images['company_image'] = await self._search_image(f"{form_data.get('company', 'company')} office")
            
            elif content_type == "article":
                images['featured_image'] = await self._search_image(f"{form_data.get('category', 'technology')} {form_data.get('title', 'article')}")
                images['header_image'] = await self._search_image(f"tech professional {form_data.get('category', 'technology')}")
            
            elif content_type == "roadmap":
                images['featured_image'] = await self._search_image(f"learning path {form_data.get('title', 'roadmap')}")
                images['progress_image'] = await self._search_image("learning progress development")
            
            elif content_type == "dsa":
                images['featured_image'] = await self._search_image(f"algorithm {form_data.get('category_id', 'programming')} coding")
                images['concept_image'] = await self._search_image(f"data structure {form_data.get('category_id', 'algorithm')}")
        
        except Exception as e:
            logger.error(f"Image generation error: {str(e)}")
            # Fallback to placeholder images
            images['featured_image'] = f"https://via.placeholder.com/800x400/0066cc/ffffff?text={content_type.title()}"
        
        return images

    async def _generate_logos(self, form_data: Dict[str, Any], content_type: str) -> Dict[str, str]:
        """Generate company logos and icons"""
        logos = {}
        
        try:
            if content_type in ["job", "internship"]:
                company_name = form_data.get('company', 'Company')
                # Generate company logo using UI Avatars
                logos['company_logo'] = f"https://ui-avatars.com/api/?name={company_name.replace(' ', '+')}&background=random&size=200&format=png"
                
                # Generate industry icon
                industry_keywords = self._extract_industry_keywords(form_data.get('title', ''))
                logos['industry_icon'] = await self._search_icon(industry_keywords)
            
            elif content_type == "article":
                category = form_data.get('category', 'technology')
                logos['category_icon'] = await self._search_icon(category)
                logos['author_avatar'] = f"https://ui-avatars.com/api/?name={form_data.get('author', 'Author')}&background=4285f4&color=fff&size=100"
            
            elif content_type == "roadmap":
                skill = form_data.get('title', 'skill')
                logos['skill_icon'] = await self._search_icon(skill)
                logos['difficulty_badge'] = self._generate_difficulty_badge(form_data.get('difficulty_level', 'intermediate'))
            
            elif content_type == "dsa":
                category = form_data.get('category_id', 'algorithm')
                logos['category_icon'] = await self._search_icon(f"{category} programming")
                logos['difficulty_badge'] = self._generate_difficulty_badge(form_data.get('difficulty', 'medium'))
        
        except Exception as e:
            logger.error(f"Logo generation error: {str(e)}")
        
        return logos

    async def _search_image(self, query: str) -> str:
        """Search for relevant images using external APIs"""
        try:
            # For now, return a placeholder image
            # In production, integrate with Unsplash, Pexels, etc.
            return f"https://via.placeholder.com/800x400/0066cc/ffffff?text={query.replace(' ', '+')}"
            
        except Exception as e:
            logger.error(f"Image search error: {str(e)}")
            return f"https://via.placeholder.com/800x400/0066cc/ffffff?text={query.replace(' ', '+')}"

    async def _search_icon(self, query: str) -> str:
        """Generate or search for relevant icons"""
        # For now, return a placeholder icon
        # In production, you could integrate with icon APIs like Flaticon, Icons8, etc.
        return f"https://via.placeholder.com/64x64/4285f4/ffffff?text={query[0].upper()}"

    def _generate_difficulty_badge(self, difficulty: str) -> str:
        """Generate difficulty badge image"""
        colors = {
            'easy': '28a745',
            'beginner': '28a745',
            'medium': 'ffc107',
            'intermediate': 'ffc107',
            'hard': 'dc3545',
            'advanced': 'dc3545'
        }
        color = colors.get(difficulty.lower(), 'ffc107')
        return f"https://via.placeholder.com/100x30/{color}/ffffff?text={difficulty.title()}"

    def _extract_industry_keywords(self, title: str) -> str:
        """Extract industry keywords from job title"""
        tech_keywords = ['software', 'developer', 'engineer', 'programmer', 'data', 'ai', 'ml', 'web', 'mobile', 'devops']
        title_lower = title.lower()
        
        for keyword in tech_keywords:
            if keyword in title_lower:
                return keyword
        
        return 'technology'

# Global instance
ai_agent = AIAgentService()