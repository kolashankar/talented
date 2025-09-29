from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from ai_agent_service import ai_agent
from auth import get_current_active_admin, AdminUser
import logging

logger = logging.getLogger(__name__)

# Create router for AI agent routes
ai_agent_router = APIRouter(prefix="/ai-agent", tags=["ai-agent"])

@ai_agent_router.post("/generate/job")
async def generate_job_content(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate job content using AI"""
    try:
        prompt = request.get("prompt", "")
        job_type = request.get("job_type", "software")
        
        content = await ai_agent.generate_job_content(prompt, job_type)
        
        return {
            "success": True,
            "content": content,
            "message": "Job content generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating job content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/generate/internship")
async def generate_internship_content(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate internship content using AI"""
    try:
        prompt = request.get("prompt", "")
        field = request.get("field", "technology")
        
        content = await ai_agent.generate_internship_content(prompt, field)
        
        return {
            "success": True,
            "content": content,
            "message": "Internship content generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating internship content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/generate/article")
async def generate_article_content(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate article content using AI"""
    try:
        prompt = request.get("prompt", "")
        topic = request.get("topic", "technology")
        
        content = await ai_agent.generate_article_content(prompt, topic)
        
        return {
            "success": True,
            "content": content,
            "message": "Article content generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating article content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/generate/roadmap")
async def generate_roadmap_content(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate roadmap content using AI"""
    try:
        prompt = request.get("prompt", "")
        skill = request.get("skill", "programming")
        
        content = await ai_agent.generate_roadmap_content(prompt, skill)
        
        return {
            "success": True,
            "content": content,
            "message": "Roadmap content generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating roadmap content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/generate/dsa-problem")
async def generate_dsa_problem_content(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate DSA problem content using AI"""
    try:
        prompt = request.get("prompt", "")
        difficulty = request.get("difficulty", "medium")
        
        content = await ai_agent.generate_dsa_problem(prompt, difficulty)
        
        return {
            "success": True,
            "content": content,
            "message": "DSA problem content generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating DSA problem content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/generate/company-logo")
async def generate_company_logo(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate company logo using AI"""
    try:
        company_name = request.get("company_name", "")
        
        if not company_name:
            raise HTTPException(status_code=400, detail="Company name is required")
        
        logo_url = await ai_agent.generate_company_logo(company_name)
        
        return {
            "success": True,
            "logo_url": logo_url,
            "message": "Company logo generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating company logo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/generate/mindmap")
async def generate_mindmap(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Generate mindmap structure using AI"""
    try:
        topic = request.get("topic", "")
        
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        mindmap_data = await ai_agent.generate_mindmap_content(topic)
        
        return {
            "success": True,
            "mindmap": mindmap_data,
            "message": "Mindmap generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating mindmap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/upload-image")
async def upload_image(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Upload image to Cloudinary"""
    try:
        image_url = request.get("image_url", "")
        public_id = request.get("public_id")
        
        if not image_url:
            raise HTTPException(status_code=400, detail="Image URL is required")
        
        uploaded_url = await ai_agent.upload_image_to_cloudinary(image_url, public_id)
        
        return {
            "success": True,
            "uploaded_url": uploaded_url,
            "message": "Image uploaded successfully"
        }
        
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agent_router.post("/auto-fill")
async def auto_fill_form(
    request: Dict[str, Any],
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Auto-fill form based on content type and prompt"""
    try:
        content_type = request.get("content_type", "")
        prompt = request.get("prompt", "")
        additional_params = request.get("params", {})
        
        if not content_type:
            raise HTTPException(status_code=400, detail="Content type is required")
        
        content = None
        
        if content_type == "job":
            job_type = additional_params.get("job_type", "software")
            content = await ai_agent.generate_job_content(prompt, job_type)
        elif content_type == "internship":
            field = additional_params.get("field", "technology")
            content = await ai_agent.generate_internship_content(prompt, field)
        elif content_type == "article":
            topic = additional_params.get("topic", "technology")
            content = await ai_agent.generate_article_content(prompt, topic)
        elif content_type == "roadmap":
            skill = additional_params.get("skill", "programming")
            content = await ai_agent.generate_roadmap_content(prompt, skill)
        elif content_type == "dsa_problem":
            difficulty = additional_params.get("difficulty", "medium")
            content = await ai_agent.generate_dsa_problem(prompt, difficulty)
        else:
            raise HTTPException(status_code=400, detail="Invalid content type")
        
        return {
            "success": True,
            "content": content,
            "message": f"{content_type.title()} form auto-filled successfully"
        }
        
    except Exception as e:
        logger.error(f"Error auto-filling form: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))