from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import HTMLResponse
from models import (
    PortfolioCreate, Portfolio, PortfolioUpdate, PortfolioTemplate,
    PortfolioGenerateRequest, PortfolioGenerateResponse, User
)
from ai_service import ai_service
from user_auth import get_current_active_user, get_current_user_optional
from database import get_database
import logging
from typing import List, Optional
import json
import uuid

logger = logging.getLogger(__name__)

# Create router for portfolio routes
portfolio_router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@portfolio_router.get("/templates", response_model=List[PortfolioTemplate])
async def get_portfolio_templates():
    """Get all available portfolio templates"""
    try:
        db = await get_database()
        templates = []
        
        # Get templates from database or return default ones
        db_templates = await db.portfolio_templates.find({"is_active": True}).to_list(length=None)
        
        if db_templates:
            for template in db_templates:
                templates.append(PortfolioTemplate(**template))
        else:
            # Create default templates if none exist
            default_templates = await create_default_templates()
            templates = default_templates
        
        return templates
        
    except Exception as e:
        logger.error(f"Error fetching portfolio templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch templates")

@portfolio_router.post("/generate", response_model=PortfolioGenerateResponse)
async def generate_portfolio(
    request: PortfolioGenerateRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Generate portfolio website using AI"""
    try:
        # Validate template exists
        db = await get_database()
        template = await db.portfolio_templates.find_one({"id": request.template_id, "is_active": True})
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Generate portfolio content using AI
        generated_portfolio = await ai_service.generate_portfolio(request)
        
        # Create portfolio record
        share_token = str(uuid.uuid4())
        live_url = f"/portfolio/view/{share_token}"
        
        portfolio_data = PortfolioCreate(
            user_id=current_user.id,
            template_id=request.template_id,
            title=f"{request.resume_data.personal_details.full_name}'s Portfolio",
            resume_data=request.resume_data,
            custom_prompt=request.user_prompt
        )
        
        portfolio = Portfolio(**portfolio_data.dict(), live_url=live_url, share_token=share_token)
        portfolio_dict = portfolio.dict()
        await db.portfolios.insert_one(portfolio_dict)
        
        response = PortfolioGenerateResponse(
            generated_content=generated_portfolio["content"],
            html_content=generated_portfolio["html"],
            css_content=generated_portfolio["css"],
            live_url=live_url,
            share_token=share_token
        )
        
        logger.info(f"Portfolio generated for user {current_user.email}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate portfolio: {str(e)}")

@portfolio_router.get("/my-portfolios", response_model=List[Portfolio])
async def get_user_portfolios(current_user: User = Depends(get_current_active_user)):
    """Get all portfolios created by the current user"""
    try:
        db = await get_database()
        portfolios = await db.portfolios.find({"user_id": current_user.id}).sort("created_at", -1).to_list(length=None)
        
        result = []
        for portfolio in portfolios:
            result.append(Portfolio(**portfolio))
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching user portfolios: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch portfolios")

@portfolio_router.get("/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(
    portfolio_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific portfolio by ID"""
    try:
        db = await get_database()
        portfolio = await db.portfolios.find_one({"id": portfolio_id, "user_id": current_user.id})
        
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        return Portfolio(**portfolio)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch portfolio")

@portfolio_router.put("/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(
    portfolio_id: str,
    update_data: PortfolioUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a portfolio"""
    try:
        db = await get_database()
        
        # Check if portfolio exists and belongs to user
        existing_portfolio = await db.portfolios.find_one({"id": portfolio_id, "user_id": current_user.id})
        if not existing_portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        # Update portfolio
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        update_dict["updated_at"] = datetime.utcnow()
        
        await db.portfolios.update_one(
            {"id": portfolio_id}, 
            {"$set": update_dict}
        )
        
        # Return updated portfolio
        updated_portfolio = await db.portfolios.find_one({"id": portfolio_id})
        return Portfolio(**updated_portfolio)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update portfolio")

@portfolio_router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a portfolio"""
    try:
        db = await get_database()
        
        # Check if portfolio exists and belongs to user
        result = await db.portfolios.delete_one({"id": portfolio_id, "user_id": current_user.id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        return {"message": "Portfolio deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete portfolio")

@portfolio_router.get("/view/{share_token}", response_class=HTMLResponse)
async def view_portfolio(share_token: str, request: Request):
    """View portfolio by share token (public endpoint)"""
    try:
        db = await get_database()
        portfolio = await db.portfolios.find_one({"share_token": share_token, "is_public": True})
        
        if not portfolio:
            return HTMLResponse(content="<h1>Portfolio not found</h1>", status_code=404)
        
        # Increment view count
        await db.portfolios.update_one(
            {"share_token": share_token},
            {"$inc": {"views": 1}}
        )
        
        # Generate HTML content for the portfolio
        html_content = await ai_service.render_portfolio_html(Portfolio(**portfolio))
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"Error viewing portfolio: {str(e)}")
        return HTMLResponse(content="<h1>Error loading portfolio</h1>", status_code=500)

async def create_default_templates() -> List[PortfolioTemplate]:
    """Create default portfolio templates"""
    db = await get_database()
    
    templates = [
        {
            "id": str(uuid.uuid4()),
            "name": "Modern Professional",
            "description": "Clean, modern design perfect for developers and professionals",
            "preview_image": "/templates/modern-professional.jpg",
            "template_data": {
                "theme": "modern",
                "colors": {"primary": "#3b82f6", "secondary": "#1f2937", "accent": "#10b981"},
                "layout": "single-page",
                "sections": ["hero", "about", "skills", "experience", "projects", "education", "contact"]
            },
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Creative Portfolio",
            "description": "Vibrant and creative design for designers and creative professionals",
            "preview_image": "/templates/creative-portfolio.jpg",
            "template_data": {
                "theme": "creative",
                "colors": {"primary": "#f59e0b", "secondary": "#7c3aed", "accent": "#ec4899"},
                "layout": "multi-page",
                "sections": ["hero", "about", "portfolio", "skills", "experience", "contact"]
            },
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Minimalist",
            "description": "Clean and minimal design focusing on content",
            "preview_image": "/templates/minimalist.jpg",
            "template_data": {
                "theme": "minimalist",
                "colors": {"primary": "#374151", "secondary": "#9ca3af", "accent": "#6366f1"},
                "layout": "single-page",
                "sections": ["hero", "about", "experience", "skills", "projects", "contact"]
            },
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Tech Focus",
            "description": "Technology-focused design with dark theme",
            "preview_image": "/templates/tech-focus.jpg",
            "template_data": {
                "theme": "tech",
                "colors": {"primary": "#22d3ee", "secondary": "#1e293b", "accent": "#a855f7"},
                "layout": "single-page",
                "sections": ["hero", "about", "skills", "projects", "experience", "education", "contact"]
            },
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Corporate",
            "description": "Professional corporate design suitable for business professionals",
            "preview_image": "/templates/corporate.jpg",
            "template_data": {
                "theme": "corporate",
                "colors": {"primary": "#1d4ed8", "secondary": "#475569", "accent": "#059669"},
                "layout": "multi-page",
                "sections": ["hero", "about", "experience", "skills", "achievements", "education", "contact"]
            },
            "is_active": True
        }
    ]
    
    # Insert templates into database
    for template_data in templates:
        existing = await db.portfolio_templates.find_one({"name": template_data["name"]})
        if not existing:
            await db.portfolio_templates.insert_one(template_data)
    
    # Return template objects
    return [PortfolioTemplate(**template) for template in templates]