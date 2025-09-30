from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from typing import List, Optional, Dict, Any
from database import get_database
from auth import get_current_active_admin
from models import AdminUser
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

# Create router for template routes
template_router = APIRouter(prefix="/templates", tags=["templates"])

class PortfolioTemplateManager:
    """Manager for portfolio templates"""

    def __init__(self):
        self.templates = self._create_all_templates()

    def _create_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create all 5 portfolio templates"""
        return {
            "modern-professional": self._create_modern_professional_template(),
            "creative-designer": self._create_creative_designer_template(),
            "tech-developer": self._create_tech_developer_template(),
            "minimal-clean": self._create_minimal_clean_template(),
            "corporate-executive": self._create_corporate_executive_template()
        }

    def _create_modern_professional_template(self) -> Dict[str, Any]:
        """Modern Professional Template"""
        return {
            "id": "modern-professional",
            "name": "Modern Professional",
            "description": "Clean, modern design perfect for professionals and consultants",
            "category": "professional",
            "preview_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop",
            "preview_url": "/templates/preview/modern-professional",
            "features": ["responsive", "animations", "dark-mode", "contact-form", "portfolio-gallery"],
            "color_scheme": {
                "primary": "#2563eb",
                "secondary": "#1e293b",
                "accent": "#10b981",
                "background": "#ffffff",
                "text": "#1f2937"
            },
            "sections": ["hero", "about", "experience", "skills", "projects", "testimonials", "contact"],
            "difficulty": "intermediate",
            "html_template": self._get_modern_professional_html(),
            "css_template": self._get_modern_professional_css(),
            "js_template": self._get_modern_professional_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_creative_designer_template(self) -> Dict[str, Any]:
        """Creative Designer Template"""
        return {
            "id": "creative-designer",
            "name": "Creative Designer",
            "description": "Vibrant and creative design perfect for designers and artists",
            "category": "creative",
            "preview_image": "https://images.unsplash.com/photo-1558655146-364adaf1fcc9?w=800&h=600&fit=crop",
            "preview_url": "/templates/preview/creative-designer",
            "features": ["animations", "parallax", "colorful", "artistic", "portfolio-filters"],
            "color_scheme": {
                "primary": "#ff6b6b",
                "secondary": "#4ecdc4",
                "accent": "#45b7d1",
                "background": "#f8f9fa",
                "text": "#2d3436"
            },
            "sections": ["hero", "about", "portfolio", "services", "testimonials", "contact"],
            "difficulty": "advanced",
            "html_template": self._get_creative_designer_html(),
            "css_template": self._get_creative_designer_css(),
            "js_template": self._get_creative_designer_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_tech_developer_template(self) -> Dict[str, Any]:
        """Tech Developer Template"""
        return {
            "id": "tech-developer",
            "name": "Tech Developer",
            "description": "Modern tech-focused design for developers and engineers",
            "category": "technology",
            "preview_image": "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=800&h=600&fit=crop",
            "preview_url": "/templates/preview/tech-developer",
            "features": ["dark-theme", "code-snippets", "terminal-style", "tech-icons", "github-integration"],
            "color_scheme": {
                "primary": "#00ff88",
                "secondary": "#1a1a1a",
                "accent": "#ff0088",
                "background": "#0d1117",
                "text": "#ffffff"
            },
            "sections": ["hero", "about", "skills", "projects", "experience", "blog", "contact"],
            "difficulty": "advanced",
            "html_template": self._get_tech_developer_html(),
            "css_template": self._get_tech_developer_css(),
            "js_template": self._get_tech_developer_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_minimal_clean_template(self) -> Dict[str, Any]:
        """Minimal Clean Template"""
        return {
            "id": "minimal-clean",
            "name": "Minimal Clean",
            "description": "Clean minimal design focusing on content and readability",
            "category": "minimal",
            "preview_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
            "preview_url": "/templates/preview/minimal-clean",
            "features": ["minimal-design", "typography-focused", "fast-loading", "print-friendly"],
            "color_scheme": {
                "primary": "#374151",
                "secondary": "#9ca3af",
                "accent": "#6366f1",
                "background": "#ffffff",
                "text": "#111827"
            },
            "sections": ["hero", "about", "work", "writing", "contact"],
            "difficulty": "beginner",
            "html_template": self._get_minimal_clean_html(),
            "css_template": self._get_minimal_clean_css(),
            "js_template": self._get_minimal_clean_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _create_corporate_executive_template(self) -> Dict[str, Any]:
        """Corporate Executive Template"""
        return {
            "id": "corporate-executive",
            "name": "Corporate Executive",
            "description": "Professional corporate design for executives and business leaders",
            "category": "corporate",
            "preview_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
            "preview_url": "/templates/preview/corporate-executive",
            "features": ["professional", "business-focused", "testimonials", "achievements", "linkedin-integration"],
            "color_scheme": {
                "primary": "#1d4ed8",
                "secondary": "#475569",
                "accent": "#059669",
                "background": "#ffffff",
                "text": "#1e293b"
            },
            "sections": ["hero", "about", "experience", "achievements", "leadership", "testimonials", "contact"],
            "difficulty": "intermediate",
            "html_template": self._get_corporate_executive_html(),
            "css_template": self._get_corporate_executive_css(),
            "js_template": self._get_corporate_executive_js(),
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _get_modern_professional_html(self) -> str:
        """Modern Professional HTML Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{full_name}} - {{professional_title}}</title>
    <meta name="description" content="{{summary}}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{css}}</style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">{{full_name}}</div>
            <div class="nav-menu" id="nav-menu">
                <a href="#home" class="nav-link">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#contact" class="nav-link">Contact</a>
                <div class="theme-toggle" id="theme-toggle">
                    <i class="fas fa-moon"></i>
                </div>
            </div>
            <div class="nav-toggle" id="nav-toggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">{{full_name}}</h1>
                <h2 class="hero-subtitle">{{professional_title}}</h2>
                <p class="hero-description">{{summary}}</p>
                <div class="hero-buttons">
                    <a href="#contact" class="btn btn-primary">Get In Touch</a>
                    <a href="#" class="btn btn-secondary">Download CV</a>
                </div>
                <div class="hero-social">
                    {{#if linkedin_url}}
                    <a href="{{linkedin_url}}" target="_blank" class="social-link">
                        <i class="fab fa-linkedin-in"></i>
                    </a>
                    {{/if}}
                    {{#if github_url}}
                    <a href="{{github_url}}" target="_blank" class="social-link">
                        <i class="fab fa-github"></i>
                    </a>
                    {{/if}}
                    {{#if twitter_url}}
                    <a href="{{twitter_url}}" target="_blank" class="social-link">
                        <i class="fab fa-twitter"></i>
                    </a>
                    {{/if}}
                </div>
            </div>
            <div class="hero-image">
                <div class="profile-container">
                    <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face" alt="{{full_name}}" class="profile-img">
                    <div class="floating-card">
                        <i class="fas fa-briefcase"></i>
                        <span>{{years_experience}}+ Years Experience</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">About Me</h2>
                <p class="section-subtitle">Get to know me better</p>
            </div>
            <div class="about-content">
                <div class="about-text">
                    <p class="about-description">{{about_me}}</p>
                    <div class="about-stats">
                        <div class="stat-item">
                            <span class="stat-number">{{project_count}}</span>
                            <span class="stat-label">Projects Completed</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">{{client_count}}</span>
                            <span class="stat-label">Happy Clients</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">{{years_experience}}</span>
                            <span class="stat-label">Years Experience</span>
                        </div>
                    </div>
                </div>
                <div class="about-skills">
                    <h3>Core Skills</h3>
                    <div class="skills-grid">
                        {{#each skills}}
                        <div class="skill-item">
                            <div class="skill-name">{{name}}</div>
                            <div class="skill-bar">
                                <div class="skill-progress" data-width="{{proficiency}}%"></div>
                            </div>
                        </div>
                        {{/each}}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="experience">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Experience</h2>
                <p class="section-subtitle">My professional journey</p>
            </div>
            <div class="timeline">
                {{#each work_experience}}
                <div class="timeline-item">
                    <div class="timeline-date">{{start_date}} - {{end_date}}</div>
                    <div class="timeline-content">
                        <h3 class="timeline-title">{{position}}</h3>
                        <h4 class="timeline-company">{{company}}</h4>
                        <p class="timeline-description">{{description}}</p>
                        <div class="timeline-skills">
                            {{#each key_achievements}}
                            <span class="achievement-tag">{{this}}</span>
                            {{/each}}
                        </div>
                    </div>
                </div>
                {{/each}}
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="projects">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Projects</h2>
                <p class="section-subtitle">Some of my recent work</p>
            </div>
            <div class="projects-grid">
                {{#each projects}}
                <div class="project-card">
                    <div class="project-image">
                        <img src="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=500&h=300&fit=crop" alt="{{title}}">
                        <div class="project-overlay">
                            <div class="project-actions">
                                {{#if live_url}}
                                <a href="{{live_url}}" target="_blank" class="project-btn">
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                                {{/if}}
                                {{#if github_url}}
                                <a href="{{github_url}}" target="_blank" class="project-btn">
                                    <i class="fab fa-github"></i>
                                </a>
                                {{/if}}
                            </div>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3 class="project-title">{{title}}</h3>
                        <p class="project-description">{{description}}</p>
                        <div class="project-tech">
                            {{#each technologies}}
                            <span class="tech-tag">{{this}}</span>
                            {{/each}}
                        </div>
                    </div>
                </div>
                {{/each}}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Get In Touch</h2>
                <p class="section-subtitle">Let's work together</p>
            </div>
            <div class="contact-content">
                <div class="contact-info">
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <div>
                            <h4>Email</h4>
                            <p>{{email}}</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <div>
                            <h4>Phone</h4>
                            <p>{{phone}}</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <div>
                            <h4>Location</h4>
                            <p>{{location}}</p>
                        </div>
                    </div>
                </div>
                <form class="contact-form" id="contact-form">
                    <div class="form-group">
                        <input type="text" name="name" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <input type="email" name="email" placeholder="Your Email" required>
                    </div>
                    <div class="form-group">
                        <input type="text" name="subject" placeholder="Subject" required>
                    </div>
                    <div class="form-group">
                        <textarea name="message" placeholder="Your Message" rows="6" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2024 {{full_name}}. All rights reserved.</p>
                <div class="footer-social">
                    {{#if linkedin_url}}
                    <a href="{{linkedin_url}}" target="_blank" class="social-link">
                        <i class="fab fa-linkedin-in"></i>
                    </a>
                    {{/if}}
                    {{#if github_url}}
                    <a href="{{github_url}}" target="_blank" class="social-link">
                        <i class="fab fa-github"></i>
                    </a>
                    {{/if}}
                </div>
            </div>
        </div>
    </footer>

    <script>{{js}}</script>
</body>
</html>
        """

    def _get_modern_professional_css(self) -> str:
        """Modern Professional CSS Template"""
        return """
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e293b;
    --accent-color: #10b981;
    --background-color: #ffffff;
    --text-color: #1f2937;
    --text-light: #6b7280;
    --border-color: #e5e7eb;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="dark"] {
    --background-color: #0f172a;
    --text-color: #f1f5f9;
    --text-light: #94a3b8;
    --border-color: #334155;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
    transition: var(--transition);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    transition: var(--transition);
}

[data-theme="dark"] .navbar {
    background: rgba(15, 23, 42, 0.95);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
}

.nav-logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
}

.nav-menu {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.nav-link {
    text-decoration: none;
    color: var(--text-color);
    font-weight: 500;
    transition: var(--transition);
    position: relative;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--primary-color);
    transition: var(--transition);
}

.nav-link:hover::after,
.nav-link.active::after {
    width: 100%;
}

.theme-toggle {
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    background: var(--primary-color);
    color: white;
    transition: var(--transition);
}

.nav-toggle {
    display: none;
    flex-direction: column;
    cursor: pointer;
}

.bar {
    width: 25px;
    height: 3px;
    background: var(--text-color);
    margin: 3px 0;
    transition: var(--transition);
}

/* Hero Section */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding-top: 70px;
    background: linear-gradient(135deg, var(--background-color) 0%, rgba(37, 99, 235, 0.05) 100%);
}

.hero-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}

.hero-content {
    animation: slideInLeft 1s ease-out;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.5rem;
    color: var(--text-light);
    margin-bottom: 1.5rem;
}

.hero-description {
    font-size: 1.1rem;
    color: var(--text-light);
    margin-bottom: 2rem;
    line-height: 1.8;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.btn {
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.btn-secondary {
    background: transparent;
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}

.btn-secondary:hover {
    background: var(--primary-color);
    color: white;
}

.hero-social {
    display: flex;
    gap: 1rem;
}

.social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    text-decoration: none;
    transition: var(--transition);
}

.social-link:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow);
}

.hero-image {
    animation: slideInRight 1s ease-out;
}

.profile-container {
    position: relative;
}

.profile-img {
    width: 100%;
    max-width: 400px;
    border-radius: 1rem;
    box-shadow: var(--shadow);
}

.floating-card {
    position: absolute;
    bottom: 20px;
    right: -20px;
    background: white;
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    animation: float 3s ease-in-out infinite;
}

[data-theme="dark"] .floating-card {
    background: var(--secondary-color);
}

/* Section Styles */
.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 3px;
    background: var(--accent-color);
}

.section-subtitle {
    color: var(--text-light);
    font-size: 1.1rem;
}

/* About Section */
.about {
    padding: 6rem 0;
    background: rgba(37, 99, 235, 0.03);
}

.about-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: start;
}

.about-description {
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 2rem;
}

.about-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
}

.stat-item {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.stat-label {
    color: var(--text-light);
    font-size: 0.9rem;
}

.skills-grid {
    display: grid;
    gap: 1.5rem;
}

.skill-item {
    display: grid;
    gap: 0.5rem;
}

.skill-name {
    font-weight: 600;
    color: var(--text-color);
}

.skill-bar {
    height: 8px;
    background: var(--border-color);
    border-radius: 4px;
    overflow: hidden;
}

.skill-progress {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    border-radius: 4px;
    transition: width 2s ease-out;
    width: 0%;
}

/* Experience Section */
.experience {
    padding: 6rem 0;
}

.timeline {
    position: relative;
    max-width: 800px;
    margin: 0 auto;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 30px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: var(--primary-color);
}

.timeline-item {
    position: relative;
    margin-bottom: 3rem;
    padding-left: 80px;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: 21px;
    top: 0;
    width: 18px;
    height: 18px;
    background: var(--primary-color);
    border: 3px solid var(--background-color);
    border-radius: 50%;
}

.timeline-date {
    position: absolute;
    left: -150px;
    top: 0;
    color: var(--primary-color);
    font-weight: 600;
    font-size: 0.9rem;
}

.timeline-content {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: var(--shadow);
    border-left: 4px solid var(--primary-color);
}

[data-theme="dark"] .timeline-content {
    background: var(--secondary-color);
}

.timeline-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

.timeline-company {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.timeline-description {
    line-height: 1.7;
    margin-bottom: 1rem;
}

.timeline-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.achievement-tag {
    background: var(--primary-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.8rem;
}

/* Projects Section */
.projects {
    padding: 6rem 0;
    background: rgba(37, 99, 235, 0.03);
}

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.project-card {
    background: white;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: var(--transition);
}

[data-theme="dark"] .project-card {
    background: var(--secondary-color);
}

.project-car
