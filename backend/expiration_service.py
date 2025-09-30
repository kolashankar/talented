import asyncio
import logging
from datetime import datetime, timedelta
from database import get_database
from models import ContentStatus

logger = logging.getLogger(__name__)

class ExpirationService:
    """Service to handle automatic expiration of jobs and internships"""
    
    def __init__(self):
        self.check_interval = 3600  # Check every hour
        
    async def check_and_expire_content(self):
        """Check and expire jobs, internships, and articles past their deadline"""
        try:
            db = await get_database()
            current_time = datetime.utcnow()
            
            # Find and expire jobs by application deadline
            expired_jobs_deadline = await db.jobs.update_many(
                {
                    "application_deadline": {"$lt": current_time},
                    "status": {"$ne": ContentStatus.ARCHIVED}
                },
                {
                    "$set": {
                        "status": ContentStatus.ARCHIVED,
                        "updated_at": current_time,
                        "archived_reason": "Expired - Application deadline passed"
                    }
                }
            )
            
            # Find and expire jobs by expiration date (delete from database)
            expired_jobs_expiration = await db.jobs.delete_many(
                {
                    "expiration_date": {"$lt": current_time}
                }
            )
            
            # Find and expire internships by application deadline
            expired_internships_deadline = await db.internships.update_many(
                {
                    "application_deadline": {"$lt": current_time},
                    "status": {"$ne": ContentStatus.ARCHIVED}
                },
                {
                    "$set": {
                        "status": ContentStatus.ARCHIVED,
                        "updated_at": current_time,
                        "archived_reason": "Expired - Application deadline passed"
                    }
                }
            )
            
            # Find and expire internships by expiration date (delete from database)
            expired_internships_expiration = await db.internships.delete_many(
                {
                    "expiration_date": {"$lt": current_time}
                }
            )
            
            # Find and expire articles by expiration date (delete from database)
            expired_articles_expiration = await db.articles.delete_many(
                {
                    "expiration_date": {"$lt": current_time}
                }
            )
            
            # Find and expire roadmaps by expiration date (delete from database)
            expired_roadmaps_expiration = await db.roadmaps.delete_many(
                {
                    "expiration_date": {"$lt": current_time}
                }
            )
            
            total_expired_jobs = expired_jobs_deadline.modified_count
            total_deleted_jobs = expired_jobs_expiration.deleted_count
            total_expired_internships = expired_internships_deadline.modified_count
            total_deleted_internships = expired_internships_expiration.deleted_count
            total_deleted_articles = expired_articles_expiration.deleted_count
            total_deleted_roadmaps = expired_roadmaps_expiration.deleted_count
            
            if total_expired_jobs > 0:
                logger.info(f"Archived {total_expired_jobs} jobs due to application deadline")
                
            if total_deleted_jobs > 0:
                logger.info(f"Deleted {total_deleted_jobs} jobs due to expiration date")
                
            if total_expired_internships > 0:
                logger.info(f"Archived {total_expired_internships} internships due to application deadline")
                
            if total_deleted_internships > 0:
                logger.info(f"Deleted {total_deleted_internships} internships due to expiration date")
                
            if total_deleted_articles > 0:
                logger.info(f"Deleted {total_deleted_articles} articles due to expiration date")
                
            if total_deleted_roadmaps > 0:
                logger.info(f"Deleted {total_deleted_roadmaps} roadmaps due to expiration date")
                
            return {
                "expired_jobs": total_expired_jobs,
                "deleted_jobs": total_deleted_jobs,
                "expired_internships": total_expired_internships,
                "deleted_internships": total_deleted_internships,
                "deleted_articles": total_deleted_articles,
                "deleted_roadmaps": total_deleted_roadmaps
            }
            
        except Exception as e:
            logger.error(f"Error checking content expiration: {str(e)}")
            return {"error": str(e)}
    
    async def start_expiration_checker(self):
        """Start the background task to check for expired content"""
        while True:
            try:
                await self.check_and_expire_content()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in expiration checker: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

# Global expiration service instance
expiration_service = ExpirationService()

async def start_expiration_service():
    """Start the expiration service"""
    logger.info("Starting expiration service...")
    asyncio.create_task(expiration_service.start_expiration_checker())

async def check_expired_content():
    """Manual function to check and expire content immediately"""
    return await expiration_service.check_and_expire_content()