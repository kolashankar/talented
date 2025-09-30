from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from models import Job, Internship, Article, Roadmap, ContentStatus
from database import get_database
import logging

logger = logging.getLogger(__name__)

# Create router for public routes (user app)
public_router = APIRouter(prefix="/public", tags=["public"])

# Public Job Routes
@public_router.get("/jobs", response_model=List[Job])
async def get_published_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    search: Optional[str] = None,
    location: Optional[str] = None,
    experience_level: Optional[str] = None,
    job_type: Optional[str] = None,
    skills: Optional[str] = None
):
    """Get published jobs for public consumption"""
    try:
        db = await get_database()
        query = {"status": ContentStatus.PUBLISHED}
        
        # Add search filters
        if search:
            query["$text"] = {"$search": search}
        
        if location:
            query["location"] = {"$regex": location, "$options": "i"}
        
        if experience_level:
            query["experience_level"] = experience_level
        
        if job_type:
            query["job_type"] = job_type
        
        if skills:
            skills_list = [skill.strip() for skill in skills.split(",")]
            query["skills_required"] = {"$in": skills_list}
        
        jobs = await db.jobs.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        
        # Increment view counts for returned jobs
        job_ids = [job["id"] for job in jobs]
        await db.jobs.update_many(
            {"id": {"$in": job_ids}},
            {"$inc": {"views": 1}}
        )
        
        return [Job(**job) for job in jobs]
    except Exception as e:
        logger.error(f"Error fetching public jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@public_router.get("/jobs/{job_id}", response_model=Job)
async def get_job_details(job_id: str = Path(..., description="Job ID")):
    """Get specific job details"""
    try:
        db = await get_database()
        job = await db.jobs.find_one({"id": job_id, "status": ContentStatus.PUBLISHED})
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Increment view count
        await db.jobs.update_one(
            {"id": job_id},
            {"$inc": {"views": 1}}
        )
        
        return Job(**job)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Public Internship Routes
@public_router.get("/internships", response_model=List[Internship])
async def get_published_internships(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    search: Optional[str] = None,
    location: Optional[str] = None,
    duration: Optional[int] = None,
    skills: Optional[str] = None
):
    """Get published internships for public consumption"""
    try:
        db = await get_database()
        query = {"status": ContentStatus.PUBLISHED}
        
        # Add search filters
        if search:
            query["$text"] = {"$search": search}
        
        if location:
            query["location"] = {"$regex": location, "$options": "i"}
        
        if duration:
            query["duration_months"] = duration
        
        if skills:
            skills_list = [skill.strip() for skill in skills.split(",")]
            query["skills_required"] = {"$in": skills_list}
        
        internships = await db.internships.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        
        # Increment view counts
        internship_ids = [internship["id"] for internship in internships]
        await db.internships.update_many(
            {"id": {"$in": internship_ids}},
            {"$inc": {"views": 1}}
        )
        
        return [Internship(**internship) for internship in internships]
    except Exception as e:
        logger.error(f"Error fetching public internships: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@public_router.get("/internships/{internship_id}", response_model=Internship)
async def get_internship_details(internship_id: str = Path(..., description="Internship ID")):
    """Get specific internship details"""
    try:
        db = await get_database()
        internship = await db.internships.find_one({"id": internship_id, "status": ContentStatus.PUBLISHED})
        
        if not internship:
            raise HTTPException(status_code=404, detail="Internship not found")
        
        # Increment view count
        await db.internships.update_one(
            {"id": internship_id},
            {"$inc": {"views": 1}}
        )
        
        return Internship(**internship)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching internship details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Public Article Routes
@public_router.get("/articles", response_model=List[Article])
async def get_published_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    search: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None
):
    """Get published articles for public consumption"""
    try:
        db = await get_database()
        query = {"status": ContentStatus.PUBLISHED}
        
        # Add search filters
        if search:
            query["$text"] = {"$search": search}
        
        if category:
            query["category"] = category
        
        if tags:
            tags_list = [tag.strip() for tag in tags.split(",")]
            query["tags"] = {"$in": tags_list}
        
        articles = await db.articles.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        
        # Increment view counts
        article_ids = [article["id"] for article in articles]
        await db.articles.update_many(
            {"id": {"$in": article_ids}},
            {"$inc": {"views": 1}}
        )
        
        return [Article(**article) for article in articles]
    except Exception as e:
        logger.error(f"Error fetching public articles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@public_router.get("/articles/{article_slug}", response_model=Article)
async def get_article_by_slug(article_slug: str = Path(..., description="Article slug")):
    """Get specific article by slug"""
    try:
        db = await get_database()
        article = await db.articles.find_one({"slug": article_slug, "status": ContentStatus.PUBLISHED})
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Increment view count
        await db.articles.update_one(
            {"slug": article_slug},
            {"$inc": {"views": 1}}
        )
        
        return Article(**article)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching article: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Public Roadmap Routes
@public_router.get("/roadmaps", response_model=List[Roadmap])
async def get_published_roadmaps(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    search: Optional[str] = None,
    difficulty: Optional[str] = None,
    tags: Optional[str] = None
):
    """Get published roadmaps for public consumption"""
    try:
        db = await get_database()
        query = {"status": ContentStatus.PUBLISHED}
        
        # Add search filters
        if search:
            query["$text"] = {"$search": search}
        
        if difficulty:
            query["difficulty_level"] = difficulty
        
        if tags:
            tags_list = [tag.strip() for tag in tags.split(",")]
            query["tags"] = {"$in": tags_list}
        
        roadmaps = await db.roadmaps.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        
        # Increment view counts
        roadmap_ids = [roadmap["id"] for roadmap in roadmaps]
        await db.roadmaps.update_many(
            {"id": {"$in": roadmap_ids}},
            {"$inc": {"views": 1}}
        )
        
        return [Roadmap(**roadmap) for roadmap in roadmaps]
    except Exception as e:
        logger.error(f"Error fetching public roadmaps: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@public_router.get("/roadmaps/{roadmap_slug}", response_model=Roadmap)
async def get_roadmap_by_slug(roadmap_slug: str = Path(..., description="Roadmap slug")):
    """Get specific roadmap by slug"""
    try:
        db = await get_database()
        roadmap = await db.roadmaps.find_one({"slug": roadmap_slug, "status": ContentStatus.PUBLISHED})
        
        if not roadmap:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        # Increment view count
        await db.roadmaps.update_one(
            {"slug": roadmap_slug},
            {"$inc": {"views": 1}}
        )
        
        return Roadmap(**roadmap)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Statistics endpoints
@public_router.get("/stats")
async def get_public_stats():
    """Get public statistics"""
    try:
        db = await get_database()
        
        total_jobs = await db.jobs.count_documents({"status": ContentStatus.PUBLISHED})
        total_internships = await db.internships.count_documents({"status": ContentStatus.PUBLISHED})
        total_articles = await db.articles.count_documents({"status": ContentStatus.PUBLISHED})
        total_roadmaps = await db.roadmaps.count_documents({"status": ContentStatus.PUBLISHED})
        
        return {
            "total_jobs": total_jobs,
            "total_internships": total_internships,
            "total_articles": total_articles,
            "total_roadmaps": total_roadmaps,
            "community_members": 46229,  # Static for now
            "monthly_readers": 623117   # Static for now
        }
    except Exception as e:
        logger.error(f"Error fetching public stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Search endpoint
@public_router.get("/search")
async def search_content(
    q: str = Query(..., description="Search query"),
    content_type: Optional[str] = Query(None, description="Content type filter: jobs, internships, articles, roadmaps"),
    limit: int = Query(10, ge=1, le=50)
):
    """Search across all content types"""
    try:
        db = await get_database()
        results = {"jobs": [], "internships": [], "articles": [], "roadmaps": []}
        
        search_query = {"$text": {"$search": q}, "status": ContentStatus.PUBLISHED}
        
        if not content_type or content_type == "jobs":
            jobs = await db.jobs.find(search_query).limit(limit).to_list(length=limit)
            results["jobs"] = [{"id": job["id"], "title": job["title"], "company": job["company"], "location": job["location"]} for job in jobs]
        
        if not content_type or content_type == "internships":
            internships = await db.internships.find(search_query).limit(limit).to_list(length=limit)
            results["internships"] = [{"id": internship["id"], "title": internship["title"], "company": internship["company"], "location": internship["location"]} for internship in internships]
        
        if not content_type or content_type == "articles":
            articles = await db.articles.find(search_query).limit(limit).to_list(length=limit)
            results["articles"] = [{"id": article["id"], "title": article["title"], "slug": article["slug"], "category": article["category"]} for article in articles]
        
        if not content_type or content_type == "roadmaps":
            roadmaps = await db.roadmaps.find(search_query).limit(limit).to_list(length=limit)
            results["roadmaps"] = [{"id": roadmap["id"], "title": roadmap["title"], "slug": roadmap["slug"], "difficulty_level": roadmap["difficulty_level"]} for roadmap in roadmaps]
        
        return results
    except Exception as e:
        logger.error(f"Error searching content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))