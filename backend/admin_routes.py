from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from models import (
    Job, JobCreate, JobUpdate, 
    Internship, InternshipCreate, InternshipUpdate,
    Article, ArticleCreate, ArticleUpdate,
    Roadmap, RoadmapCreate, RoadmapUpdate,
    ContentStatus, DashboardStats,
    DSAProblem, DSAProblemCreate, DSAProblemUpdate,
    DSACategory, DSATopic, DSAChapter, DSADifficulty
)
from database import get_database
from auth import get_current_active_admin, AdminUser
from datetime import datetime
import logging
from expiration_service import check_expired_content

logger = logging.getLogger(__name__)

# Create router for admin routes
admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Job Management Routes
@admin_router.post("/jobs", response_model=Job)
async def create_job(job_data: JobCreate, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Create a new job posting"""
    try:
        db = await get_database()
        
        # Process the job data
        job_dict = job_data.dict()
        
        # Handle skills field mapping
        if job_dict.get('skills') and not job_dict.get('skills_required'):
            job_dict['skills_required'] = job_dict['skills']
        elif not job_dict.get('skills') and job_dict.get('skills_required'):
            job_dict['skills'] = job_dict['skills_required']
        
        # Set default duration_months if duration is provided
        if job_dict.get('duration') and not job_dict.get('duration_months'):
            try:
                # Try to extract months from duration string
                duration_str = job_dict['duration'].lower()
                if 'month' in duration_str:
                    import re
                    months = re.findall(r'\d+', duration_str)
                    if months:
                        job_dict['duration_months'] = int(months[0])
            except:
                pass
        
        job = Job(**job_dict, created_by=current_admin.username)
        job_dict = job.dict()
        
        result = await db.jobs.insert_one(job_dict)
        if result.inserted_id:
            return job
        else:
            raise HTTPException(status_code=500, detail="Failed to create job")
    except Exception as e:
        logger.error(f"Error creating job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/jobs", response_model=List[Job])
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    search: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Get all jobs with pagination and filtering"""
    try:
        db = await get_database()
        query = {}
        
        if status:
            query["status"] = status
        
        if search:
            query["$text"] = {"$search": search}
        
        jobs = await db.jobs.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [Job(**job) for job in jobs]
    except Exception as e:
        logger.error(f"Error fetching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/jobs/{job_id}", response_model=Job)
async def get_job(job_id: str, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Get a specific job by ID"""
    try:
        db = await get_database()
        job = await db.jobs.find_one({"id": job_id})
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return Job(**job)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.put("/jobs/{job_id}", response_model=Job)
async def update_job(
    job_id: str, 
    job_update: JobUpdate, 
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Update a job posting"""
    try:
        db = await get_database()
        
        # Remove None values from update data
        update_data = {k: v for k, v in job_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.jobs.update_one(
            {"id": job_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        
        updated_job = await db.jobs.find_one({"id": job_id})
        return Job(**updated_job)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.delete("/jobs/{job_id}")
async def delete_job(job_id: str, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Delete a job posting"""
    try:
        db = await get_database()
        result = await db.jobs.delete_one({"id": job_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {"message": "Job deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Internship Management Routes
@admin_router.post("/internships", response_model=Internship)
async def create_internship(internship_data: InternshipCreate, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Create a new internship posting"""
    try:
        db = await get_database()
        
        # Process the internship data
        internship_dict = internship_data.dict()
        
        # Handle skills field mapping
        if internship_dict.get('skills') and not internship_dict.get('skills_required'):
            internship_dict['skills_required'] = internship_dict['skills']
        elif not internship_dict.get('skills') and internship_dict.get('skills_required'):
            internship_dict['skills'] = internship_dict['skills_required']
        
        # Set default duration_months if duration is provided
        if internship_dict.get('duration') and not internship_dict.get('duration_months'):
            try:
                # Try to extract months from duration string
                duration_str = internship_dict['duration'].lower()
                if 'month' in duration_str:
                    import re
                    months = re.findall(r'\d+', duration_str)
                    if months:
                        internship_dict['duration_months'] = int(months[0])
                else:
                    internship_dict['duration_months'] = 3  # Default to 3 months
            except:
                internship_dict['duration_months'] = 3  # Default to 3 months
        
        internship = Internship(**internship_dict, created_by=current_admin.username)
        internship_dict = internship.dict()
        
        result = await db.internships.insert_one(internship_dict)
        if result.inserted_id:
            return internship
        else:
            raise HTTPException(status_code=500, detail="Failed to create internship")
    except Exception as e:
        logger.error(f"Error creating internship: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/internships", response_model=List[Internship])
async def get_internships(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    search: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Get all internships with pagination and filtering"""
    try:
        db = await get_database()
        query = {}
        
        if status:
            query["status"] = status
        
        if search:
            query["$text"] = {"$search": search}
        
        internships = await db.internships.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [Internship(**internship) for internship in internships]
    except Exception as e:
        logger.error(f"Error fetching internships: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.put("/internships/{internship_id}", response_model=Internship)
async def update_internship(
    internship_id: str, 
    internship_update: InternshipUpdate, 
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Update an internship posting"""
    try:
        db = await get_database()
        
        update_data = {k: v for k, v in internship_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.internships.update_one(
            {"id": internship_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Internship not found")
        
        updated_internship = await db.internships.find_one({"id": internship_id})
        return Internship(**updated_internship)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating internship: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.delete("/internships/{internship_id}")
async def delete_internship(internship_id: str, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Delete an internship posting"""
    try:
        db = await get_database()
        result = await db.internships.delete_one({"id": internship_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Internship not found")
        
        return {"message": "Internship deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting internship: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Article Management Routes
@admin_router.post("/articles", response_model=Article)
async def create_article(article_data: ArticleCreate, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Create a new article"""
    try:
        db = await get_database()
        
        # Check if slug is unique
        existing_article = await db.articles.find_one({"slug": article_data.slug})
        if existing_article:
            raise HTTPException(status_code=400, detail="Article with this slug already exists")
        
        # Process the article data
        article_dict = article_data.dict()
        
        # Set default author if not provided
        if not article_dict.get('author'):
            article_dict['author'] = current_admin.username
        
        # Set default excerpt if not provided
        if not article_dict.get('excerpt') and article_dict.get('content'):
            # Create excerpt from first 150 characters of content
            article_dict['excerpt'] = article_dict['content'][:150] + "..." if len(article_dict['content']) > 150 else article_dict['content']
        
        article = Article(**article_dict, created_by=current_admin.username)
        article_dict = article.dict()
        
        result = await db.articles.insert_one(article_dict)
        if result.inserted_id:
            return article
        else:
            raise HTTPException(status_code=500, detail="Failed to create article")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating article: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/articles", response_model=List[Article])
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Get all articles with pagination and filtering"""
    try:
        db = await get_database()
        query = {}
        
        if status:
            query["status"] = status
        
        if category:
            query["category"] = category
        
        if search:
            query["$text"] = {"$search": search}
        
        articles = await db.articles.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [Article(**article) for article in articles]
    except Exception as e:
        logger.error(f"Error fetching articles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.put("/articles/{article_id}", response_model=Article)
async def update_article(
    article_id: str, 
    article_update: ArticleUpdate, 
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Update an article"""
    try:
        db = await get_database()
        
        # Check if slug is unique (if being updated)
        if article_update.slug:
            existing_article = await db.articles.find_one({
                "slug": article_update.slug, 
                "id": {"$ne": article_id}
            })
            if existing_article:
                raise HTTPException(status_code=400, detail="Article with this slug already exists")
        
        update_data = {k: v for k, v in article_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.articles.update_one(
            {"id": article_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        
        updated_article = await db.articles.find_one({"id": article_id})
        return Article(**updated_article)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating article: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.delete("/articles/{article_id}")
async def delete_article(article_id: str, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Delete an article"""
    try:
        db = await get_database()
        result = await db.articles.delete_one({"id": article_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return {"message": "Article deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting article: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Roadmap Management Routes
@admin_router.post("/roadmaps", response_model=Roadmap)
async def create_roadmap(roadmap_data: RoadmapCreate, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Create a new roadmap"""
    try:
        db = await get_database()
        
        # Check if slug is unique
        existing_roadmap = await db.roadmaps.find_one({"slug": roadmap_data.slug})
        if existing_roadmap:
            raise HTTPException(status_code=400, detail="Roadmap with this slug already exists")
        
        roadmap = Roadmap(**roadmap_data.dict(), created_by=current_admin.username)
        roadmap_dict = roadmap.dict()
        
        result = await db.roadmaps.insert_one(roadmap_dict)
        if result.inserted_id:
            return roadmap
        else:
            raise HTTPException(status_code=500, detail="Failed to create roadmap")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/roadmaps", response_model=List[Roadmap])
async def get_roadmaps(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Get all roadmaps with pagination and filtering"""
    try:
        db = await get_database()
        query = {}
        
        if status:
            query["status"] = status
        
        if difficulty:
            query["difficulty_level"] = difficulty
        
        if search:
            query["$text"] = {"$search": search}
        
        roadmaps = await db.roadmaps.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [Roadmap(**roadmap) for roadmap in roadmaps]
    except Exception as e:
        logger.error(f"Error fetching roadmaps: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.put("/roadmaps/{roadmap_id}", response_model=Roadmap)
async def update_roadmap(
    roadmap_id: str, 
    roadmap_update: RoadmapUpdate, 
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Update a roadmap"""
    try:
        db = await get_database()
        
        # Check if slug is unique (if being updated)
        if roadmap_update.slug:
            existing_roadmap = await db.roadmaps.find_one({
                "slug": roadmap_update.slug, 
                "id": {"$ne": roadmap_id}
            })
            if existing_roadmap:
                raise HTTPException(status_code=400, detail="Roadmap with this slug already exists")
        
        update_data = {k: v for k, v in roadmap_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.roadmaps.update_one(
            {"id": roadmap_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        updated_roadmap = await db.roadmaps.find_one({"id": roadmap_id})
        return Roadmap(**updated_roadmap)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.delete("/roadmaps/{roadmap_id}")
async def delete_roadmap(roadmap_id: str, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Delete a roadmap"""
    try:
        db = await get_database()
        result = await db.roadmaps.delete_one({"id": roadmap_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        return {"message": "Roadmap deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Dashboard Statistics
@admin_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_admin: AdminUser = Depends(get_current_active_admin)):
    """Get dashboard statistics"""
    try:
        db = await get_database()
        
        # Count totals
        total_jobs = await db.jobs.count_documents({})
        total_internships = await db.internships.count_documents({})
        total_articles = await db.articles.count_documents({})
        total_roadmaps = await db.roadmaps.count_documents({})
        
        # Calculate total views and applications
        jobs_stats = await db.jobs.aggregate([
            {"$group": {
                "_id": None,
                "total_views": {"$sum": "$views"},
                "total_applications": {"$sum": "$applications"}
            }}
        ]).to_list(1)
        
        internship_stats = await db.internships.aggregate([
            {"$group": {
                "_id": None,
                "total_views": {"$sum": "$views"},
                "total_applications": {"$sum": "$applications"}
            }}
        ]).to_list(1)
        
        total_views = (
            jobs_stats[0]["total_views"] if jobs_stats else 0
        ) + (
            internship_stats[0]["total_views"] if internship_stats else 0
        )
        
        total_applications = (
            jobs_stats[0]["total_applications"] if jobs_stats else 0
        ) + (
            internship_stats[0]["total_applications"] if internship_stats else 0
        )
        
        # Get recent activity (last 10 items)
        recent_jobs = await db.jobs.find().sort("created_at", -1).limit(5).to_list(5)
        recent_articles = await db.articles.find().sort("created_at", -1).limit(5).to_list(5)
        
        recent_activity = []
        for job in recent_jobs:
            recent_activity.append({
                "type": "job",
                "title": job["title"],
                "created_at": job["created_at"],
                "status": job["status"]
            })
        
        for article in recent_articles:
            recent_activity.append({
                "type": "article", 
                "title": article["title"],
                "created_at": article["created_at"],
                "status": article["status"]
            })
        
        # Sort by created_at and limit to 10
        recent_activity.sort(key=lambda x: x["created_at"], reverse=True)
        recent_activity = recent_activity[:10]
        
        # Get popular content (by views)
        popular_jobs = await db.jobs.find().sort("views", -1).limit(5).to_list(5)
        popular_content = []
        
        for job in popular_jobs:
            popular_content.append({
                "type": "job",
                "title": job["title"],
                "views": job["views"],
                "applications": job["applications"]
            })
        
        stats = DashboardStats(
            total_jobs=total_jobs,
            total_internships=total_internships,
            total_articles=total_articles,
            total_roadmaps=total_roadmaps,
            total_views=total_views,
            total_applications=total_applications,
            recent_activity=recent_activity,
            popular_content=popular_content
        )
        
        return stats
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# DSA Corner Management Routes
@admin_router.post("/dsa-problems", response_model=DSAProblem)
async def create_dsa_problem(problem_data: DSAProblemCreate, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Create a new DSA problem"""
    try:
        db = await get_database()
        
        # Check if slug is unique
        existing_problem = await db.dsa_problems.find_one({"slug": problem_data.slug})
        if existing_problem:
            raise HTTPException(status_code=400, detail="DSA problem with this slug already exists")
        
        problem = DSAProblem(**problem_data.dict(), created_by=current_admin.username)
        problem_dict = problem.dict()
        
        result = await db.dsa_problems.insert_one(problem_dict)
        if result.inserted_id:
            return problem
        else:
            raise HTTPException(status_code=500, detail="Failed to create DSA problem")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating DSA problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/dsa-problems", response_model=List[DSAProblem])
async def get_dsa_problems_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    difficulty: Optional[DSADifficulty] = None,
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Get all DSA problems for admin with pagination and filtering"""
    try:
        db = await get_database()
        query = {}
        
        if status:
            query["status"] = status
        
        if difficulty:
            query["difficulty"] = difficulty
            
        if category_id:
            query["category_id"] = category_id
        
        if search:
            query["$text"] = {"$search": search}
        
        problems = await db.dsa_problems.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [DSAProblem(**problem) for problem in problems]
    except Exception as e:
        logger.error(f"Error fetching DSA problems: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/dsa-problems/{problem_id}", response_model=DSAProblem)
async def get_dsa_problem_admin(problem_id: str, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Get a specific DSA problem by ID for admin"""
    try:
        db = await get_database()
        problem = await db.dsa_problems.find_one({"id": problem_id})
        
        if not problem:
            raise HTTPException(status_code=404, detail="DSA problem not found")
        
        return DSAProblem(**problem)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching DSA problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.put("/dsa-problems/{problem_id}", response_model=DSAProblem)
async def update_dsa_problem(
    problem_id: str, 
    problem_update: DSAProblemUpdate, 
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Update a DSA problem"""
    try:
        db = await get_database()
        
        # Check if slug is unique (if being updated)
        if problem_update.slug:
            existing_problem = await db.dsa_problems.find_one({
                "slug": problem_update.slug, 
                "id": {"$ne": problem_id}
            })
            if existing_problem:
                raise HTTPException(status_code=400, detail="DSA problem with this slug already exists")
        
        update_data = {k: v for k, v in problem_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.dsa_problems.update_one(
            {"id": problem_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="DSA problem not found")
        
        updated_problem = await db.dsa_problems.find_one({"id": problem_id})
        return DSAProblem(**updated_problem)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating DSA problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.delete("/dsa-problems/{problem_id}")
async def delete_dsa_problem(problem_id: str, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Delete a DSA problem"""
    try:
        db = await get_database()
        result = await db.dsa_problems.delete_one({"id": problem_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="DSA problem not found")
        
        return {"message": "DSA problem deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting DSA problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Fresher Jobs Management Routes (Jobs with experience_level=fresher)
@admin_router.get("/fresher-jobs", response_model=List[Job])
async def get_fresher_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    search: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_active_admin)
):
    """Get all fresher jobs with pagination and filtering"""
    try:
        db = await get_database()
        query = {"experience_level": "fresher"}
        
        if status:
            query["status"] = status
        
        if search:
            query["$text"] = {"$search": search}
        
        jobs = await db.jobs.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [Job(**job) for job in jobs]
    except Exception as e:
        logger.error(f"Error fetching fresher jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/fresher-jobs", response_model=Job)
async def create_fresher_job(job_data: JobCreate, current_admin: AdminUser = Depends(get_current_active_admin)):
    """Create a new fresher job posting"""
    try:
        db = await get_database()
        
        # Force experience_level to fresher
        job_dict = job_data.dict()
        job_dict['experience_level'] = "fresher"
        
        # Handle skills field mapping
        if job_dict.get('skills') and not job_dict.get('skills_required'):
            job_dict['skills_required'] = job_dict['skills']
        elif not job_dict.get('skills') and job_dict.get('skills_required'):
            job_dict['skills'] = job_dict['skills_required']
        
        job = Job(**job_dict, created_by=current_admin.username)
        job_dict = job.dict()
        
        result = await db.jobs.insert_one(job_dict)
        if result.inserted_id:
            return job
        else:
            raise HTTPException(status_code=500, detail="Failed to create fresher job")
    except Exception as e:
        logger.error(f"Error creating fresher job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))