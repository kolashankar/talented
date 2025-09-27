import asyncio
import json
from typing import Dict, Any, Optional
from datetime import datetime
from emergentintegrations.llm.chat import LlmChat, UserMessage
from models import (
    AIContentRequest, AIContentResponse, ResumeAnalysisRequest, ResumeAnalysisResponse,
    ResumeParseRequest, ResumeParseResponse, PortfolioGenerateRequest, Portfolio,
    ParsedResumeData, PersonalDetails, Education, Experience, Project
)
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def _get_chat_instance(self, system_message: str, session_id: str = None) -> LlmChat:
        """Initialize LLM chat instance"""
        if not session_id:
            session_id = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        ).with_model("gemini", "gemini-2.0-flash")
        
        return chat
    
    async def generate_job_content(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate job posting content using AI"""
        system_message = """
You are an expert HR professional and job posting writer. Generate comprehensive job postings with the following structure:

- Title: Professional and attractive job title
- Company: If not specified, generate a realistic tech company name
- Description: Detailed job description (200-400 words)
- Requirements: List of required qualifications and skills (5-10 items)
- Responsibilities: List of key job responsibilities (5-8 items) 
- Location: Professional location format
- Salary range: Realistic salary range in INR for Indian market
- Skills: Technical and soft skills required (5-10 skills)
- Benefits: Company benefits and perks (3-6 items)
- Tags: Relevant job tags for categorization

Return your response as a valid JSON object only, no additional text.
"""
        
        try:
            chat = self._get_chat_instance(system_message)
            
            full_prompt = f"""
Generate a job posting based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, company, description, requirements, responsibilities, location, salary_min, salary_max, skills_required, benefits, tags, job_type, experience_level
"""
            
            user_message = UserMessage(text=full_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            content = json.loads(response)
            
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
- Requirements: List of required qualifications (3-8 items)
- Responsibilities: List of key internship responsibilities (4-7 items)
- Location: Professional location format
- Stipend: Realistic monthly stipend in INR for Indian market
- Duration: Duration in months
- Skills: Technical and soft skills required (4-8 skills)
- Benefits: Internship benefits and learning opportunities (3-5 items)
- Tags: Relevant internship tags for categorization

Return your response as a valid JSON object only, no additional text.
"""
        
        try:
            chat = self._get_chat_instance(system_message)
            
            full_prompt = f"""
Generate an internship posting based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, company, description, requirements, responsibilities, location, stipend, duration_months, skills_required, benefits, tags
"""
            
            user_message = UserMessage(text=full_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            content = json.loads(response)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating internship content: {str(e)}")
            raise Exception(f"Failed to generate internship content: {str(e)}")
    
    async def generate_article_content(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate article content using AI"""
        system_message = """
You are an expert tech content writer and career advisor. Generate comprehensive articles for tech freshers with the following structure:

- Title: Engaging and SEO-friendly title
- Slug: URL-friendly slug
- Excerpt: Compelling article summary (100-150 words)
- Content: Full article content in markdown format (800-1500 words)
- Category: Appropriate category (Fresher Guide, Career Tips, Tech Skills, etc.)
- Tags: Relevant tags for categorization (5-8 tags)
- Reading time: Estimated reading time in minutes
- SEO meta title: Optimized meta title
- SEO meta description: Optimized meta description

Write engaging, informative, and actionable content that helps tech freshers in their career journey.

Return your response as a valid JSON object only, no additional text.
"""
        
        try:
            chat = self._get_chat_instance(system_message)
            
            full_prompt = f"""
Generate an article based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, slug, excerpt, content, category, tags, reading_time_minutes, seo_meta_title, seo_meta_description
"""
            
            user_message = UserMessage(text=full_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            content = json.loads(response)
            
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
- Estimated completion time: Realistic time estimate
- Prerequisites: List of prerequisites (if any)
- Steps: Detailed learning steps with:
  - Title: Step title
  - Description: Step description (100-200 words)
  - Resources: List of learning resources (links, books, courses)
  - Estimated duration: Time needed for this step
  - Prerequisites: Prerequisites for this specific step
  - Order: Sequential order number
- Tags: Relevant tags for categorization

Create practical, actionable roadmaps that guide learners step-by-step.

Return your response as a valid JSON object only, no additional text.
"""
        
        try:
            chat = self._get_chat_instance(system_message)
            
            full_prompt = f"""
Generate a learning roadmap based on: {prompt}

{f"Additional context: {json.dumps(context)}" if context else ""}

Return as JSON with keys: title, slug, description, difficulty_level, estimated_completion_time, prerequisites, steps, tags
Steps should be an array of objects with keys: title, description, resources, estimated_duration, prerequisites, order
"""
            
            user_message = UserMessage(text=full_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            content = json.loads(response)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating roadmap content: {str(e)}")
            raise Exception(f"Failed to generate roadmap content: {str(e)}")
    
    async def analyze_resume(self, request: ResumeAnalysisRequest) -> ResumeAnalysisResponse:
        """Analyze resume and provide ATS feedback"""
        system_message = """
You are an expert ATS (Applicant Tracking System) analyzer and career counselor. Analyze resumes and provide comprehensive feedback including:

- Overall Score: Score out of 100 based on ATS compatibility and content quality
- Strengths: List of strong points in the resume (3-8 points)
- Weaknesses: List of areas for improvement (3-8 points)
- Suggestions: Specific actionable suggestions (5-10 points)
- Keyword Match Score: Score out of 100 for keyword optimization
- Skills Analysis: Analysis of technical and soft skills
- Experience Analysis: Analysis of work experience and projects
- Education Analysis: Analysis of educational background
- Formatting Score: Score out of 100 for ATS-friendly formatting
- Recommendations: Priority recommendations for improvement

Provide constructive, actionable feedback that helps candidates improve their resumes for better ATS performance.

Return your response as a valid JSON object only, no additional text.
"""
        
        try:
            chat = self._get_chat_instance(system_message)
            
            full_prompt = f"""
Analyze this resume:

Resume Content:
{request.resume_text}

{f"Job Description: {request.job_description}" if request.job_description else ""}
{f"Target Role: {request.target_role}" if request.target_role else ""}

Provide comprehensive ATS analysis as JSON with keys:
- overall_score (float 0-100)
- strengths (array of strings)
- weaknesses (array of strings) 
- suggestions (array of strings)
- keyword_match_score (float 0-100)
- skills_analysis (object with technical_skills, soft_skills, missing_skills)
- experience_analysis (object with years_experience, project_quality, achievements)
- education_analysis (object with degree_relevance, certifications, additional_courses)
- formatting_score (float 0-100)
- recommendations (array of priority recommendations)
"""
            
            user_message = UserMessage(text=full_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            analysis_data = json.loads(response)
            
            # Create ResumeAnalysisResponse object
            analysis_response = ResumeAnalysisResponse(**analysis_data)
            
            return analysis_response
            
        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            raise Exception(f"Failed to analyze resume: {str(e)}")
    
    async def generate_content(self, request: AIContentRequest) -> AIContentResponse:
        """Generate content based on content type"""
        try:
            if request.content_type == "job":
                content = await self.generate_job_content(request.prompt, request.additional_context)
            elif request.content_type == "internship":
                content = await self.generate_internship_content(request.prompt, request.additional_context)
            elif request.content_type == "article":
                content = await self.generate_article_content(request.prompt, request.additional_context)
            elif request.content_type == "roadmap":
                content = await self.generate_roadmap_content(request.prompt, request.additional_context)
            else:
                raise ValueError(f"Unsupported content type: {request.content_type}")
            
            response = AIContentResponse(
                content=content,
                tokens_used=None  # We can add token counting later if needed
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in generate_content: {str(e)}")
            raise

# Global AI service instance
ai_service = AIService()