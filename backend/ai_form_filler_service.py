import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import google.generativeai as genai
import requests
import cloudinary
from cloudinary import uploader
from models import (
    JobCreate, InternshipCreate, ArticleCreate, 
    RoadmapCreate, DSAProblemCreate, DSADifficulty,
    AIFormFillerRequest, AIFormFillerResponse, 
    ImageGenerationRequest, ImageGenerationResponse
)

logger = logging.getLogger(__name__)

class AIFormFillerService:
    def __init__(self):
        """Initialize the AI Form Filler Service with required configurations"""
        self.model = genai.GenerativeModel('gemini-pro')
        self.image_apis = {
            'unsplash': os.environ.get('UNSPLASH_ACCESS_KEY'),
            'pexels': os.environ.get('PEXELS_API_KEY')
        }
        
        # Configure Cloudinary if available
        if all([
            os.environ.get('REACT_APP_CLOUDINARY_CLOUD_NAME'),
            os.environ.get('CLOUDINARY_API_KEY'),
            os.environ.get('CLOUDINARY_API_SECRET')
        ]):
            cloudinary.config(
                cloud_name=os.environ.get('REACT_APP_CLOUDINARY_CLOUD_NAME'),
                api_key=os.environ.get('CLOUDINARY_API_KEY'),
                api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
                secure=True
            )
    
    async def fill_form(self, request: AIFormFillerRequest) -> AIFormFillerResponse:
        """
        Fill a form based on the content type and user prompt
        
        Args:
            request: AIFormFillerRequest containing content type and user prompt
            
        Returns:
            AIFormFillerResponse with filled form data and generated assets
        """
        try:
            # Route to the appropriate form filler based on content type
            content_type = request.content_type.lower()
            
            if content_type == "job":
                form_data = await self._generate_job_form(request)
            elif content_type == "internship":
                form_data = await self._generate_internship_form(request)
            elif content_type == "article":
                form_data = await self._generate_article_form(request)
            elif content_type == "roadmap":
                form_data = await self._generate_roadmap_form(request)
            elif content_type == "dsa":
                form_data = await self._generate_dsa_form(request)
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            # Generate images if requested
            generated_images = {}
            if request.generate_images:
                generated_images = await self._generate_content_images(form_data, content_type)
            
            # Generate logos if requested and applicable
            generated_logos = {}
            if request.generate_logos and content_type in ["job", "internship"]:
                generated_logos = await self._generate_company_logos(form_data)
            
            return AIFormFillerResponse(
                form_data=form_data.dict(),
                generated_images=generated_images,
                generated_logos=generated_logos,
                confidence_score=0.95,  # Placeholder confidence score
                suggestions=self._generate_suggestions(form_data, content_type)
            )
            
        except Exception as e:
            logger.error(f"Error in fill_form: {str(e)}")
            raise
    
    async def _generate_job_form(self, request: AIFormFillerRequest) -> JobCreate:
        """Generate job form data based on user prompt"""
        system_prompt = """
        You are an expert job description writer. Generate a comprehensive job posting 
        based on the user's description. Return ONLY a valid JSON object with the 
        following structure:
        {
            "title": "Job Title",
            "company": "Company Name",
            "description": "Detailed job description...",
            "requirements": ["req1", "req2", ...],
            "responsibilities": ["resp1", "resp2", ...],
            "location": "Job Location",
            "salary_min": 50000,
            "salary_max": 80000,
            "job_type": "full-time",
            "experience_level": "mid-level",
            "skills_required": ["skill1", "skill2", ...],
            "benefits": ["benefit1", "benefit2", ...]
        }
        """
        response = self.model.generate_content(f"{system_prompt}\n\nUser Request: {request.user_prompt}")
        job_data = json.loads(response.text)
        return JobCreate(**job_data)
    
    async def _generate_internship_form(self, request: AIFormFillerRequest) -> InternshipCreate:
        """Generate internship form data based on user prompt"""
        system_prompt = """
        You are an expert at creating internship descriptions. Generate a comprehensive 
        internship posting based on the user's description. Return ONLY a valid JSON object 
        with the following structure:
        {
            "title": "Internship Title",
            "company": "Company Name",
            "description": "Detailed internship description...",
            "requirements": ["req1", "req2", ...],
            "responsibilities": ["resp1", "resp2", ...],
            "location": "Internship Location",
            "stipend": 2000,
            "duration": "3-6 months",
            "skills_required": ["skill1", "skill2", ...]
        }
        """
        response = self.model.generate_content(f"{system_prompt}\n\nUser Request: {request.user_prompt}")
        internship_data = json.loads(response.text)
        return InternshipCreate(**internship_data)
    
    async def _generate_article_form(self, request: AIFormFillerRequest) -> ArticleCreate:
        """Generate article form data based on user prompt"""
        system_prompt = """
        You are an expert content creator. Generate a comprehensive article outline 
        based on the user's description. Return ONLY a valid JSON object with the 
        following structure:
        {
            "title": "Article Title",
            "slug": "article-title-slug",
            "excerpt": "Brief article excerpt...",
            "content": "Full article content...",
            "author": "Author Name",
            "category": "Technology",
            "tags": ["tag1", "tag2", ...]
        }
        """
        response = self.model.generate_content(f"{system_prompt}\n\nUser Request: {request.user_prompt}")
        article_data = json.loads(response.text)
        return ArticleCreate(**article_data)
    
    async def _generate_roadmap_form(self, request: AIFormFillerRequest) -> RoadmapCreate:
        """Generate roadmap form data based on user prompt"""
        system_prompt = """
        You are an expert at creating learning roadmaps. Generate a comprehensive 
        learning roadmap based on the user's description. Return ONLY a valid JSON object 
        with the following structure:
        {
            "title": "Roadmap Title",
            "slug": "roadmap-title-slug",
            "description": "Detailed roadmap description...",
            "difficulty_level": "beginner | intermediate | advanced",
            "estimated_completion_time": "3 months",
            "tags": ["tag1", "tag2", ...],
            "steps": [
                {
                    "title": "Step 1",
                    "description": "Step description...",
                    "resources": ["resource1", "resource2", ...],
                    "estimated_duration": "2 weeks",
                    "prerequisites": [],
                    "order": 1
                },
                ...
            ]
        }
        """
        response = self.model.generate_content(f"{system_prompt}\n\nUser Request: {request.user_prompt}")
        roadmap_data = json.loads(response.text)
        return RoadmapCreate(**roadmap_data)
    
    async def _generate_dsa_form(self, request: AIFormFillerRequest) -> DSAProblemCreate:
        """Generate DSA problem form data based on user prompt"""
        system_prompt = """
        You are an expert at creating Data Structures and Algorithms problems. 
        Generate a comprehensive DSA problem based on the user's description. 
        Return ONLY a valid JSON object with the following structure:
        {
            "title": "Problem Title",
            "slug": "problem-title-slug",
            "description": "Detailed problem description...",
            "difficulty": "easy | medium | hard",
            "category_id": "category-id",
            "topic_id": "topic-id",
            "chapter_id": "chapter-id",
            "companies": ["company1", "company2", ...],
            "tags": ["tag1", "tag2", ...],
            "constraints": ["constraint1", "constraint2", ...],
            "examples": [
                {"input": "input1", "output": "output1", "explanation": "explanation1"},
                ...
            ],
            "test_cases": [
                {"input": "input1", "expected_output": "output1"},
                ...
            ],
            "hints": ["hint1", "hint2", ...],
            "solution_approach": "Detailed solution approach...",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)"
        }
        """
        response = self.model.generate_content(f"{system_prompt}\n\nUser Request: {request.user_prompt}")
        dsa_data = json.loads(response.text)
        return DSAProblemCreate(**dsa_data)
    
    async def _generate_content_images(self, form_data: Any, content_type: str) -> Dict[str, str]:
        """Generate relevant images for the content"""
        images = {}
        
        try:
            if content_type in ["job", "internship"]:
                # Generate company/office image
                prompt = f"Professional {content_type} image for {getattr(form_data, 'company', 'a company')}"
                images["featured_image"] = await self._generate_image(prompt)
                
            elif content_type == "article":
                # Generate article featured image
                prompt = f"Featured image for article: {getattr(form_data, 'title', '')}"
                images["featured_image"] = await self._generate_image(prompt)
                
            elif content_type == "roadmap":
                # Generate roadmap cover image
                prompt = f"Cover image for learning roadmap: {getattr(form_data, 'title', '')}"
                images["cover_image"] = await self._generate_image(prompt)
                
            elif content_type == "dsa":
                # Generate DSA problem visualization
                prompt = f"Visualization for DSA problem: {getattr(form_data, 'title', '')}"
                images["visualization"] = await self._generate_image(prompt)
                
        except Exception as e:
            logger.error(f"Error generating content images: {str(e)}")
        
        return images
    
    async def _generate_company_logos(self, form_data: Any) -> Dict[str, str]:
        """Generate company logos"""
        logos = {}
        
        try:
            if hasattr(form_data, 'company'):
                prompt = f"Professional logo for {form_data.company}"
                logos["company_logo"] = await self._generate_logo(prompt)
                
        except Exception as e:
            logger.error(f"Error generating company logo: {str(e)}")
        
        return logos
    
    async def _generate_image(self, prompt: str) -> str:
        """Generate an image using the configured image generation API"""
        # Try to use Cloudinary first if configured
        try:
            if 'cloudinary' in globals():
                response = cloudinary.uploader.upload(
                    f"text:{prompt}",
                    folder="ai_generated",
                    transformation=[
                        {"width": 1200, "height": 630, "crop": "fill", "background": "auto:predominant"},
                        {"overlay": "text:Montserrat_72_bold", 
                         "color": "#ffffff", 
                         "text": prompt[:100],
                         "width": 1000,
                         "crop": "fit",
                         "gravity": "center",
                         "y": 0
                        }
                    ]
                )
                return response.get('secure_url', '')
        except Exception as e:
            logger.warning(f"Cloudinary image generation failed: {str(e)}")
        
        # Fallback to placeholder service
        return f"https://via.placeholder.com/1200x630/0066cc/ffffff?text={prompt.replace(' ', '+')}"
    
    async def _generate_logo(self, prompt: str) -> str:
        """Generate a logo using the configured logo generation API"""
        # Try to use Cloudinary first if configured
        try:
            if 'cloudinary' in globals():
                response = cloudinary.uploader.upload(
                    f"text:{prompt}",
                    folder="logos",
                    transformation=[
                        {"width": 400, "height": 400, "crop": "fill", "background": "auto:predominant"}
                    ]
                )
                return response.get('secure_url', '')
        except Exception as e:
            logger.warning(f"Cloudinary logo generation failed: {str(e)}")
        
        # Fallback to placeholder service
        return f"https://via.placeholder.com/400/0066cc/ffffff?text={prompt[:2].upper()}"
    
    def _generate_suggestions(self, form_data: Any, content_type: str) -> List[str]:
        """Generate suggestions for improving the form data"""
        suggestions = []
        
        # Common suggestions
        if hasattr(form_data, 'description') and len(getattr(form_data, 'description', '')) < 100:
            suggestions.append("Consider expanding the description with more details.")
            
        if hasattr(form_data, 'requirements') and len(getattr(form_data, 'requirements', [])) < 3:
            suggestions.append("Add more requirements to make the listing more specific.")
        
        # Content type specific suggestions
        if content_type == "job" or content_type == "internship":
            if not hasattr(form_data, 'location') or not getattr(form_data, 'location'):
                suggestions.append("Add a specific location or mention if remote work is available.")
                
        elif content_type == "article":
            if not hasattr(form_data, 'tags') or len(getattr(form_data, 'tags', [])) < 2:
                suggestions.append("Add more relevant tags to improve discoverability.")
                
        elif content_type == "roadmap":
            if hasattr(form_data, 'steps') and len(getattr(form_data, 'steps', [])) < 5:
                suggestions.append("Consider adding more steps to create a more comprehensive learning path.")
                
        elif content_type == "dsa":
            if not hasattr(form_data, 'examples') or len(getattr(form_data, 'examples', [])) < 2:
                suggestions.append("Add more examples to help users understand the problem better.")
        
        return suggestions

# Global instance
ai_form_filler = AIFormFillerService()
