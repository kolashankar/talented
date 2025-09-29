
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from ai_service import ai_service
from auth import get_current_active_admin, AdminUser
import logging

logger = logging.getLogger(__name__)

# Create router for AI routes
ai_router = APIRouter(prefix="/ai", tags=["ai"])

# Create router for public AI routes (no authentication required)
public_ai_router = APIRouter(prefix="/public-ai", tags=["public-ai"])

@ai_router.post("/generate-job")
async def generate_job_content(
    prompt: str = Query(..., description="Prompt for job generation"),
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate job content using AI"""
    try:
        content = await ai_service.generate_job_content(prompt)
        return {
            "success": True,
            "content": content,
            "message": "Job content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating job content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@ai_router.post("/generate-internship")
async def generate_internship_content(
    prompt: str = Query(..., description="Prompt for internship generation"),
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate internship content using AI"""
    try:
        content = await ai_service.generate_internship_content(prompt)
        return {
            "success": True,
            "content": content,
            "message": "Internship content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating internship content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@ai_router.post("/generate-article")
async def generate_article_content(
    prompt: str = Query(..., description="Prompt for article generation"),
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate article content using AI"""
    try:
        content = await ai_service.generate_article_content(prompt)
        return {
            "success": True,
            "content": content,
            "message": "Article content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating article content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@ai_router.post("/generate-roadmap")
async def generate_roadmap_content(
    prompt: str = Query(..., description="Prompt for roadmap generation"),
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate roadmap content using AI"""
    try:
        content = await ai_service.generate_roadmap_content(prompt)
        return {
            "success": True,
            "content": content,
            "message": "Roadmap content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating roadmap content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@ai_router.post("/generate-dsa-problem")
async def generate_dsa_problem_content(
    prompt: str = Query(..., description="Prompt for DSA problem generation"),
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate DSA problem content using AI"""
    try:
        content = await ai_service.generate_dsa_problem(prompt)
        return {
            "success": True,
            "content": content,
            "message": "DSA problem content generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating DSA problem content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@ai_router.post("/generate-all")
async def generate_multiple_content(
    content_type: str = Query(..., description="Type of content to generate"),
    prompt: str = Query(..., description="Prompt for content generation"),
    count: int = Query(1, ge=1, le=10, description="Number of items to generate"),
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate multiple content items of the same type"""
    try:
        results = []
        for i in range(count):
            if content_type == "job":
                content = await ai_service.generate_job_content(f"{prompt} (variation {i+1})")
            elif content_type == "internship":
                content = await ai_service.generate_internship_content(f"{prompt} (variation {i+1})")
            elif content_type == "article":
                content = await ai_service.generate_article_content(f"{prompt} (variation {i+1})")
            elif content_type == "roadmap":
                content = await ai_service.generate_roadmap_content(f"{prompt} (variation {i+1})")
            elif content_type == "dsa-problem":
                content = await ai_service.generate_dsa_problem(f"{prompt} (variation {i+1})")
            else:
                raise HTTPException(status_code=400, detail="Invalid content type")
            
            results.append(content)
        
        return {
            "success": True,
            "content": results,
            "message": f"Generated {count} {content_type} items successfully"
        }
    except Exception as e:
        logger.error(f"Error generating multiple content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@public_ai_router.post("/analyze-resume")
async def analyze_resume_public(request: Dict[str, Any]):
    """Analyze resume text using AI (public endpoint)"""
    try:
        from ai_service import ai_service
        
        resume_text = request.get("resume_text", "")
        job_description = request.get("job_description")
        target_role = request.get("target_role")
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Resume text is required")
        
        # Create a mock request object for the AI service
        from models import ResumeAnalysisRequest
        analysis_request = ResumeAnalysisRequest(
            resume_text=resume_text,
            job_description=job_description,
            target_role=target_role
        )
        
        analysis = await ai_service.analyze_resume(analysis_request)
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {str(e)}")
