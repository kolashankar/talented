import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import google.generativeai as genai
import requests
import uuid
from models import (
    JobCreate, InternshipCreate, ArticleCreate, 
    RoadmapCreate, DSAProblemCreate, DSADifficulty
)

logger = logging.getLogger(__name__)

# Initialize Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    logger.warning("GEMINI_API_KEY not found. AI features will be disabled.")

class AIService:
    def __init__(self):
        self.model = model

    async def _generate_content(self, system_message: str, user_prompt: str) -> str:
        """Generate content using Gemini AI"""
        if not self.model:
            raise Exception("Gemini AI not configured. Please set GEMINI_API_KEY environment variable.")

        full_prompt = f"{system_message}\n\nUser Request: {user_prompt}"
        response = self.model.generate_content(full_prompt)
        return response.text

    def _generate_image_placeholder(self, entity_type: str, title: str) -> str:
        """Generate placeholder image URL"""
        entity_type_clean = entity_type.replace(' ', '+')
        title_clean = title.replace(' ', '+')
        return f"https://via.placeholder.com/400x300/0066cc/ffffff?text={entity_type_clean}:+{title_clean}"

    def _generate_logo_placeholder(self, company_name: str) -> str:
        """Generate company logo placeholder"""
        company_clean = company_name.replace(' ', '+')
        return f"https://ui-avatars.com/api/?name={company_clean}&background=random&size=200&format=png"

    async def generate_job_content(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate job posting content using AI"""
        system_message = """
You are an expert HR professional. Generate comprehensive job postings with the following structure:

- Title: Professional job title
- Company: If not specified, generate a realistic tech company name
- Description: Detailed job description (200-400 words)
- Requirements: List of required qualifications (4-8 items)
- Responsibilities: List of key job responsibilities (4-8 items)
- Location: Professional location format (Indian cities preferred)
- Salary range: Realistic salary range in INR
- Job type: full-time, part-time, contract, or remote
- Experience level: fresher, experienced, or senior
- Skills: Technical skills required (4-10 skills)
- Benefits: Employee benefits (3-6 items)
- Tags: Relevant job tags for categorization
- Application URL: Generate a realistic application URL

Return your response as a valid JSON object only, no additional text.
"""

        try:
            full_prompt = f"""
Generate a job posting based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, company, description, requirements, responsibilities, location, salary_range, job_type, experience_level, skills_required, benefits, tags, application_url
"""

            response_text = await self._generate_content(system_message, full_prompt)

            # Clean the response to extract JSON
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse the JSON response
            content = json.loads(response_text)

            # Add generated images and metadata
            content['company_logo'] = self._generate_logo_placeholder(content.get('company', 'Company'))
            content['featured_image'] = self._generate_image_placeholder('Job', content.get('title', 'Position'))
            content['expiration_date'] = (datetime.utcnow() + timedelta(days=30)).isoformat()
            content['is_active'] = True
            content['is_featured'] = False

            return content

        except Exception as e:
            logger.error(f"Error generating job content: {str(e)}")
            raise Exception(f"Failed to generate job content: {str(e)}")

    async def generate_internship_content(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate internship posting content using AI"""
        system_message = """
You are an expert HR professional specializing in internship programs. Generate comprehensive internship postings with the following structure:

- Title: Professional and attractive internship title
- Company: If not specified, generate a realistic tech company name
- Description: Detailed internship description (150-300 words)
- Requirements: List of required qualifications (3-6 items)
- Responsibilities: List of key internship responsibilities (3-6 items)
- Location: Professional location format (Indian cities preferred)
- Stipend: Realistic monthly stipend in INR (use numbers only)
- Duration: Duration description like "3 months"
- Duration months: Duration in months as number
- Skills: Technical and soft skills required (4-8 skills)
- Benefits: Internship benefits and learning opportunities (3-5 items)
- Tags: Relevant internship tags for categorization
- Application URL: Generate a realistic application URL

Return your response as a valid JSON object only, no additional text.
"""

        try:
            full_prompt = f"""
Generate an internship posting based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, company, description, requirements, responsibilities, location, stipend, duration, duration_months, skills_required, benefits, tags, application_url, is_remote, is_paid
"""

            response_text = await self._generate_content(system_message, full_prompt)

            # Clean the response to extract JSON
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse the JSON response
            content = json.loads(response_text)

            # Add generated images and metadata
            content['company_logo'] = self._generate_logo_placeholder(content.get('company', 'Company'))
            content['featured_image'] = self._generate_image_placeholder('Internship', content.get('title', 'Internship'))
            content['expiration_date'] = (datetime.utcnow() + timedelta(days=60)).isoformat()
            content['is_active'] = True
            content['is_featured'] = False

            # Ensure boolean fields
            content['is_remote'] = content.get('is_remote', False)
            content['is_paid'] = content.get('is_paid', True)

            return content

        except Exception as e:
            logger.error(f"Error generating internship content: {str(e)}")
            raise Exception(f"Failed to generate internship content: {str(e)}")

    async def generate_article_content(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate article content using AI"""
        system_message = """
You are an expert tech content writer and career advisor. Generate comprehensive articles with the following structure:

- Title: Engaging and informative article title
- Slug: URL-friendly slug based on title
- Excerpt: Brief article summary (100-200 words)
- Content: Full article content in markdown format (800-1500 words)
- Author: Professional author name
- Category: Article category (career-advice, technical, interview-tips, industry-news, tutorials)
- Tags: Relevant article tags (4-8 tags)
- Featured image: Will be auto-generated
- SEO meta title: SEO optimized title
- SEO meta description: SEO meta description (150-160 characters)
- Reading time: Estimated reading time in minutes

Create engaging, informative content that provides real value to tech professionals and job seekers.

Return your response as a valid JSON object only, no additional text.
"""

        try:
            full_prompt = f"""
Generate an article based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, slug, excerpt, content, author, category, tags, seo_meta_title, seo_meta_description, reading_time_minutes
"""

            response_text = await self._generate_content(system_message, full_prompt)

            # Clean the response to extract JSON
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse the JSON response
            content = json.loads(response_text)

            # Add generated images and metadata
            content['featured_image'] = self._generate_image_placeholder('Article', content.get('title', 'Article'))
            content['is_published'] = True
            content['is_featured'] = False

            return content

        except Exception as e:
            logger.error(f"Error generating article content: {str(e)}")
            raise Exception(f"Failed to generate article content: {str(e)}")

    async def generate_roadmap_content(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate roadmap content using AI"""
        system_message = """
You are an expert tech educator and career mentor. Generate comprehensive learning roadmaps with the following structure:

- Title: Clear and descriptive roadmap title
- Slug: URL-friendly slug
- Description: Detailed roadmap description (200-400 words)
- Difficulty level: beginner, intermediate, or advanced
- Estimated completion time: Realistic time estimate (e.g., "3 months", "6 weeks")
- Prerequisites: List of prerequisites (if any)
- Steps: Detailed learning steps (6-12 steps) with:
  - Title: Step title
  - Description: Step description (100-200 words)
  - Resources: List of learning resources
  - Estimated duration: Time needed for this step
  - Prerequisites: Prerequisites for this specific step
  - Order: Sequential order number
- Tags: Relevant tags for categorization

Create practical, actionable roadmaps that guide learners step-by-step.

Return your response as a valid JSON object only, no additional text.
"""

        try:
            full_prompt = f"""
Generate a learning roadmap based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, slug, description, difficulty_level, estimated_completion_time, prerequisites, steps, tags
"""

            response_text = await self._generate_content(system_message, full_prompt)

            # Clean the response to extract JSON
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse the JSON response
            content = json.loads(response_text)

            # Add generated images and metadata
            content['featured_image'] = self._generate_image_placeholder('Roadmap', content.get('title', 'Learning Path'))

            return content

        except Exception as e:
            logger.error(f"Error generating roadmap content: {str(e)}")
            raise Exception(f"Failed to generate roadmap content: {str(e)}")

    async def generate_dsa_problem(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate DSA problem using AI"""
        system_message = """
You are an expert computer science educator specializing in Data Structures and Algorithms. Generate comprehensive DSA problems with the following structure:

- Title: Clear problem title
- Slug: URL-friendly slug
- Description: Detailed problem description with clear explanation
- Difficulty: easy, medium, or hard
- Category ID: arrays, strings, trees, graphs, dynamic-programming, etc.
- Topic ID: based on specific topic within category
- Chapter ID: specific chapter or concept
- Companies: List of companies that have asked this question (3-5 companies)
- Tags: Relevant problem tags (3-6 tags)
- Constraints: Problem constraints (2-4 constraints)
- Examples: Input/output examples with explanations (2-3 examples)
- Test cases: Test cases for validation (3-5 test cases)
- Hints: Helpful hints for solving (2-4 hints)
- Solution approach: High-level solution approach
- Time complexity: Big O time complexity
- Space complexity: Big O space complexity

Create realistic coding interview problems that test algorithmic thinking.

Return your response as a valid JSON object only, no additional text.
"""

        try:
            full_prompt = f"""
Generate a DSA problem based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, slug, description, difficulty, category_id, topic_id, chapter_id, companies, tags, constraints, examples, test_cases, hints, solution_approach, time_complexity, space_complexity
"""

            response_text = await self._generate_content(system_message, full_prompt)

            # Clean the response to extract JSON
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse the JSON response
            content = json.loads(response_text)

            return content

        except Exception as e:
            logger.error(f"Error generating DSA problem: {str(e)}")
            raise Exception(f"Failed to generate DSA problem: {str(e)}")

# Global instance
ai_service = AIService()