from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models import CompanyProfile
from database import get_database

company_router = APIRouter(prefix="/companies", tags=["companies"])

@company_router.get("/{company_id}")
async def get_company_profile(company_id: str):
    """Get company profile details"""
    try:
        db = await get_database()
        
        company = await db.company_profiles.find_one({"id": company_id})
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Get associated jobs and internships
        jobs = await db.jobs.find({"company": company["name"]}).limit(10).to_list(10)
        internships = await db.internships.find({"company": company["name"]}).limit(10).to_list(10)
        
        return {
            "company": company,
            "recent_jobs": jobs,
            "recent_internships": internships
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch company profile: {str(e)}")

@company_router.get("/")
async def search_companies(
    search: Optional[str] = None,
    industry: Optional[str] = None,
    size: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
):
    """Search companies with filters"""
    try:
        db = await get_database()
        
        filter_criteria = {}
        
        if search:
            filter_criteria["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}}
            ]
        
        if industry:
            filter_criteria["industry"] = industry
        
        if size:
            filter_criteria["size"] = size
            
        if location:
            filter_criteria["location"] = {"$regex": location, "$options": "i"}
        
        companies = await db.company_profiles.find(filter_criteria).skip(skip).limit(limit).to_list(limit)
        total_count = await db.company_profiles.count_documents(filter_criteria)
        
        return {
            "companies": companies,
            "total": total_count,
            "page": (skip // limit) + 1,
            "total_pages": (total_count + limit - 1) // limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search companies: {str(e)}")

@company_router.get("/{company_name}/jobs")
async def get_company_jobs(company_name: str, limit: int = 20, skip: int = 0):
    """Get all jobs from a specific company"""
    try:
        db = await get_database()
        
        jobs = await db.jobs.find({
            "company": {"$regex": f"^{company_name}$", "$options": "i"},
            "status": "published"
        }).skip(skip).limit(limit).to_list(limit)
        
        total_count = await db.jobs.count_documents({
            "company": {"$regex": f"^{company_name}$", "$options": "i"},
            "status": "published"
        })
        
        return {
            "jobs": jobs,
            "total": total_count,
            "page": (skip // limit) + 1,
            "total_pages": (total_count + limit - 1) // limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch company jobs: {str(e)}")

@company_router.get("/{company_name}/internships")
async def get_company_internships(company_name: str, limit: int = 20, skip: int = 0):
    """Get all internships from a specific company"""
    try:
        db = await get_database()
        
        internships = await db.internships.find({
            "company": {"$regex": f"^{company_name}$", "$options": "i"},
            "status": "published"
        }).skip(skip).limit(limit).to_list(limit)
        
        total_count = await db.internships.count_documents({
            "company": {"$regex": f"^{company_name}$", "$options": "i"},
            "status": "published"
        })
        
        return {
            "internships": internships,
            "total": total_count,
            "page": (skip // limit) + 1,
            "total_pages": (total_count + limit - 1) // limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch company internships: {str(e)}")

@company_router.get("/stats/industries")
async def get_industry_stats():
    """Get statistics about companies by industry"""
    try:
        db = await get_database()
        
        pipeline = [
            {"$group": {"_id": "$industry", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 20}
        ]
        
        industries = await db.company_profiles.aggregate(pipeline).to_list(20)
        
        return {"industries": industries}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch industry stats: {str(e)}")