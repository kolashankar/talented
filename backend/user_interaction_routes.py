from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from models import (
    UserInteraction, DSAUserProgress, DSADiscussion, CompanyProfile,
    LikeResponse, SaveResponse, ShareResponse
)
from database import get_database
from user_auth import get_current_user
from datetime import datetime

interaction_router = APIRouter(prefix="/interactions", tags=["user-interactions"])

# Like/Unlike functionality
@interaction_router.post("/{content_type}/{content_id}/like")
async def toggle_like(
    content_type: str,
    content_id: str,
    current_user = Depends(get_current_user)
):
    """Toggle like status for content (article, job, internship, roadmap, dsa_problem)"""
    try:
        db = await get_database()
        
        # Check if already liked
        existing_like = await db.user_interactions.find_one({
            "user_id": current_user.id,
            "content_type": content_type,
            "content_id": content_id,
            "interaction_type": "like"
        })
        
        if existing_like:
            # Unlike
            await db.user_interactions.delete_one({"_id": existing_like["_id"]})
            liked = False
        else:
            # Like
            like_data = UserInteraction(
                user_id=current_user.id,
                content_type=content_type,
                content_id=content_id,
                interaction_type="like"
            )
            await db.user_interactions.insert_one(like_data.dict())
            liked = True
        
        # Get total likes count
        total_likes = await db.user_interactions.count_documents({
            "content_type": content_type,
            "content_id": content_id,
            "interaction_type": "like"
        })
        
        return LikeResponse(liked=liked, total_likes=total_likes)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle like: {str(e)}")

# Save/Unsave functionality
@interaction_router.post("/{content_type}/{content_id}/save")
async def toggle_save(
    content_type: str,
    content_id: str,
    current_user = Depends(get_current_user)
):
    """Toggle save status for content"""
    try:
        db = await get_database()
        
        # Check if already saved
        existing_save = await db.user_interactions.find_one({
            "user_id": current_user.id,
            "content_type": content_type,
            "content_id": content_id,
            "interaction_type": "save"
        })
        
        if existing_save:
            # Unsave
            await db.user_interactions.delete_one({"_id": existing_save["_id"]})
            return SaveResponse(saved=False, message="Removed from saved items")
        else:
            # Save
            save_data = UserInteraction(
                user_id=current_user.id,
                content_type=content_type,
                content_id=content_id,
                interaction_type="save"
            )
            await db.user_interactions.insert_one(save_data.dict())
            return SaveResponse(saved=True, message="Added to saved items")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle save: {str(e)}")

# Share functionality
@interaction_router.post("/{content_type}/{content_id}/share")
async def share_content(
    content_type: str,
    content_id: str,
    platform: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Share content and track sharing"""
    try:
        db = await get_database()
        
        # Generate share URL based on content type
        base_url = "https://talentd.com"  # Replace with actual domain
        share_urls = {
            "article": f"{base_url}/articles/{content_id}",
            "job": f"{base_url}/jobs/{content_id}",
            "internship": f"{base_url}/internships/{content_id}",
            "roadmap": f"{base_url}/roadmaps/{content_id}",
            "dsa_problem": f"{base_url}/dsa-corner/problem/{content_id}"
        }
        
        share_url = share_urls.get(content_type, f"{base_url}/{content_type}/{content_id}")
        
        # Track the share interaction
        share_data = UserInteraction(
            user_id=current_user.id,
            content_type=content_type,
            content_id=content_id,
            interaction_type="share",
            metadata={"platform": platform, "share_url": share_url}
        )
        await db.user_interactions.insert_one(share_data.dict())
        
        return ShareResponse(share_url=share_url, message="Content shared successfully")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to share content: {str(e)}")

# Apply to job/internship
@interaction_router.post("/{content_type}/{content_id}/apply")
async def apply_to_position(
    content_type: str,
    content_id: str,
    current_user = Depends(get_current_user)
):
    """Track job/internship application"""
    try:
        if content_type not in ["job", "internship"]:
            raise HTTPException(status_code=400, detail="Apply action only available for jobs and internships")
        
        db = await get_database()
        
        # Check if already applied
        existing_application = await db.user_interactions.find_one({
            "user_id": current_user.id,
            "content_type": content_type,
            "content_id": content_id,
            "interaction_type": "apply"
        })
        
        if existing_application:
            return {"message": "You have already applied to this position", "applied": True}
        
        # Track the application
        apply_data = UserInteraction(
            user_id=current_user.id,
            content_type=content_type,
            content_id=content_id,
            interaction_type="apply"
        )
        await db.user_interactions.insert_one(apply_data.dict())
        
        # Update application count in the job/internship
        collection = db.jobs if content_type == "job" else db.internships
        await collection.update_one(
            {"id": content_id},
            {"$inc": {"applications": 1}}
        )
        
        return {"message": "Application recorded successfully", "applied": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply: {str(e)}")

# Get user's saved items
@interaction_router.get("/saved")
async def get_saved_items(
    content_type: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get user's saved items"""
    try:
        db = await get_database()
        
        filter_criteria = {
            "user_id": current_user.id,
            "interaction_type": "save"
        }
        
        if content_type:
            filter_criteria["content_type"] = content_type
        
        saved_items = await db.user_interactions.find(filter_criteria).sort("created_at", -1).to_list(100)
        
        return {"saved_items": saved_items}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch saved items: {str(e)}")

# Get user's interaction status for content
@interaction_router.get("/{content_type}/{content_id}/status")
async def get_interaction_status(
    content_type: str,
    content_id: str,
    current_user = Depends(get_current_user)
):
    """Get user's interaction status for specific content"""
    try:
        db = await get_database()
        
        interactions = await db.user_interactions.find({
            "user_id": current_user.id,
            "content_type": content_type,
            "content_id": content_id
        }).to_list(10)
        
        status = {
            "liked": False,
            "saved": False,
            "applied": False,
            "shared": False
        }
        
        for interaction in interactions:
            if interaction["interaction_type"] in status:
                status[interaction["interaction_type"]] = True
        
        # Get total likes count
        total_likes = await db.user_interactions.count_documents({
            "content_type": content_type,
            "content_id": content_id,
            "interaction_type": "like"
        })
        
        status["total_likes"] = total_likes
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get interaction status: {str(e)}")