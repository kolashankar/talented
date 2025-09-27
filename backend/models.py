from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum

class JobType(str, Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"

class ExperienceLevel(str, Enum):
    FRESHER = "fresher"
    EXPERIENCED = "experienced"
    SENIOR = "senior"

class ContentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

# Base Models
class BaseDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(default="admin")
    status: ContentStatus = ContentStatus.DRAFT

# Job Models
class JobCreate(BaseModel):
    title: str
    company: str
    company_logo: Optional[str] = None
    description: str
    requirements: List[str] = []
    responsibilities: List[str] = []
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "INR"
    job_type: JobType
    experience_level: ExperienceLevel
    skills_required: List[str] = []
    benefits: List[str] = []
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    is_remote: bool = False
    tags: List[str] = []

class Job(BaseDocument, JobCreate):
    views: int = 0
    applications: int = 0

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_logo: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    responsibilities: Optional[List[str]] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    skills_required: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    is_remote: Optional[bool] = None
    tags: Optional[List[str]] = None
    status: Optional[ContentStatus] = None

# Internship Models  
class InternshipCreate(BaseModel):
    title: str
    company: str
    company_logo: Optional[str] = None
    description: str
    requirements: List[str] = []
    responsibilities: List[str] = []
    location: str
    stipend: Optional[int] = None
    duration_months: int
    skills_required: List[str] = []
    benefits: List[str] = []
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    is_remote: bool = False
    tags: List[str] = []

class Internship(BaseDocument, InternshipCreate):
    views: int = 0
    applications: int = 0

class InternshipUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_logo: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    responsibilities: Optional[List[str]] = None
    location: Optional[str] = None
    stipend: Optional[int] = None
    duration_months: Optional[int] = None
    skills_required: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    is_remote: Optional[bool] = None
    tags: Optional[List[str]] = None
    status: Optional[ContentStatus] = None

# Article Models
class ArticleCreate(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    featured_image: Optional[str] = None
    category: str
    tags: List[str] = []
    reading_time_minutes: Optional[int] = None
    seo_meta_title: Optional[str] = None
    seo_meta_description: Optional[str] = None

class Article(BaseDocument, ArticleCreate):
    views: int = 0
    likes: int = 0

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    reading_time_minutes: Optional[int] = None
    seo_meta_title: Optional[str] = None
    seo_meta_description: Optional[str] = None
    status: Optional[ContentStatus] = None

# Roadmap Models
class RoadmapStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    resources: List[str] = []
    estimated_duration: Optional[str] = None
    prerequisites: List[str] = []
    order: int

class RoadmapCreate(BaseModel):
    title: str
    slug: str
    description: str
    featured_image: Optional[str] = None
    difficulty_level: str  # beginner, intermediate, advanced
    estimated_completion_time: Optional[str] = None
    tags: List[str] = []
    steps: List[RoadmapStep] = []
    prerequisites: List[str] = []

class Roadmap(BaseDocument, RoadmapCreate):
    views: int = 0
    enrollments: int = 0

class RoadmapUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    featured_image: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_completion_time: Optional[str] = None
    tags: Optional[List[str]] = None
    steps: Optional[List[RoadmapStep]] = None
    prerequisites: Optional[List[str]] = None
    status: Optional[ContentStatus] = None

# Admin User Models
class AdminUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminCreate(BaseModel):
    username: str
    email: str
    password: str
    is_superuser: bool = False

# AI Content Generation Models
class AIContentRequest(BaseModel):
    content_type: str  # job, internship, article, roadmap
    prompt: str
    additional_context: Optional[Dict[str, Any]] = {}

class AIContentResponse(BaseModel):
    content: Dict[str, Any]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    tokens_used: Optional[int] = None

# Resume ATS Models
class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None
    target_role: Optional[str] = None

class ResumeAnalysisResponse(BaseModel):
    overall_score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    keyword_match_score: float
    skills_analysis: Dict[str, Any]
    experience_analysis: Dict[str, Any]
    education_analysis: Dict[str, Any]
    formatting_score: float
    recommendations: List[str]
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)

# Statistics Models
class DashboardStats(BaseModel):
    total_jobs: int
    total_internships: int
    total_articles: int
    total_roadmaps: int
    total_views: int
    total_applications: int
    recent_activity: List[Dict[str, Any]]
    popular_content: List[Dict[str, Any]]