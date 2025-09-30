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
    salary_range: Optional[str] = None
    job_type: JobType
    experience_level: ExperienceLevel
    skills_required: List[str] = []
    skills: List[str] = []  # Alternative field name for compatibility
    benefits: List[str] = []
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    is_remote: bool = False
    is_featured: bool = False
    is_active: bool = True
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
    salary_range: Optional[str] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    skills_required: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    is_remote: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
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
    duration: Optional[str] = None  # For compatibility with frontend
    duration_months: Optional[int] = None
    skills_required: List[str] = []
    skills: List[str] = []  # Alternative field name for compatibility
    benefits: List[str] = []
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    is_remote: bool = False
    is_paid: bool = False
    is_featured: bool = False
    is_active: bool = True
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
    duration: Optional[str] = None
    duration_months: Optional[int] = None
    skills_required: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    is_remote: Optional[bool] = None
    is_paid: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None
    status: Optional[ContentStatus] = None

# Article Models
class ArticleCreate(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    author: Optional[str] = None
    featured_image: Optional[str] = None
    category: str
    tags: List[str] = []
    reading_time_minutes: Optional[int] = None
    seo_meta_title: Optional[str] = None
    seo_meta_description: Optional[str] = None
    is_published: bool = False
    is_featured: bool = False
    expiration_date: Optional[datetime] = None

class Article(BaseDocument, ArticleCreate):
    views: int = 0
    likes: int = 0

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    featured_image: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    reading_time_minutes: Optional[int] = None
    seo_meta_title: Optional[str] = None
    seo_meta_description: Optional[str] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None
    expiration_date: Optional[datetime] = None
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
    expiration_date: Optional[datetime] = None

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

# User Models (for user authentication and features)
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    google_id: Optional[str] = None
    hashed_password: Optional[str] = None  # For email/password login
    name: str
    profile_picture: Optional[str] = None
    is_active: bool = True
    email_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    email: str
    google_id: Optional[str] = None
    hashed_password: Optional[str] = None
    name: str
    profile_picture: Optional[str] = None
    email_verified: bool = False

class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

# DSA Problem Models
class DSADifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class DSACategory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: Optional[str] = None
    order: int

class DSATopic(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category_id: str
    order: int

class DSAChapter(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    topic_id: str
    order: int

class DSATestCase(BaseModel):
    input: str
    expected_output: str
    explanation: Optional[str] = None

class DSAProblemCreate(BaseModel):
    title: str
    slug: str
    description: str
    difficulty: DSADifficulty
    category_id: str
    topic_id: str
    chapter_id: str
    companies: List[str] = []
    tags: List[str] = []
    constraints: List[str] = []
    examples: List[Dict[str, str]] = []
    test_cases: List[DSATestCase] = []
    hints: List[str] = []
    solution_approach: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None

class DSAProblem(BaseDocument, DSAProblemCreate):
    attempts: int = 0
    solved_count: int = 0
    success_rate: float = 0.0

class DSAProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[DSADifficulty] = None
    category_id: Optional[str] = None
    topic_id: Optional[str] = None
    chapter_id: Optional[str] = None
    companies: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    examples: Optional[List[Dict[str, str]]] = None
    test_cases: Optional[List[DSATestCase]] = None
    hints: Optional[List[str]] = None
    solution_approach: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    status: Optional[ContentStatus] = None

class DSASubmission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    problem_id: str
    user_id: str
    code: str
    language: str
    status: str  # accepted, wrong_answer, time_limit_exceeded, etc.
    execution_time: Optional[float] = None
    memory_used: Optional[int] = None
    test_cases_passed: int = 0
    total_test_cases: int = 0
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

# Portfolio Builder Models
class PortfolioTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    preview_image: str
    template_data: Dict[str, Any]  # Template structure and styling
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PersonalDetails(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio_url: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

class Education(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None
    cgpa: Optional[str] = None
    description: Optional[str] = None

class Experience(BaseModel):
    title: str
    company: str
    duration: str
    location: Optional[str] = None
    description: List[str] = []

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image: Optional[str] = None

class ParsedResumeData(BaseModel):
    personal_details: PersonalDetails
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    skills: List[str] = []
    certifications: List[str] = []
    achievements: List[str] = []

class PortfolioCreate(BaseModel):
    user_id: str
    template_id: str
    title: str
    resume_data: ParsedResumeData
    custom_prompt: Optional[str] = None
    additional_sections: Dict[str, Any] = {}

class Portfolio(BaseDocument, PortfolioCreate):
    live_url: str
    share_token: str = Field(default_factory=lambda: str(uuid.uuid4()))
    is_public: bool = True
    views: int = 0

class PortfolioUpdate(BaseModel):
    title: Optional[str] = None
    template_id: Optional[str] = None
    resume_data: Optional[ParsedResumeData] = None
    custom_prompt: Optional[str] = None
    additional_sections: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None

# Enhanced AI Models for Portfolio and Resume
class ResumeParseRequest(BaseModel):
    resume_text: str

class ResumeParseResponse(BaseModel):
    parsed_data: ParsedResumeData
    parsing_confidence: float
    suggestions: List[str] = []
    missing_sections: List[str] = []

class PortfolioGenerateRequest(BaseModel):
    template_id: str
    resume_data: ParsedResumeData
    user_prompt: str
    additional_preferences: Dict[str, Any] = {}

class PortfolioGenerateResponse(BaseModel):
    generated_content: Dict[str, Any]
    html_content: str
    css_content: str
    js_content: Optional[str] = None
    live_url: str
    share_token: str
    template_name: str
    preview_image: Optional[str] = None

# Portfolio Template Models
class PortfolioTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: str  # 'modern', 'creative', 'minimal', 'corporate', 'animated'
    difficulty: str  # 'basic', 'intermediate', 'advanced'
    features: List[str] = []  # ['3d-effects', 'animations', 'dark-mode', 'responsive']
    preview_image: str
    html_template: str
    css_template: str
    js_template: Optional[str] = None
    variables: Dict[str, Any] = {}  # Template variables for customization
    created_at: datetime = Field(default_factory=datetime.utcnow)

# AI Form Filler Models
class AIFormFillerRequest(BaseModel):
    content_type: str  # 'job', 'internship', 'article', 'roadmap', 'dsa'
    user_prompt: str
    context_data: Optional[Dict[str, Any]] = {}
    generate_images: bool = True
    generate_logos: bool = True
    
class AIFormFillerResponse(BaseModel):
    form_data: Dict[str, Any]
    generated_images: Dict[str, str] = {}  # field_name -> image_url
    generated_logos: Dict[str, str] = {}   # field_name -> logo_url
    confidence_score: float
    suggestions: List[str] = []

# Image Generation Models
class ImageGenerationRequest(BaseModel):
    prompt: str
    style: str = "professional"  # 'professional', 'creative', 'minimal', 'corporate'
    size: str = "1024x1024"
    quality: str = "standard"
    
class ImageGenerationResponse(BaseModel):
    image_url: str
    prompt_used: str
    generation_time: float
    
# Enhanced Resume Analysis
class EnhancedResumeAnalysis(BaseModel):
    ats_score: float
    keyword_density: Dict[str, float]
    section_completeness: Dict[str, float]
    formatting_issues: List[str] = []
    improvement_suggestions: List[str] = []
    skill_gaps: List[str] = []
    career_recommendations: List[str] = []

# User Interaction Models
class UserInteraction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    content_type: str  # 'article', 'job', 'internship', 'roadmap', 'dsa_problem'
    content_id: str
    interaction_type: str  # 'like', 'save', 'share', 'view', 'apply'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}  # Additional data like share platform, etc.

class DSAUserProgress(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    problem_id: str
    status: str  # 'not_attempted', 'in_progress', 'solved', 'reviewed'
    attempts: int = 0
    best_solution: Optional[str] = None
    best_language: Optional[str] = None
    time_spent: int = 0  # in minutes
    last_attempted: datetime = Field(default_factory=datetime.utcnow)
    solved_at: Optional[datetime] = None
    
class DSADiscussion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    problem_id: str
    user_id: str
    user_name: str
    content: str
    is_solution: bool = False
    parent_id: Optional[str] = None  # For replies
    likes: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CompanyProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    logo_url: Optional[str] = None
    description: str
    website: Optional[str] = None
    industry: str
    size: Optional[str] = None  # '1-10', '11-50', '51-200', etc.
    location: str
    founded_year: Optional[int] = None
    social_links: Dict[str, str] = {}  # linkedin, twitter, etc.
    job_count: int = 0
    internship_count: int = 0
    rating: float = 0.0
    review_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Footer Page Models
class FooterPage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    content: str
    meta_description: Optional[str] = None
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Response Models for User Interactions
class LikeResponse(BaseModel):
    liked: bool
    total_likes: int

class SaveResponse(BaseModel):
    saved: bool
    message: str

class ShareResponse(BaseModel):
    share_url: str
    message: str