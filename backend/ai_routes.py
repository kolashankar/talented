from fastapi import APIRouter, HTTPException, Depends
from models import (
    AIContentRequest, AIContentResponse, 
    ResumeAnalysisRequest, ResumeAnalysisResponse,
    JobCreate, InternshipCreate, ArticleCreate, RoadmapCreate
)
from ai_service import ai_service
from auth import get_current_active_admin, AdminUser
import logging

logger = logging.getLogger(__name__)

# Create router for AI routes
ai_router = APIRouter(prefix="/ai", tags=["ai"])

@ai_router.post("/generate-content", response_model=AIContentResponse)
async def generate_content(
    request: AIContentRequest, 
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate content using AI based on content type and prompt"""
    try:
        response = await ai_service.generate_content(request)
        return response
    except Exception as e:
        logger.error(f"Error in generate_content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {str(e)}")

@ai_router.post("/generate-job")
async def generate_job_content(
    prompt: str,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate job posting content using AI"""
    try:
        content = await ai_service.generate_job_content(prompt)
        return {
            "content": content,
            "message": "Job content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating job content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate job content: {str(e)}")

@ai_router.post("/generate-internship")
async def generate_internship_content(
    prompt: str,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate internship posting content using AI"""
    try:
        content = await ai_service.generate_internship_content(prompt)
        return {
            "content": content,
            "message": "Internship content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating internship content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate internship content: {str(e)}")

@ai_router.post("/generate-article")
async def generate_article_content(
    prompt: str,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate article content using AI"""
    try:
        content = await ai_service.generate_article_content(prompt)
        return {
            "content": content,
            "message": "Article content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating article content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate article content: {str(e)}")

@ai_router.post("/generate-roadmap")
async def generate_roadmap_content(
    prompt: str,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate roadmap content using AI"""
    try:
        content = await ai_service.generate_roadmap_content(prompt)
        return {
            "content": content,
            "message": "Roadmap content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating roadmap content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate roadmap content: {str(e)}")

# Resume ATS Analysis Routes (Public - for user app)
public_ai_router = APIRouter(prefix="/public-ai", tags=["public-ai"])

@public_ai_router.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest):
    """Analyze resume using AI ATS system (public endpoint for user app)"""
    try:
        analysis = await ai_service.analyze_resume(request)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze resume: {str(e)}")