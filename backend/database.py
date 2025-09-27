from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    db = None

# Database instance
database = Database()

async def get_database():
    return database.db

async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    database.db = database.client[os.getenv("DB_NAME")]
    
    # Create indexes for better performance
    await create_indexes()
    
    print("Connected to MongoDB")

async def close_mongo_connection():
    """Close database connection"""
    database.client.close()
    print("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for optimal performance"""
    db = database.db
    
    # Jobs collection indexes
    await db.jobs.create_indexes([
        IndexModel([("title", TEXT), ("company", TEXT), ("description", TEXT)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("experience_level", ASCENDING)]),
        IndexModel([("location", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([("job_type", ASCENDING)]),
        IndexModel([("skills_required", ASCENDING)]),
        IndexModel([("tags", ASCENDING)])
    ])
    
    # Internships collection indexes
    await db.internships.create_indexes([
        IndexModel([("title", TEXT), ("company", TEXT), ("description", TEXT)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("location", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([("duration_months", ASCENDING)]),
        IndexModel([("skills_required", ASCENDING)]),
        IndexModel([("tags", ASCENDING)])
    ])
    
    # Articles collection indexes
    await db.articles.create_indexes([
        IndexModel([("title", TEXT), ("content", TEXT), ("excerpt", TEXT)]),
        IndexModel([("slug", ASCENDING)], unique=True),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("category", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([("tags", ASCENDING)])
    ])
    
    # Roadmaps collection indexes
    await db.roadmaps.create_indexes([
        IndexModel([("title", TEXT), ("description", TEXT)]),
        IndexModel([("slug", ASCENDING)], unique=True),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("difficulty_level", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([("tags", ASCENDING)])
    ])
    
    # Admin users collection indexes
    await db.admin_users.create_indexes([
        IndexModel([("username", ASCENDING)], unique=True),
        IndexModel([("email", ASCENDING)], unique=True),
        IndexModel([("is_active", ASCENDING)])
    ])
    
    print("Database indexes created successfully")