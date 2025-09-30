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
        self.templates = self._create_templates()

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates"""
        return list(self.templates.values())

    def get_template_by_id(self, template_id: str) -> Dict[str, Any]:
        """Get a specific template by ID"""
        return self.templates.get(template_id)

    def _create_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create all portfolio templates"""
        return {
            "modern-professional": self._create_modern_professional_template(),
            "creative-designer": self._create_creative_designer_template(),
            "tech-developer": self._create_tech_developer_template(),
            "minimal-clean": self._create_minimal_clean_template(),
            "corporate-executive": self._create_corporate_executive_template()
        }

    def _create_modern_professional_template(self) -> Dict[str, Any]:
        """Modern Professional Template - Clean, responsive design"""
        return {
            "id": "modern-professional",
            "name": "Modern Professional",
            "description": "Clean, modern design perfect for professionals and consultants",
            "category": "professional",
            "preview_image": "/templates/modern-professional.jpg",
            "features": ["responsive", "animations", "dark-mode", "contact-form"],
            "html_template": self._get_modern_professional_html(),
            "css_template": self._get_modern_professional_css(),
            "js_template": self._get_modern_professional_js(),
            "color_scheme": {
                "primary": "#2563eb",
                "secondary": "#1e293b",
                "accent": "#10b981",
                "background": "#ffffff",
                "text": "#1f2937"
            },
            "sections": ["hero", "about", "experience", "skills", "projects", "testimonials", "contact"],
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _get_modern_professional_html(self) -> str:
        """HTML template for Modern Professional"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{name}} - Professional Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{css}}</style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">{{name}}</div>
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
                <h1 class="hero-title">{{name}}</h1>
                <h2 class="hero-subtitle">{{title}}</h2>
                <p class="hero-description">{{summary}}</p>
                <div class="hero-buttons">
                    <a href="#contact" class="btn btn-primary">Get In Touch</a>
                    <a href="{{resume_url}}" class="btn btn-secondary" target="_blank">Download CV</a>
                </div>
                <div class="hero-social">
                    {{#each social_links}}
                    <a href="{{url}}" target="_blank" class="social-link">
                        <i class="{{icon}}"></i>
                    </a>
                    {{/each}}
                </div>
            </div>
            <div class="hero-image">
                <img src="{{profile_image}}" alt="{{name}}" class="profile-img">
                <div class="floating-card">
                    <i class="fas fa-code"></i>
                    <span>{{years_experience}}+ Years Experience</span>
                </div>
            </div>
        </div>
        <div class="scroll-indicator">
            <div class="scroll-arrow"></div>
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
                    <p class="about-description">{{about_description}}</p>
                    <div class="about-stats">
                        <div class="stat-item">
                            <span class="stat-number">{{projects_count}}</span>
                            <span class="stat-label">Projects Completed</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">{{clients_count}}</span>
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
                                <div class="skill-progress" data-width="{{level}}%"></div>
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
                {{#each experience}}
                <div class="timeline-item">
                    <div class="timeline-date">{{start_date}} - {{end_date}}</div>
                    <div class="timeline-content">
                        <h3 class="timeline-title">{{position}}</h3>
                        <h4 class="timeline-company">{{company}}</h4>
                        <p class="timeline-description">{{description}}</p>
                        <div class="timeline-skills">
                            {{#each technologies}}
                            <span class="skill-tag">{{this}}</span>
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
                        <img src="{{image}}" alt="{{title}}">
                        <div class="project-overlay">
                            <div class="project-actions">
                                <a href="{{live_url}}" target="_blank" class="project-btn">
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                                <a href="{{github_url}}" target="_blank" class="project-btn">
                                    <i class="fab fa-github"></i>
                                </a>
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
                <p>&copy; 2024 {{name}}. All rights reserved.</p>
                <div class="footer-social">
                    {{#each social_links}}
                    <a href="{{url}}" target="_blank" class="social-link">
                        <i class="{{icon}}"></i>
                    </a>
                    {{/each}}
                </div>
            </div>
        </div>
    </footer>

    <script>{{js}}</script>
</body>
</html>
        """

    def _get_modern_professional_css(self) -> str:
        """CSS template for Modern Professional"""
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
    position: relative;
    animation: slideInRight 1s ease-out;
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

.scroll-indicator {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    animation: bounce 2s infinite;
}

.scroll-arrow {
    width: 30px;
    height: 30px;
    border-right: 3px solid var(--primary-color);
    border-bottom: 3px solid var(--primary-color);
    transform: rotate(45deg);
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

.skill-tag {
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

/* Contact Section */
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

/* Footer */
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

/* Animations */
@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes float {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-20px);
    }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0) translateX(-50%);
    }
    40% {
        transform: translateY(-30px) translateX(-50%);
    }
    60% {
        transform: translateY(-15px) translateX(-50%);
    }
}

/* Responsive Design */
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

    .about-stats {
        grid-template-columns: 1fr;
        gap: 1rem;
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
}
        """

    def _get_modern_professional_js(self) -> str:
        """JavaScript template for Modern Professional"""
        return """
document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });

    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    themeToggle.addEventListener('click', () => {
        body.dataset.theme = body.dataset.theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', body.dataset.theme);

        const icon = themeToggle.querySelector('i');
        if (body.dataset.theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.dataset.theme = savedTheme;
        const icon = themeToggle.querySelector('i');
        icon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
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
            if (link.getAttribute('href') === `#${current}`) {
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

    // Animate stats counter
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const finalValue = parseInt(stat.textContent);
                    let currentValue = 0;
                    const increment = finalValue / 50;
                    const timer = setInterval(() => {
                        currentValue += increment;
                        if (currentValue >= finalValue) {
                            stat.textContent = finalValue;
                            clearInterval(timer);
                        } else {
                            stat.textContent = Math.floor(currentValue);
                        }
                    }, 50);
                });
            }
        });
    }, observerOptions);

    const aboutStats = document.querySelector('.about-stats');
    if (aboutStats) {
        statsObserver.observe(aboutStats);
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

    // Navbar background on scroll
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = body.dataset.theme === 'dark'
                ? 'rgba(15, 23, 42, 0.98)'
                : 'rgba(255, 255, 255, 0.98)';
        } else {
            navbar.style.background = body.dataset.theme === 'dark'
                ? 'rgba(15, 23, 42, 0.95)'
                : 'rgba(255, 255, 255, 0.95)';
        }
    });

    // Parallax effect for hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });

    // Lazy loading for project images
    const projectImages = document.querySelectorAll('.project-image img');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            }
        });
    });

    projectImages.forEach(img => {
        if (img.dataset.src) {
            imageObserver.observe(img);
        }
    });

    // Add loading animations
    const animateOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    // Apply animation to various elements
    document.querySelectorAll('.project-card, .timeline-item, .contact-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        animateOnScroll.observe(el);
    });
});
        """

    def _create_creative_designer_template(self) -> Dict[str, Any]:
        """Creative Designer Template - Vibrant and artistic design"""
        return {
            "id": "creative-designer",
            "name": "Creative Designer",
            "description": "Vibrant and creative design perfect for designers and artists",
            "category": "creative",
            "preview_image": "/templates/creative-designer.jpg",
            "features": ["animations", "parallax", "colorful", "artistic"],
            "html_template": self._get_creative_designer_html(),
            "css_template": self._get_creative_designer_css(),
            "js_template": self._get_creative_designer_js(),
            "color_scheme": {
                "primary": "#ff6b6b",
                "secondary": "#4ecdc4",
                "accent": "#45b7d1",
                "background": "#f8f9fa",
                "text": "#2d3436"
            },
            "sections": ["hero", "about", "portfolio", "services", "testimonials", "contact"],
            "is_active": True,
            "created_at": datetime.utcnow()
        }

    def _get_creative_designer_html(self) -> str:
        """HTML template for Creative Designer"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{name}} - Creative Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{css}}</style>
</head>
<body>
    <!-- Loading Screen -->
    <div class="loading-screen" id="loading-screen">
        <div class="loader">
            <div class="loader-circle"></div>
            <div class="loader-text">{{name}}</div>
        </div>
    </div>

    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <span class="logo-icon">🎨</span>
                {{name}}
            </div>
            <div class="nav-menu" id="nav-menu">
                <a href="#home" class="nav-link active">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#portfolio" class="nav-link">Portfolio</a>
                <a href="#services" class="nav-link">Services</a>
                <a href="#contact" class="nav-link">Contact</a>
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
        <div class="hero-bg">
            <div class="floating-shapes">
                <div class="shape shape-1"></div>
                <div class="shape shape-2"></div>
                <div class="shape shape-3"></div>
                <div class="shape shape-4"></div>
                <div class="shape shape-5"></div>
            </div>
        </div>
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">
                    <span class="title-line">Creative</span>
                    <span class="title-line">Designer</span>
                    <span class="title-highlight">{{name}}</span>
                </h1>
                <p class="hero-description">{{summary}}</p>
                <div class="hero-buttons">
                    <a href="#portfolio" class="btn btn-primary">
                        <span>View My Work</span>
                        <i class="fas fa-arrow-right"></i>
                    </a>
                    <a href="#contact" class="btn btn-outline">
                        <span>Let's Talk</span>
                        <i class="fas fa-comments"></i>
                    </a>
                </div>
            </div>
            <div class="hero-visual">
                <div class="profile-container">
                    <div class="profile-frame">
                        <img src="{{profile_image}}" alt="{{name}}" class="profile-img">
                        <div class="profile-overlay"></div>
                    </div>
                    <div class="creativity-indicators">
                        <div class="indicator indicator-1">
                            <i class="fas fa-palette"></i>
                        </div>
                        <div class="indicator indicator-2">
                            <i class="fas fa-pencil-ruler"></i>
                        </div>
                        <div class="indicator indicator-3">
                            <i class="fas fa-lightbulb"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="scroll-indicator">
            <div class="scroll-text">Scroll Down</div>
            <div class="scroll-arrow"></div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">About Me</h2>
                <div class="section-decoration">
                    <span class="decoration-line"></span>
                    <i class="fas fa-star"></i>
                    <span class="decoration-line"></span>
                </div>
            </div>
            <div class="about-content">
                <div class="about-text">
                    <h3 class="about-heading">Hello! I'm {{name}}</h3>
                    <p class="about-description">{{about_description}}</p>
                    <div class="about-highlights">
                        <div class="highlight-item">
                            <div class="highlight-icon">
                                <i class="fas fa-rocket"></i>
                            </div>
                            <div class="highlight-content">
                                <h4>Innovative Solutions</h4>
                                <p>Creating unique designs that stand out</p>
                            </div>
                        </div>
                        <div class="highlight-item">
                            <div class="highlight-icon">
                                <i class="fas fa-heart"></i>
                            </div>
                            <div class="highlight-content">
                                <h4>Passionate Work</h4>
                                <p>Every project is crafted with love</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="about-skills">
                    <h3 class="skills-title">My Expertise</h3>
                    <div class="skills-container">
                        {{#each skills}}
                        <div class="skill-bubble">
                            <div class="skill-icon">{{icon}}</div>
                            <div class="skill-name">{{name}}</div>
                            <div class="skill-level">{{level}}%</div>
                        </div>
                        {{/each}}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Portfolio Section -->
    <section id="portfolio" class="portfolio">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">My Portfolio</h2>
                <div class="section-decoration">
                    <span class="decoration-line"></span>
                    <i class="fas fa-palette"></i>
                    <span class="decoration-line"></span>
                </div>
            </div>
            <div class="portfolio-filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="web">Web Design</button>
                <button class="filter-btn" data-filter="mobile">Mobile</button>
                <button class="filter-btn" data-filter="branding">Branding</button>
                <button class="filter-btn" data-filter="print">Print</button>
            </div>
            <div class="portfolio-grid">
                {{#each projects}}
                <div class="portfolio-item" data-category="{{category}}">
                    <div class="portfolio-image">
                        <img src="{{image}}" alt="{{title}}">
                        <div class="portfolio-overlay">
                            <div class="portfolio-info">
                                <h3 class="portfolio-title">{{title}}</h3>
                                <p class="portfolio-category">{{category}}</p>
                            </div>
                            <div class="portfolio-actions">
                                <a href="{{image}}" class="portfolio-btn" data-lightbox="portfolio">
                                    <i class="fas fa-search-plus"></i>
                                </a>
                                <a href="{{url}}" target="_blank" class="portfolio-btn">
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                {{/each}}
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="services">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">What I Do</h2>
                <div class="section-decoration">
                    <span class="decoration-line"></span>
                    <i class="fas fa-cogs"></i>
                    <span class="decoration-line"></span>
                </div>
            </div>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-laptop-code"></i>
                    </div>
                    <h3 class="service-title">Web Design</h3>
                    <p class="service-description">Beautiful, responsive websites that engage your audience</p>
                    <ul class="service-features">
                        <li>Responsive Design</li>
                        <li>User Experience</li>
                        <li>Modern Aesthetics</li>
                    </ul>
                </div>
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-mobile-alt"></i>
                    </div>
                    <h3 class="service-title">Mobile Apps</h3>
                    <p class="service-description">Intuitive mobile applications that users love</p>
                    <ul class="service-features">
                        <li>iOS & Android</li>
                        <li>User Interface</li>
                        <li>App Store Ready</li>
                    </ul>
                </div>
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-paint-brush"></i>
                    </div>
                    <h3 class="service-title">Branding</h3>
                    <p class="service-description">Complete brand identity that tells your story</p>
                    <ul class="service-features">
                        <li>Logo Design</li>
                        <li>Brand Guidelines</li>
                        <li>Marketing Materials</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Let's Create Together</h2>
                <div class="section-decoration">
                    <span class="decoration-line"></span>
                    <i class="fas fa-envelope"></i>
                    <span class="decoration-line"></span>
                </div>
            </div>
            <div class="contact-content">
                <div class="contact-info">
                    <h3>Ready to start a project?</h3>
                    <p>I'd love to hear about your ideas and bring them to life!</p>
                    <div class="contact-details">
                        <div class="contact-item">
                            <i class="fas fa-envelope"></i>
                            <span>{{email}}</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-phone"></i>
                            <span>{{phone}}</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>{{location}}</span>
                        </div>
                    </div>
                    <div class="social-links">
                        {{#each social_links}}
                        <a href="{{url}}" target="_blank" class="social-link">
                            <i class="{{icon}}"></i>
                        </a>
                        {{/each}}
                    </div>
                </div>
                <form class="contact-form" id="contact-form">
                    <div class="form-row">
                        <div class="form-group">
                            <input type="text" name="name" placeholder="Your Name" required>
                        </div>
                        <div class="form-group">
                            <input type="email" name="email" placeholder="Your Email" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <input type="text" name="subject" placeholder="Subject" required>
                    </div>
                    <div class="form-group">
                        <textarea name="message" placeholder="Tell me about your project..." rows="6" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <span>Send Message</span>
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-text">
                    <p>&copy; 2024 {{name}}. Crafted with ❤️ and creativity.</p>
                </div>
                <div class="footer-links">
                    <a href="#home">Home</a>
                    <a href="#about">About</a>
                    <a href="#portfolio">Portfolio</a>
                    <a href="#contact">Contact</a>
                </div>
            </div>
        </div>
    </footer>

    <script>{{js}}</script>
</body>
</html>
        """
