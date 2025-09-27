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

    async def parse_resume(self, request: ResumeParseRequest) -> ResumeParseResponse:
        """Parse resume text into structured data"""
        system_message = """
You are an expert resume parser. Parse resume text into structured JSON data with the following format:

{
  "personal_details": {
    "full_name": "string",
    "email": "string",
    "phone": "string (optional)",
    "location": "string (optional)",
    "linkedin": "string (optional)",
    "github": "string (optional)",
    "portfolio_url": "string (optional)",
    "bio": "string (optional)",
    "profile_image": null
  },
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "year": "string (optional)",
      "cgpa": "string (optional)",
      "description": "string (optional)"
    }
  ],
  "experience": [
    {
      "title": "string",
      "company": "string",
      "duration": "string",
      "location": "string (optional)",
      "description": ["array of strings"]
    }
  ],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "technologies": ["array of strings"],
      "github_url": "string (optional)",
      "live_url": "string (optional)",
      "image": null
    }
  ],
  "skills": ["array of strings"],
  "certifications": ["array of strings"],
  "achievements": ["array of strings"],
  "parsing_confidence": 0.95,
  "suggestions": ["array of improvement suggestions"],
  "missing_sections": ["array of missing sections"]
}

Extract all available information accurately. If information is missing, use empty arrays/null values appropriately.
Ensure the parsing_confidence is a realistic score between 0 and 1.
Return valid JSON only, no additional text.
"""
        
        try:
            chat = self._get_chat_instance(system_message)
            
            full_prompt = f"""
Parse this resume text into structured JSON:

{request.resume_text}

Return the parsed data as JSON matching the specified format exactly.
"""
            
            user_message = UserMessage(text=full_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            parsed_data = json.loads(response)
            
            # Extract the main data and metadata
            parsed_resume = ParsedResumeData(
                personal_details=PersonalDetails(**parsed_data["personal_details"]),
                education=[Education(**edu) for edu in parsed_data.get("education", [])],
                experience=[Experience(**exp) for exp in parsed_data.get("experience", [])],
                projects=[Project(**proj) for proj in parsed_data.get("projects", [])],
                skills=parsed_data.get("skills", []),
                certifications=parsed_data.get("certifications", []),
                achievements=parsed_data.get("achievements", [])
            )
            
            response_obj = ResumeParseResponse(
                parsed_data=parsed_resume,
                parsing_confidence=parsed_data.get("parsing_confidence", 0.8),
                suggestions=parsed_data.get("suggestions", []),
                missing_sections=parsed_data.get("missing_sections", [])
            )
            
            return response_obj
            
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise Exception(f"Failed to parse resume: {str(e)}")
    
    async def generate_portfolio(self, request: PortfolioGenerateRequest) -> dict:
        """Generate portfolio website content"""
        system_message = """
You are an expert web developer and designer. Generate complete portfolio website content including HTML, CSS, and structured data based on the provided template and resume data.

Create a professional, responsive, and visually appealing portfolio that showcases the person's skills and experience effectively.

Return your response as a JSON object with these keys:
- content: Structured content data
- html: Complete HTML content
- css: Complete CSS styles
- javascript: Any required JavaScript (optional)

Make sure the website is:
1. Fully responsive (mobile, tablet, desktop)
2. Modern and professional
3. Optimized for performance
4. Accessible
5. SEO-friendly

Use the provided template theme and colors. Include all relevant sections based on the available data.
"""
        
        try:
            chat = self._get_chat_instance(system_message)
            
            # Prepare the data for the prompt
            resume_data = request.resume_data
            template_info = f"Template ID: {request.template_id}"
            
            full_prompt = f"""
Generate a complete portfolio website based on:

Template: {template_info}
User Prompt: {request.user_prompt}

Resume Data:
Personal: {resume_data.personal_details.dict()}
Education: {[edu.dict() for edu in resume_data.education]}
Experience: {[exp.dict() for exp in resume_data.experience]}
Projects: {[proj.dict() for proj in resume_data.projects]}
Skills: {resume_data.skills}
Certifications: {resume_data.certifications}
Achievements: {resume_data.achievements}

Additional Preferences: {request.additional_preferences}

Generate a complete, modern, responsive portfolio website with proper HTML structure, CSS styling, and content organization.
Return as JSON with content, html, css keys.
"""
            
            user_message = UserMessage(text=full_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            portfolio_content = json.loads(response)
            
            return portfolio_content
            
        except Exception as e:
            logger.error(f"Error generating portfolio: {str(e)}")
            raise Exception(f"Failed to generate portfolio: {str(e)}")
    
    async def render_portfolio_html(self, portfolio: Portfolio) -> str:
        """Render portfolio as HTML for viewing"""
        try:
            # This would typically render based on the stored portfolio data
            # For now, return a simple HTML structure
            personal = portfolio.resume_data.personal_details
            
            html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal.full_name} - Portfolio</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: #f8fafc;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            color: #2d3748;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .skill-tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            margin: 5px;
            font-size: 14px;
        }}
        .project {{
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{personal.full_name}</h1>
            <p>{personal.bio or 'Professional Portfolio'}</p>
            <p>{personal.email} | {personal.phone or ''} | {personal.location or ''}</p>
        </div>
        <div class="content">
            <div class="section">
                <h2>Skills</h2>
                {"".join([f'<span class="skill-tag">{skill}</span>' for skill in portfolio.resume_data.skills])}
            </div>
            
            <div class="section">
                <h2>Experience</h2>
                {"".join([f'<div class="project"><h3>{exp.title} at {exp.company}</h3><p>{exp.duration}</p><ul>{"".join([f"<li>{desc}</li>" for desc in exp.description])}</ul></div>' for exp in portfolio.resume_data.experience])}
            </div>
            
            <div class="section">
                <h2>Projects</h2>
                {"".join([f'<div class="project"><h3>{proj.name}</h3><p>{proj.description}</p><p><strong>Technologies:</strong> {", ".join(proj.technologies)}</p></div>' for proj in portfolio.resume_data.projects])}
            </div>
            
            <div class="section">
                <h2>Education</h2>
                {"".join([f'<div class="project"><h3>{edu.degree}</h3><p>{edu.institution} {f"({edu.year})" if edu.year else ""}</p></div>' for edu in portfolio.resume_data.education])}
            </div>
        </div>
    </div>
</body>
</html>
"""
            return html
            
        except Exception as e:
            logger.error(f"Error rendering portfolio HTML: {str(e)}")
            return "<h1>Error rendering portfolio</h1>"

# Global AI service instance
ai_service = AIService()