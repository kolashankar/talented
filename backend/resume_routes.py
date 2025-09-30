from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from models import (
    ResumeAnalysisRequest, ResumeAnalysisResponse, 
    ResumeParseRequest, ResumeParseResponse, User
)
from ai_service import ai_service
from user_auth import get_current_active_user
import logging
import PyPDF2
import io
import docx

logger = logging.getLogger(__name__)

# Create router for resume routes
resume_router = APIRouter(prefix="/resume", tags=["resume"])

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc_file = io.BytesIO(file_content)
        doc = docx.Document(doc_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to extract text from DOCX")

@resume_router.post("/upload-analyze", response_model=ResumeAnalysisResponse)
async def upload_and_analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(None),
    target_role: str = Form(None),
    current_user: User = Depends(get_current_active_user)
):
    """Upload resume file and analyze it using AI ATS system (requires authentication)"""
    try:
        # Validate file type
        allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
        if resume_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload PDF, DOCX, or TXT files only."
            )
        
        # Read file content
        file_content = await resume_file.read()
        
        # Extract text based on file type
        if resume_file.content_type == 'application/pdf':
            resume_text = extract_text_from_pdf(file_content)
        elif resume_file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            resume_text = extract_text_from_docx(file_content)
        else:  # text/plain
            resume_text = file_content.decode('utf-8')
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the uploaded file")
        
        # Create analysis request
        request = ResumeAnalysisRequest(
            resume_text=resume_text,
            job_description=job_description,
            target_role=target_role
        )
        
        # Analyze resume
        analysis = await ai_service.analyze_resume(request)
        
        logger.info(f"Resume analyzed for user {current_user.email}")
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing uploaded resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze resume: {str(e)}")

@resume_router.post("/analyze-text", response_model=ResumeAnalysisResponse)
async def analyze_resume_text(
    request: ResumeAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Analyze resume text using AI ATS system (requires authentication)"""
    try:
        analysis = await ai_service.analyze_resume(request)
        logger.info(f"Resume text analyzed for user {current_user.email}")
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing resume text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze resume: {str(e)}")

@resume_router.post("/parse", response_model=ResumeParseResponse)
async def parse_resume(
    request: ResumeParseRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Parse resume text into structured data for portfolio builder"""
    try:
        parsed_data = await ai_service.parse_resume(request)
        logger.info(f"Resume parsed for user {current_user.email}")
        return parsed_data
    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

@resume_router.post("/upload-parse", response_model=ResumeParseResponse)
async def upload_and_parse_resume(
    resume_file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload resume file and parse it into structured data"""
    try:
        # Validate file type
        allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
        if resume_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload PDF, DOCX, or TXT files only."
            )
        
        # Read file content
        file_content = await resume_file.read()
        
        # Extract text based on file type
        if resume_file.content_type == 'application/pdf':
            resume_text = extract_text_from_pdf(file_content)
        elif resume_file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            resume_text = extract_text_from_docx(file_content)
        else:  # text/plain
            resume_text = file_content.decode('utf-8')
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the uploaded file")
        
        # Create parse request
        request = ResumeParseRequest(resume_text=resume_text)
        
        # Parse resume
        parsed_data = await ai_service.parse_resume(request)
        
        logger.info(f"Resume uploaded and parsed for user {current_user.email}")
        return parsed_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error parsing uploaded resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")