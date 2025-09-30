#!/usr/bin/env python3
"""
Portfolio Templates Service
Provides 5 complete, production-ready portfolio website templates
"""

from typing import Dict, List, Any
import uuid
from datetime import datetime

class PortfolioTemplatesService:
    """Service for managing portfolio templates"""

    def __init__(self):
        self.templates = self._create_all_templates()

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates"""
        return list(self.templates.values())

    def get_template_by_id(self, template_id: str) -> Dict[str, Any]:
        """Get a specific template by ID"""
        return self.templates.get(template_id)

    def _create_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create all portfolio templates"""
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
            <div class="nav-menu" id="nav-menu">
                <a href="#home" class="nav-link active">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#contact" class="nav-link">Contact</a>
                <button class="theme-toggle" id="theme-toggle">
                    <i class="fas fa-moon"></i>
                </button>
            </div>
            <button class="nav-toggle" id="nav-toggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </button>
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
                <div class="hero-social">
                    <a href="{{linkedin_url}}" target="_blank" class="social-link">
                        <i class="fab fa-linkedin-in"></i>
                    </a>
                    <a href="{{github_url}}" target="_blank" class="social-link">
                        <i class="fab fa-github"></i>
                    </a>
                </div>
            </div>
            <div class="hero-image">
                <div class="profile-container">
                    <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face" alt="{{full_name}}" class="profile-img">
                    <div class="floating-card">
                        <i class="fas fa-briefcase"></i>
                        <span>{{years_experience}}+ Years</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

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
                            <span class="stat-number">50+</span>
                            <span class="stat-label">Projects Completed</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">30+</span>
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
                        <div class="skill-item">
                            <div class="skill-name">JavaScript</div>
                            <div class="skill-bar">
                                <div class="skill-progress" data-width="90%"></div>
                            </div>
                        </div>
                        <div class="skill-item">
                            <div class="skill-name">React</div>
                            <div class="skill-bar">
                                <div class="skill-progress" data-width="85%"></div>
                            </div>
                        </div>
                        <div class="skill-item">
                            <div class="skill-name">Node.js</div>
                            <div class="skill-bar">
                                <div class="skill-progress" data-width="80%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="experience" class="experience">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Experience</h2>
                <p class="section-subtitle">My professional journey</p>
            </div>
            <div class="timeline">
                <div class="timeline-item">
                    <div class="timeline-date">2022 - Present</div>
                    <div class="timeline-content">
                        <h3 class="timeline-title">Senior Developer</h3>
                        <h4 class="timeline-company">Tech Company</h4>
                        <p class="timeline-description">Leading development of scalable web applications and mentoring junior developers.</p>
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-date">2019 - 2022</div>
                    <div class="timeline-content">
                        <h3 class="timeline-title">Full Stack Developer</h3>
                        <h4 class="timeline-company">Startup Inc</h4>
                        <p class="timeline-description">Built and maintained full-stack applications using modern web technologies.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="projects" class="projects">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Projects</h2>
                <p class="section-subtitle">Some of my recent work</p>
            </div>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-image">
                        <img src="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=500&h=300&fit=crop" alt="Project 1">
                        <div class="project-overlay">
                            <div class="project-actions">
                                <a href="#" target="_blank" class="project-btn">
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                                <a href="#" target="_blank" class="project-btn">
                                    <i class="fab fa-github"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3 class="project-title">E-commerce Platform</h3>
                        <p class="project-description">Full-stack e-commerce solution with modern design and functionality.</p>
                        <div class="project-tech">
                            <span class="tech-tag">React</span>
                            <span class="tech-tag">Node.js</span>
                            <span class="tech-tag">MongoDB</span>
                        </div>
                    </div>
                </div>
                <div class="project-card">
                    <div class="project-image">
                        <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&h=300&fit=crop" alt="Project 2">
                        <div class="project-overlay">
                            <div class="project-actions">
                                <a href="#" target="_blank" class="project-btn">
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                                <a href="#" target="_blank" class="project-btn">
                                    <i class="fab fa-github"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3 class="project-title">Task Management App</h3>
                        <p class="project-description">Real-time task management with team collaboration features.</p>
                        <div class="project-tech">
                            <span class="tech-tag">Vue.js</span>
                            <span class="tech-tag">Express</span>
                            <span class="tech-tag">Socket.io</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

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

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2024 {{full_name}}. All rights reserved.</p>
                <div class="footer-social">
                    <a href="{{linkedin_url}}" target="_blank" class="social-link">
                        <i class="fab fa-linkedin-in"></i>
                    </a>
                    <a href="{{github_url}}" target="_blank" class="social-link">
                        <i class="fab fa-github"></i>
                    </a>
                </div>
            </div>
        </div>
    </footer>

    <script>{{js}}</script>
</body>
</html>"""

    def _get_modern_professional_css(self) -> str:
        """Modern Professional CSS"""
        return """:root {
    --primary-color: #2563eb;
    --secondary-color: #1e293b;
    --accent-color: #10b981;
    --background-color: #ffffff;
    --text-color: #1f2937;
    --text-light: #6b7280;
    --border-color: #e5e7eb;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}

[data-theme="dark"] {
    --background-color: #0f172a;
    --text-color: #f1f5f9;
    --text-light: #94a3b8;
    --border-color: #334155;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html { scroll-behavior: smooth; }

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
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 0.5rem;
    border-radius: 50%;
    cursor: pointer;
    transition: var(--transition);
}

.nav-toggle {
    display: none;
    flex-direction: column;
    cursor: pointer;
    background: none;
    border: none;
}

.bar {
    width: 25px;
    height: 3px;
    background: var(--text-color);
    margin: 3px 0;
    transition: var(--transition);
}

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
    font-family: inherit;
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
}

.timeline-company {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.timeline-description {
    line-height: 1.7;
}

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

.project-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.project-image {
    position: relative;
    overflow: hidden;
    height: 200px;
}

.project-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: var(--transition);
}

.project-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(37, 99, 235, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: var(--transition);
}

.project-image:hover .project-overlay {
    opacity: 1;
}

.project-actions {
    display: flex;
    gap: 1rem;
}

.project-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    background: white;
    color: var(--primary-color);
    border-radius: 50%;
    text-decoration: none;
    transition: var(--transition);
}

.project-btn:hover {
    transform: scale(1.1);
}

.project-content {
    padding: 2rem;
}

.project-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.project-description {
    color: var(--text-light);
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.project-tech {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.tech-tag {
    background: rgba(37, 99, 235, 0.1);
    color: var(--primary-color);
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.8rem;
}

.contact {
    padding: 6rem 0;
}

.contact-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
}

.contact-info {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.contact-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: white;
    border-radius: 1rem;
    box-shadow: var(--shadow);
}

[data-theme="dark"] .contact-item {
    background: var(--secondary-color);
}

.contact-item i {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
}

.contact-item h4 {
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

.contact-form {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: var(--shadow);
}

[data-theme="dark"] .contact-form {
    background: var(--secondary-color);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 1rem;
    border: 2px solid var(--border-color);
    border-radius: 0.5rem;
    font-family: inherit;
    font-size: 1rem;
    transition: var(--transition);
    background: var(--background-color);
    color: var(--text-color);
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary-color);
}

.footer {
    background: var(--secondary-color);
    color: white;
    padding: 2rem 0;
    text-align: center;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-social {
    display: flex;
    gap: 1rem;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

@media (max-width: 768px) {
    .nav-menu {
        position: fixed;
        left: -100%;
        top: 70px;
        flex-direction: column;
        background-color: var(--background-color);
        width: 100%;
        text-align: center;
        transition: var(--transition);
        box-shadow: var(--shadow);
        padding: 2rem 0;
    }

    .nav-menu.active {
        left: 0;
    }

    .nav-toggle {
        display: flex;
    }

    .hero-container {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .hero-title {
        font-size: 2.5rem;
    }

    .about-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }

    .contact-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }

    .timeline-date {
        position: static;
        margin-bottom: 1rem;
    }

    .timeline-item {
        padding-left: 60px;
    }

    .timeline::before {
        left: 20px;
    }

    .timeline-item::before {
        left: 11px;
    }

    .footer-content {
        flex-direction: column;
        gap: 1rem;
    }
}"""

    def _get_modern_professional_js(self) -> str:
        """Modern Professional JavaScript"""
        return """document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu) {
                navMenu.classList.remove('active');
            }
        });
    });

    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.dataset.theme = body.dataset.theme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', body.dataset.theme);

            const icon = themeToggle.querySelector('i');
            if (icon) {
                if (body.dataset.theme === 'dark') {
                    icon.className = 'fas fa-sun';
                } else {
                    icon.className = 'fas fa-moon';
                }
            }
        });
    }

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.dataset.theme = savedTheme;
        const themeIcon = themeToggle?.querySelector('i');
        if (themeIcon) {
            themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
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

    // Animate skill bars on scroll
    const observerOptions = {
        threshold: 0.7,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const skillBars = entry.target.querySelectorAll('.skill-progress');
                skillBars.forEach(bar => {
                    const width = bar.getAttribute('data-width');
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 300);
                });
            }
        });
    }, observerOptions);

    const skillsSection = document.querySelector('.about-skills');
    if (skillsSection) {
        observer.observe(skillsSection);
    }

    // Contact form handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const data = Object.fromEntries(formData);

            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;

            // Simulate form submission (replace with actual API call)
            setTimeout(() => {
                alert('Message sent successfully! I will get back to you soon.');
                this.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
});"""

    def _get_creative_designer_html(self) -> str:
        """Creative Designer HTML Template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{full_name}} - Creative Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{css}}</style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <span class="logo-icon">🎨</span>
                {{full_name}}
            </div>
            <div class="nav-menu">
                <a href="#home" class="nav-link active">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#portfolio" class="nav-link">Portfolio</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="hero-bg">
            <div class="floating-shapes">
                <div class="shape shape-1"></div>
                <div class="shape shape-2"></div>
                <div class="shape shape-3"></div>
            </div>
        </div>
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">
                    <span class="title-line">Creative</span>
                    <span class="title-highlight">{{full_name}}</span>
                </h1>
                <p class="hero-description">{{summary}}</p>
                <div class="hero-buttons">
                    <a href="#portfolio" class="btn btn-primary">View My Work</a>
                    <a href="#contact" class="btn btn-outline">Let's Talk</a>
                </div>
            </div>
            <div class="hero-visual">
                <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face" alt="{{full_name}}" class="profile-img">
            </div>
        </div>
    </section>

    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>{{about_me}}</p>
                </div>
            </div>
        </div>
    </section>

    <section id="portfolio" class="portfolio">
        <div class="container">
            <h2 class="section-title">My Work</h2>
            <div class="portfolio-grid">
                <div class="portfolio-item">
                    <img src="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=400&h=300&fit=crop" alt="Project 1">
                    <div class="portfolio-overlay">
                        <h3>Creative Project 1</h3>
                        <p>An amazing creative project</p>
                    </div>
                </div>
                <div class="portfolio-item">
                    <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop" alt="Project 2">
                    <div class="portfolio-overlay">
                        <h3>Creative Project 2</h3>
                        <p>Another stunning design</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Get In Touch</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <p>Email: {{email}}</p>
                    <p>Phone: {{phone}}</p>
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
    <script>{{js}}</script>
</body>
</html>"""

    def _get_creative_designer_css(self) -> str:
        return """body { font-family: 'Poppins', sans-serif; margin: 0; color: #2d3436; }
.navbar { position: fixed; top: 0; width: 100%; background: #fff; z-index: 1000; padding: 1rem 0; }
.nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 2rem; }
.hero { min-height: 100vh; display: flex; align-items: center; background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); color: white; position: relative; }
.hero-container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }
.section-title { font-size: 2.5rem; text-align: center; margin-bottom: 3rem; }
.about, .portfolio, .contact { padding: 6rem 0; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
.btn { padding: 1rem 2rem; margin: 0.5rem; text-decoration: none; border-radius: 50px; font-weight: 600; display: inline-block; }
.btn-primary { background: #ff6b6b; color: white; }
.btn-outline { background: transparent; color: white; border: 2px solid white; }
.portfolio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
.portfolio-item { position: relative; overflow: hidden; border-radius: 1rem; }
.portfolio-item img { width: 100%; height: 250px; object-fit: cover; }
.contact-content { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; }
.contact-form { display: flex; flex-direction: column; gap: 1rem; }
.contact-form input, .contact-form textarea { padding: 1rem; border: 1px solid #ddd; border-radius: 0.5rem; }
.contact-form button { padding: 1rem; background: #ff6b6b; color: white; border: none; border-radius: 0.5rem; cursor: pointer; }"""

    def _get_creative_designer_js(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() {
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });
    });"""

    def _get_tech_developer_html(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{full_name}} - Developer Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{css}}</style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">{{full_name}}.dev</div>
            <div class="nav-menu">
                <a href="#home" class="nav-link">&gt; home</a>
                <a href="#about" class="nav-link">&gt; about</a>
                <a href="#projects" class="nav-link">&gt; projects</a>
                <a href="#contact" class="nav-link">&gt; contact</a>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="container">
            <div class="terminal">
                <div class="terminal-header">
                    <span class="terminal-title">{{full_name}}@portfolio:~$</span>
                </div>
                <div class="terminal-body">
                    <p>&gt; whoami</p>
                    <p>{{full_name}} - {{title}}</p>
                    <p>&gt; cat about.txt</p>
                    <p>{{summary}}</p>
                    <p>&gt; ls skills/</p>
                    <div class="skills-list">
                        <span class="skill-tag">JavaScript</span>
                        <span class="skill-tag">Python</span>
                        <span class="skill-tag">React</span>
                        <span class="skill-tag">Node.js</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">&lt;projects/&gt;</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-header">
                        <h3>Awesome Project</h3>
                        <div class="project-links">
                            <a href="{{github_url}}" target="_blank"><i class="fab fa-github"></i></a>
                            <a href="#" target="_blank"><i class="fas fa-external-link-alt"></i></a>
                        </div>
                    </div>
                    <p>A cool project description</p>
                    <div class="tech-stack">
                        <span class="tech-tag">React</span>
                        <span class="tech-tag">Node.js</span>
                        <span class="tech-tag">MongoDB</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <script>{{js}}</script>
</body>
</html>"""

    def _get_tech_developer_css(self) -> str:
        return """body { font-family: 'Fira Code', monospace; margin: 0; background: #0d1117; color: #c9d1d9; }
.navbar { position: fixed; top: 0; width: 100%; background: #161b22; z-index: 1000; padding: 1rem 0; }
.nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 2rem; }
.nav-logo { color: #00ff88; font-weight: bold; }
.nav-link { color: #c9d1d9; text-decoration: none; margin: 0 1rem; }
.nav-link:hover { color: #00ff88; }
.hero { min-height: 100vh; display: flex; align-items: center; padding-top: 70px; }
.terminal { background: #161b22; border: 1px solid #30363d; border-radius: 0.5rem; }
.terminal-header { background: #21262d; padding: 1rem; border-bottom: 1px solid #30363d; }
.terminal-body { padding: 2rem; line-height: 1.8; }
.skills-list { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
.skill-tag { background: #238636; color: white; padding: 0.25rem 0.75rem; border-radius: 0.25rem; font-size: 0.8rem; }
.projects { padding: 6rem 0; }
.section-title { font-size: 2rem; color: #00ff88; text-align: center; margin-bottom: 3rem; }
.projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; }
.project-card { background: #161b22; border: 1px solid #30363d; border-radius: 0.5rem; padding: 2rem; }
.project-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.tech-tag { background: #ff0088; color: white; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.7rem; margin: 0.25rem; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }"""

    def _get_tech_developer_js(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() {
        // Terminal typing effect
        const terminalBody = document.querySelector('.terminal-body');
        if (terminalBody) {
            terminalBody.style.opacity = '0';
            setTimeout(() => {
                terminalBody.style.opacity = '1';
                terminalBody.style.animation = 'fadeIn 1s ease-in';
            }, 500);
        }
    });"""

    def _get_minimal_clean_html(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{full_name}}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>{{css}}</style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">{{full_name}}</div>
            <div class="nav-menu">
                <a href="#about">About</a>
                <a href="#work">Work</a>
                <a href="#contact">Contact</a>
            </div>
        </div>
    </nav>

    <main>
        <section class="hero">
            <div class="container">
                <h1>{{full_name}}</h1>
                <p class="lead">{{title}}</p>
                <p>{{summary}}</p>
            </div>
        </section>

        <section id="about" class="about">
            <div class="container">
                <h2>About</h2>
                <p>{{about_me}}</p>
            </div>
        </section>

        <section id="work" class="work">
            <div class="container">
                <h2>Work</h2>
                <div class="work-list">
                    <article class="work-item">
                        <h3>Sample Project</h3>
                        <p>A great project description</p>
                        <a href="#" target="_blank">View Project</a>
                    </article>
                </div>
            </div>
        </section>

        <section id="contact" class="contact">
            <div class="container">
                <h2>Contact</h2>
                <p>{{email}}</p>
            </div>
        </section>
    </main>
    <script>{{js}}</script>
</body>
</html>"""

    def _get_minimal_clean_css(self) -> str:
        return """body { font-family: 'Inter', sans-serif; line-height: 1.6; color: #111827; margin: 0; }
.navbar { position: fixed; top: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); z-index: 1000; }
.nav-container { max-width: 800px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; }
.nav-logo { font-weight: 600; }
.nav-menu a { text-decoration: none; color: #111827; margin-left: 2rem; }
.container { max-width: 800px; margin: 0 auto; padding: 0 2rem; }
.hero { padding: 8rem 0 4rem; }
.hero h1 { font-size: 3rem; font-weight: 300; margin-bottom: 0.5rem; }
.lead { font-size: 1.25rem; color: #6b7280; margin-bottom: 2rem; }
.about, .work, .contact { padding: 4rem 0; }
h2 { font-size: 1.5rem; font-weight: 600; margin-bottom: 2rem; }
.work-item { margin-bottom: 3rem; }
.work-item h3 { font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem; }
.work-item a { color: #6366f1; text-decoration: none; }
.work-item a:hover { text-decoration: underline; }"""

    def _get_minimal_clean_js(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() {
        // Simple smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });
    });"""

    def _get_corporate_executive_html(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{full_name}} - Executive Profile</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{css}}</style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">{{full_name}}</div>
            <div class="nav-menu">
                <a href="#home" class="nav-link">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#achievements" class="nav-link">Achievements</a>
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
                    <a href="#contact" class="btn btn-primary">Connect</a>
                    <a href="#experience" class="btn btn-secondary">View Experience</a>
                </div>
            </div>
            <div class
