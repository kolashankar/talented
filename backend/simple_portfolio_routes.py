from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Optional, Dict, Any
from database import get_database
from user_auth import get_current_active_user
from models import User
import logging
import uuid
from datetime import datetime
import json
import re

logger = logging.getLogger(__name__)

# Create router for enhanced portfolio routes
enhanced_portfolio_router = APIRouter(prefix="/enhanced-portfolio", tags=["enhanced-portfolio"])

class SimplePortfolioTemplateService:
    """Simple Portfolio Template Service with 5 complete templates"""

    def __init__(self):
        self.templates = self._create_all_templates()

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates"""
        return list(self.templates.values())

    def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template by ID"""
        return self.templates.get(template_id)

    def _create_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create all 5 portfolio templates"""
        return {
            "modern-professional": self._create_modern_professional(),
            "creative-designer": self._create_creative_designer(),
            "tech-developer": self._create_tech_developer(),
            "minimal-clean": self._create_minimal_clean(),
            "corporate-executive": self._create_corporate_executive()
        }

    def _create_modern_professional(self) -> Dict[str, Any]:
        """Modern Professional Template"""
        return {
            "id": "modern-professional",
            "name": "Modern Professional",
            "description": "Clean, modern design perfect for professionals and consultants",
            "category": "professional",
            "preview_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop",
            "features": ["responsive", "dark-mode", "animations", "contact-form"],
            "difficulty": "beginner",
            "color_scheme": {
                "primary": "#2563eb",
                "secondary": "#1e293b",
                "accent": "#10b981",
                "background": "#ffffff",
                "text": "#1f2937"
            },
            "sections": ["hero", "about", "experience", "skills", "projects", "contact"],
            "html_template": self._get_modern_professional_html(),
            "css_template": self._get_modern_professional_css(),
            "js_template": self._get_modern_professional_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_creative_designer(self) -> Dict[str, Any]:
        """Creative Designer Template"""
        return {
            "id": "creative-designer",
            "name": "Creative Designer",
            "description": "Vibrant and artistic design for creative professionals",
            "category": "creative",
            "preview_image": "https://images.unsplash.com/photo-1558655146-364adaf1fcc9?w=800&h=600&fit=crop",
            "features": ["animations", "portfolio-filters", "colorful", "parallax"],
            "difficulty": "intermediate",
            "color_scheme": {
                "primary": "#ff6b6b",
                "secondary": "#4ecdc4",
                "accent": "#45b7d1",
                "background": "#f8f9fa",
                "text": "#2d3436"
            },
            "sections": ["hero", "about", "portfolio", "services", "testimonials", "contact"],
            "html_template": self._get_creative_designer_html(),
            "css_template": self._get_creative_designer_css(),
            "js_template": self._get_creative_designer_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_tech_developer(self) -> Dict[str, Any]:
        """Tech Developer Template"""
        return {
            "id": "tech-developer",
            "name": "Tech Developer",
            "description": "Dark-themed design perfect for developers and engineers",
            "category": "technology",
            "preview_image": "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=800&h=600&fit=crop",
            "features": ["dark-theme", "code-snippets", "github-integration", "terminal-style"],
            "difficulty": "advanced",
            "color_scheme": {
                "primary": "#00ff88",
                "secondary": "#1a1a1a",
                "accent": "#ff0088",
                "background": "#0d1117",
                "text": "#ffffff"
            },
            "sections": ["hero", "about", "skills", "projects", "experience", "contact"],
            "html_template": self._get_tech_developer_html(),
            "css_template": self._get_tech_developer_css(),
            "js_template": self._get_tech_developer_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_minimal_clean(self) -> Dict[str, Any]:
        """Minimal Clean Template"""
        return {
            "id": "minimal-clean",
            "name": "Minimal Clean",
            "description": "Clean minimal design focusing on content and readability",
            "category": "minimal",
            "preview_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
            "features": ["minimal-design", "typography-focused", "fast-loading"],
            "difficulty": "beginner",
            "color_scheme": {
                "primary": "#374151",
                "secondary": "#9ca3af",
                "accent": "#6366f1",
                "background": "#ffffff",
                "text": "#111827"
            },
            "sections": ["hero", "about", "work", "writing", "contact"],
            "html_template": self._get_minimal_clean_html(),
            "css_template": self._get_minimal_clean_css(),
            "js_template": self._get_minimal_clean_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_corporate_executive(self) -> Dict[str, Any]:
        """Corporate Executive Template"""
        return {
            "id": "corporate-executive",
            "name": "Corporate Executive",
            "description": "Professional design for executives and business leaders",
            "category": "corporate",
            "preview_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
            "features": ["professional", "testimonials", "achievements", "business-focused"],
            "difficulty": "intermediate",
            "color_scheme": {
                "primary": "#1d4ed8",
                "secondary": "#475569",
                "accent": "#059669",
                "background": "#ffffff",
                "text": "#1e293b"
            },
            "sections": ["hero", "about", "experience", "achievements", "testimonials", "contact"],
            "html_template": self._get_corporate_executive_html(),
            "css_template": self._get_corporate_executive_css(),
            "js_template": self._get_corporate_executive_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _get_modern_professional_html(self) -> str:
        """Modern Professional HTML Template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{full_name}} - {{title}}</title>
    <meta name="description" content="{{summary}}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{css}}</style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">{{full_name}}</div>
            <div class="nav-menu">
                <a href="#home" class="nav-link active">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">{{full_name}}</h1>
                <h2 class="hero-subtitle">{{title}}</h2>
                <p class="hero-description">{{summary}}</p>
                <div class="hero-buttons">
                    <a href="#contact" class="btn btn-primary">Get In Touch</a>
                    <a href="#projects" class="btn btn-secondary">View My Work</a>
                </div>
            </div>
            <div class="hero-image">
                <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face" alt="{{full_name}}" class="profile-img">
            </div>
        </div>
    </section>

    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <p class="about-description">{{about_me}}</p>
                <div class="about-stats">
                    <div class="stat-item">
                        <span class="stat-number">50+</span>
                        <span class="stat-label">Projects</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">{{years_experience}}+</span>
                        <span class="stat-label">Years</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">30+</span>
                        <span class="stat-label">Clients</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">Projects</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-image">
                        <img src="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=500&h=300&fit=crop" alt="Project 1">
                    </div>
                    <div class="project-content">
                        <h3 class="project-title">Sample Project</h3>
                        <p class="project-description">A great project description</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Contact</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <p>Email: {{email}}</p>
                    <p>Phone: {{phone}}</p>
                    <p>Location: {{location}}</p>
                </div>
                <form class="contact-form">
                    <input type="text" placeholder="Name" required>
                    <input type="email" placeholder="Email" required>
                    <textarea placeholder="Message" required></textarea>
                    <button type="submit">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 {{full_name}}. All rights reserved.</p>
        </div>
    </footer>

    <script>{{js}}</script>
</body>
</html>"""

    def _get_modern_professional_css(self) -> str:
        """Modern Professional CSS"""
        return """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; line-height: 1.6; color: #1f2937; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }

/* Navigation */
.navbar { position: fixed; top: 0; width: 100%; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); z-index: 1000; }
.nav-container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; display: flex; justify-content: space-between; align-items: center; height: 70px; }
.nav-logo { font-size: 1.5rem; font-weight: 700; color: #2563eb; }
.nav-menu { display: flex; gap: 2rem; }
.nav-link { text-decoration: none; color: #1f2937; font-weight: 500; transition: color 0.3s; }
.nav-link:hover, .nav-link.active { color: #2563eb; }

/* Hero Section */
.hero { min-height: 100vh; display: flex; align-items: center; padding-top: 70px; background: linear-gradient(135deg, #ffffff 0%, rgba(37, 99, 235, 0.05) 100%); }
.hero-container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }
.hero-title { font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem; background: linear-gradient(135deg, #2563eb, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { font-size: 1.5rem; color: #6b7280; margin-bottom: 1.5rem; }
.hero-description { font-size: 1.1rem; color: #6b7280; margin-bottom: 2rem; line-height: 1.8; }
.hero-buttons { display: flex; gap: 1rem; margin-bottom: 2rem; }
.btn { padding: 0.75rem 2rem; border: none; border-radius: 0.5rem; font-weight: 600; text-decoration: none; cursor: pointer; transition: all 0.3s; display: inline-flex; align-items: center; gap: 0.5rem; font-family: inherit; }
.btn-primary { background: #2563eb; color: white; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
.btn-secondary { background: transparent; color: #2563eb; border: 2px solid #2563eb; }
.btn-secondary:hover { background: #2563eb; color: white; }
.profile-img { width: 100%; max-width: 400px; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }

/* Section Styles */
.section-title { font-size: 2.5rem; font-weight: 700; margin-bottom: 3rem; text-align: center; position: relative; }
.section-title::after { content: ''; position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); width: 50px; height: 3px; background: #10b981; }

/* About Section */
.about { padding: 6rem 0; background: rgba(37, 99, 235, 0.03); }
.about-description { font-size: 1.1rem; line-height: 1.8; margin-bottom: 3rem; text-align: center; max-width: 800px; margin-left: auto; margin-right: auto; }
.about-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; max-width: 600px; margin: 0 auto; }
.stat-item { text-align: center; }
.stat-number { display: block; font-size: 2rem; font-weight: 700; color: #2563eb; margin-bottom: 0.5rem; }
.stat-label { color: #6b7280; font-size: 0.9rem; }

/* Projects Section */
.projects { padding: 6rem 0; }
.projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; }
.project-card { background: white; border-radius: 1rem; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); transition: all 0.3s; }
.project-card:hover { transform: translateY(-10px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); }
.project-image { height: 200px; overflow: hidden; }
.project-image img { width: 100%; height: 100%; object-fit: cover; }
.project-content { padding: 2rem; }
.project-title { font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem; }
.project-description { color: #6b7280; line-height: 1.6; }

/* Contact Section */
.contact { padding: 6rem 0; background: rgba(37, 99, 235, 0.03); }
.contact-content { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; max-width: 800px; margin: 0 auto; }
.contact-info p { margin-bottom: 1rem; font-size: 1.1rem; }
.contact-form { display: flex; flex-direction: column; gap: 1rem; }
.contact-form input, .contact-form textarea { padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-family: inherit; font-size: 1rem; transition: border-color 0.3s; }
.contact-form input:focus, .contact-form textarea:focus { outline: none; border-color: #2563eb; }
.contact-form button { padding: 1rem; background: #2563eb; color: white; border: none; border-radius: 0.5rem; cursor: pointer; font-weight: 600; transition: all 0.3s; }
.contact-form button:hover { background: #1d4ed8; }

/* Footer */
.footer { background: #1e293b; color: white; padding: 2rem 0; text-align: center; }

/* Responsive Design */
@media (max-width: 768px) {
    .nav-menu { display: none; }
    .hero-container { grid-template-columns: 1fr; text-align: center; }
    .hero-title { font-size: 2.5rem; }
    .about-stats { grid-template-columns: 1fr; gap: 1rem; }
    .contact-content { grid-template-columns: 1fr; gap: 2rem; }
}
"""

    def _get_modern_professional_js(self) -> str:
        """Modern Professional JavaScript"""
        return """
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Active navigation link highlighting
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === \`#\${current}\`) {
                link.classList.add('active');
            }
        });
    });

    // Contact form handling
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Thank you for your message! I will get back to you soon.');
            this.reset();
        });
    }
});
"""

    def _get_creative_designer_html(self) -> str:
        return """<!DOCTYPE html>
<html><head><title>{{full_name}} - Creative</title><style>{{css}}</style></head>
<body><h1>{{full_name}}</h1><p>{{summary}}</p><script>{{js}}</script></body></html>"""

    def _get_creative_designer_css(self) -> str:
        return """body { font-family: 'Poppins', sans-serif; color: #2d3436; background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 0; }
h1 { font-size: 3rem; color: white; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
p { font-size: 1.2rem; color: white; text-align: center; max-width: 600px; line-height: 1.6; }"""

    def _get_creative_designer_js(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() { console.log('Creative template loaded'); });"""

    def _get_tech_developer_html(self) -> str:
        return """<!DOCTYPE html>
<html><head><title>{{full_name}} - Developer</title><style>{{css}}</style></head>
<body><div class="terminal"><div class="terminal-header">{{full_name}}@portfolio:~$</div>
<div class="terminal-body"><p>&gt; whoami</p><p>{{full_name}} - {{title}}</p><p>&gt; cat about.txt</p><p>{{summary}}</p></div></div>
<script>{{js}}</script></body></html>"""

    def _get_tech_developer_css(self) -> str:
        return """body { font-family: 'Fira Code', monospace; background: #0d1117; color: #c9d1d9; margin: 0; padding: 2rem; }
.terminal { background: #161b22; border: 1px solid #30363d; border-radius: 0.5rem; max-width: 800px; margin: 2rem auto; }
.terminal-header { background: #21262d; padding: 1rem; border-bottom: 1px solid #30363d; color: #00ff88; font-weight: bold; }
.terminal-body { padding: 2rem; line-height: 1.8; } .terminal-body p { margin: 0.5rem 0; }"""

    def _get_tech_developer_js(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() { console.log('Tech template loaded'); });"""

    def _get_minimal_clean_html(self) -> str:
        return """<!DOCTYPE html>
<html><head><title>{{full_name}}</title><style>{{css}}</style></head>
<body><main><section class="hero"><div class="container"><h1>{{full_name}}</h1><p class="lead">{{title}}</p><p>{{summary}}</p></div></section>
<section class="about"><div class="container"><h2>About</h2><p>{{about_me}}</p></div></section>
<section class="contact"><div class="container"><h2>Contact</h2><p>{{email}}</p></div></section></main>
<script>{{js}}</script></body></html>"""

    def _get_minimal_clean_css(self) -> str:
        return """body { font-family: 'Inter', sans-serif; line-height: 1.6; color: #111827; margin: 0; }
.container { max-width: 800px; margin: 0 auto; padding: 0 2rem; }
.hero { padding: 4rem 0; } .hero h1 { font-size: 3rem; font-weight: 300; margin-bottom: 0.5rem; }
.lead { font-size: 1.25rem; color: #6b7280; margin-bottom: 2rem; }
.about, .contact { padding: 3rem 0; border-top: 1px solid #e5e7eb; }
h2 { font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; }"""

    def _get_minimal_clean_js(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() { console.log('Minimal template loaded'); });"""

    def _get_corporate_executive_html(self) -> str:
        return """<!DOCTYPE html>
<html><head><title>{{full_name}} - Executive</title><style>{{css}}</style></head>
<body><header class="header"><div class="container"><h1>{{full_name}}</h1><h2>{{title}}</h2></div></header>
<main><section class="summary"><div class="container"><p>{{summary}}</p></div></section>
<section class="contact"><div class="container"><h3>Contact Information</h3><p>Email: {{email}}</p><p>Phone: {{phone}}</p></div></section></main>
<script>{{js}}</script></body></html>"""

    def _get_corporate_executive_css(self) -> str:
        return """body { font-family: 'Inter', sans-serif; color: #1e293b; margin: 0; line-height: 1.6; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 2rem; }
.header { background: linear-gradient(135deg, #1d4ed8 0%, #059669 100%); color: white; padding: 4rem 0; text-align: center; }
.header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; } .header h2 { font-size: 1.3rem; opacity: 0.9; }
.summary, .contact { padding: 3rem 0; } .summary p { font-size: 1.1rem; text-align: center; max-width: 700px; margin: 0 auto; }"""

    def _get_corporate_executive_js(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() { console.log('Corporate template loaded'); });"""

# Initialize template service
template_service = SimplePortfolioTemplateService()

@enhanced_portfolio_router.get("/templates")
async def get_enhanced_portfolio_templates():
    """Get all enhanced portfolio templates"""
    try:
        templates = template_service.get_all_templates()
        return JSONResponse(content={"templates": templates, "count": len(templates)})
    except Exception as e:
        logger.error(f"Error fetching enhanced templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch enhanced templates")

@enhanced_portfolio_router.get("/templates/{template_id}")
async def get_enhanced_template_by_id(template_id: str):
    """Get a specific enhanced template by ID"""
    try:
        template = template_service.get_template_by_id(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return JSONResponse(content=template)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching template {template_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch template")

@enhanced_portfolio_router.post("/generate")
async def generate_enhanced_portfolio(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_active_user)
):
    """Generate portfolio using enhanced templates"""
    try:
        template_id = request.get("template_id")
        resume_data = request.get("resume_data", {})

        if not template_id:
            raise HTTPException(status_code=400, detail="Template ID is required")

        template = template_service.get_template_by_id(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

        # Generate portfolio HTML by replacing placeholders
        html_content = template["html_template"]
        css_content = template["css_template"]
        js_content = template["js_template"]

        # Replace CSS and JS placeholders
        html_content = html_content.replace("{{css}}", css_content)
        html_content = html_content.replace("{{js}}", js_content)

        # Replace user data placeholders with safe defaults
        replacements = {
            "full_name": resume_data.get("full_name", "Your Name"),
            "title": resume_data.get("title", "Professional Title"),
            "email": resume_data.get("email", "your.email@example.com"),
            "phone": resume_data.get("phone", "+1 (555) 123-4567"),
            "location": resume_data.get("location", "Your Location"),
            "summary": resume_data.get("summary", "Professional summary goes here."),
            "about_me": resume_data.get("about_me", "Tell people about yourself here."),
            "years_experience": str(resume_data.get("years_experience", "5")),
            "linkedin_url": resume_data.get("linkedin_url", "#"),
            "github_url": resume_data.get("github_url", "#")
        }

        # Apply replacements
        for key, value in replacements.items():
            placeholder = f"{{{{{key}}}}}"
            html_content = html_content.replace(placeholder, str(value))

        # Generate unique share token
        share_token = str(uuid.uuid4())

        # Save to database
        db = await get_database()
        portfolio_data = {
            "id": str(uuid.uuid4()),
            "user_id": current_user.id,
            "template_id": template_id,
            "title": f"{replacements['full_name']} - Portfolio",
            "html_content": html_content,
            "share_token": share_token,
            "is_public": True,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await db.portfolios.insert_one(portfolio_data)

        return JSONResponse(content={
            "success": True,
            "portfolio_id": portfolio_data["id"],
            "live_url": f"/api/portfolio/view/{share_token}",
            "share_token": share_token,
            "template_used": template["name"]
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating enhanced portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate portfolio")

@enhanced_portfolio_router.get("/view/{share_token}", response_class=HTMLResponse)
async def view_enhanced_portfolio(share_token: str):
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

        return HTMLResponse(content=portfolio["html_content"])

    except Exception as e:
        logger.error(f"Error viewing portfolio: {str(e)}")
        return HTMLResponse(content="<h1>Error loading portfolio</h1>", status_code=500)
