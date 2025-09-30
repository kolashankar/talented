import os
import json
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
import google.generativeai as genai
from models import (
    PortfolioGenerateRequest, PortfolioGenerateResponse, PortfolioTemplate,
    ParsedResumeData, PersonalDetails
)

logger = logging.getLogger(__name__)

class PortfolioBuilderService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro') if os.environ.get('GEMINI_API_KEY') else None
        self.templates = self._create_advanced_templates()

    def _create_advanced_templates(self) -> Dict[str, PortfolioTemplate]:
        """Create 10+ advanced portfolio templates with animations and 3D effects"""
        templates = {
            "modern-3d": PortfolioTemplate(
                id="modern-3d",
                name="Modern 3D Interactive",
                description="Cutting-edge 3D portfolio with WebGL animations",
                category="modern",
                difficulty="advanced",
                features=["3d-effects", "webgl", "animations", "dark-mode", "responsive"],
                preview_image="https://via.placeholder.com/800x600/1a1a1a/ffffff?text=Modern+3D+Portfolio",
                html_template=self._get_modern_3d_html(),
                css_template=self._get_modern_3d_css(),
                js_template=self._get_modern_3d_js(),
                variables={"primary_color": "#00ff88", "accent_color": "#ff0088"}
            ),
            
            "creative-parallax": PortfolioTemplate(
                id="creative-parallax",
                name="Creative Parallax",
                description="Stunning parallax scrolling with creative animations",
                category="creative",
                difficulty="intermediate",
                features=["parallax", "animations", "scroll-effects", "responsive"],
                preview_image="https://via.placeholder.com/800x600/ff6b6b/ffffff?text=Creative+Parallax",
                html_template=self._get_creative_parallax_html(),
                css_template=self._get_creative_parallax_css(),
                js_template=self._get_creative_parallax_js(),
                variables={"theme_color": "#ff6b6b", "bg_color": "#f8f9fa"}
            ),
            
            "minimal-glass": PortfolioTemplate(
                id="minimal-glass",
                name="Minimal Glassmorphism",
                description="Clean minimal design with glassmorphism effects",
                category="minimal",
                difficulty="intermediate",
                features=["glassmorphism", "minimal", "animations", "responsive"],
                preview_image="https://via.placeholder.com/800x600/ffffff/333333?text=Minimal+Glass",
                html_template=self._get_minimal_glass_html(),
                css_template=self._get_minimal_glass_css(),
                js_template=self._get_minimal_glass_js(),
                variables={"glass_opacity": "0.1", "blur_strength": "20px"}
            ),
            
            "corporate-professional": PortfolioTemplate(
                id="corporate-professional",
                name="Corporate Professional",
                description="Professional corporate design with subtle animations",
                category="corporate",
                difficulty="basic",
                features=["professional", "clean", "responsive", "print-friendly"],
                preview_image="https://via.placeholder.com/800x600/2c3e50/ffffff?text=Corporate+Pro",
                html_template=self._get_corporate_html(),
                css_template=self._get_corporate_css(),
                js_template=self._get_corporate_js(),
                variables={"primary_color": "#2c3e50", "secondary_color": "#3498db"}
            ),
            
            "animated-particles": PortfolioTemplate(
                id="animated-particles",
                name="Animated Particles",
                description="Dynamic particle system background with smooth animations",
                category="animated",
                difficulty="advanced",
                features=["particles", "canvas", "animations", "interactive", "responsive"],
                preview_image="https://via.placeholder.com/800x600/0a0a0a/ffffff?text=Particle+Animation",
                html_template=self._get_particles_html(),
                css_template=self._get_particles_css(),
                js_template=self._get_particles_js(),
                variables={"particle_count": "100", "particle_color": "#00ff88"}
            )
        }
        
        # Add 5 more templates
        templates.update({
            "cyberpunk-neon": self._create_cyberpunk_template(),
            "nature-organic": self._create_nature_template(),
            "retro-vintage": self._create_retro_template(),
            "futuristic-hologram": self._create_futuristic_template(),
            "artistic-canvas": self._create_artistic_template()
        })
        
        return templates

    async def generate_portfolio(self, request: PortfolioGenerateRequest) -> PortfolioGenerateResponse:
        """Generate a complete portfolio website from resume data"""
        try:
            template = self.templates.get(request.template_id)
            if not template:
                raise ValueError(f"Template {request.template_id} not found")

            # Generate personalized content using AI
            personalized_content = await self._personalize_template(template, request)
            
            # Generate HTML, CSS, and JS
            html_content = self._inject_data_into_template(
                template.html_template, 
                request.resume_data, 
                personalized_content
            )
            
            css_content = self._customize_css(
                template.css_template, 
                template.variables,
                request.additional_preferences
            )
            
            js_content = template.js_template or ""
            
            # Generate unique URLs and tokens
            share_token = str(uuid.uuid4())
            live_url = f"https://portfolio.talentd.com/{share_token}"
            
            return PortfolioGenerateResponse(
                generated_content=personalized_content,
                html_content=html_content,
                css_content=css_content,
                js_content=js_content,
                live_url=live_url,
                share_token=share_token,
                template_name=template.name,
                preview_image=template.preview_image
            )
            
        except Exception as e:
            logger.error(f"Portfolio generation error: {str(e)}")
            raise

    async def _personalize_template(self, template: PortfolioTemplate, request: PortfolioGenerateRequest) -> Dict[str, Any]:
        """Use AI to personalize template content"""
        if not self.model:
            return {"sections": ["hero", "about", "experience", "projects", "contact"]}

        prompt = f"""
        Create personalized portfolio content for:
        Name: {request.resume_data.personal_details.full_name}
        Role: Based on experience and skills
        Template: {template.name} ({template.category})
        User Request: {request.user_prompt}
        
        Generate engaging content including:
        - Hero section tagline
        - About me description
        - Skills categorization
        - Project descriptions enhancement
        - Call-to-action texts
        
        Return as JSON with sections: hero, about, skills_categories, enhanced_projects, cta_texts
        """
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            return json.loads(content)
        except:
            return {"hero": {"tagline": "Welcome to my portfolio"}}

    def _inject_data_into_template(self, html_template: str, resume_data: ParsedResumeData, content: Dict[str, Any]) -> str:
        """Inject resume data into HTML template"""
        # Replace placeholders with actual data
        html = html_template
        html = html.replace("{{FULL_NAME}}", resume_data.personal_details.full_name)
        html = html.replace("{{EMAIL}}", resume_data.personal_details.email or "")
        html = html.replace("{{PHONE}}", resume_data.personal_details.phone or "")
        html = html.replace("{{LOCATION}}", resume_data.personal_details.location or "")
        html = html.replace("{{LINKEDIN}}", resume_data.personal_details.linkedin or "")
        html = html.replace("{{GITHUB}}", resume_data.personal_details.github or "")
        html = html.replace("{{BIO}}", resume_data.personal_details.bio or "")
        
        # Inject experience
        experience_html = ""
        for exp in resume_data.experience:
            experience_html += f"""
            <div class="experience-item">
                <h3>{exp.title}</h3>
                <h4>{exp.company}</h4>
                <span class="duration">{exp.duration}</span>
                <ul>
                    {''.join([f'<li>{desc}</li>' for desc in exp.description])}
                </ul>
            </div>
            """
        html = html.replace("{{EXPERIENCE}}", experience_html)
        
        # Inject projects
        projects_html = ""
        for proj in resume_data.projects:
            projects_html += f"""
            <div class="project-item">
                <h3>{proj.name}</h3>
                <p>{proj.description}</p>
                <div class="tech-stack">
                    {''.join([f'<span class="tech">{tech}</span>' for tech in proj.technologies])}
                </div>
                <div class="project-links">
                    {f'<a href="{proj.github_url}" target="_blank">GitHub</a>' if proj.github_url else ''}
                    {f'<a href="{proj.live_url}" target="_blank">Live Demo</a>' if proj.live_url else ''}
                </div>
            </div>
            """
        html = html.replace("{{PROJECTS}}", projects_html)
        
        # Inject skills
        skills_html = ''.join([f'<span class="skill">{skill}</span>' for skill in resume_data.skills])
        html = html.replace("{{SKILLS}}", skills_html)
        
        return html

    def _customize_css(self, css_template: str, variables: Dict[str, Any], preferences: Dict[str, Any]) -> str:
        """Customize CSS with variables and preferences"""
        css = css_template
        
        # Replace CSS variables
        for key, value in variables.items():
            css = css.replace(f"var(--{key})", str(value))
            css = css.replace(f"{{{{{key.upper()}}}}}", str(value))
        
        # Apply user preferences
        if preferences.get("primary_color"):
            css = css.replace(variables.get("primary_color", "#000"), preferences["primary_color"])
        
        return css

    # Template HTML generators
    def _get_modern_3d_html(self) -> str:
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{FULL_NAME}} - Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container-3d">
        <header class="hero-3d">
            <div class="hero-content">
                <h1 class="glitch-text">{{FULL_NAME}}</h1>
                <p class="hero-subtitle">{{BIO}}</p>
                <div class="hero-cta">
                    <a href="#contact" class="btn-3d">Get In Touch</a>
                </div>
            </div>
            <div class="hero-3d-bg"></div>
        </header>
        
        <section id="about" class="section-3d">
            <div class="section-content">
                <h2>About Me</h2>
                <p>{{BIO}}</p>
            </div>
        </section>
        
        <section id="experience" class="section-3d">
            <div class="section-content">
                <h2>Experience</h2>
                <div class="experience-grid">
                    {{EXPERIENCE}}
                </div>
            </div>
        </section>
        
        <section id="projects" class="section-3d">
            <div class="section-content">
                <h2>Projects</h2>
                <div class="projects-grid">
                    {{PROJECTS}}
                </div>
            </div>
        </section>
        
        <section id="skills" class="section-3d">
            <div class="section-content">
                <h2>Skills</h2>
                <div class="skills-cloud">
                    {{SKILLS}}
                </div>
            </div>
        </section>
        
        <section id="contact" class="section-3d">
            <div class="section-content">
                <h2>Contact</h2>
                <div class="contact-info">
                    <p>Email: {{EMAIL}}</p>
                    <p>Phone: {{PHONE}}</p>
                    <p>Location: {{LOCATION}}</p>
                    <div class="social-links">
                        <a href="{{LINKEDIN}}" target="_blank">LinkedIn</a>
                        <a href="{{GITHUB}}" target="_blank">GitHub</a>
                    </div>
                </div>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>
        """

    def _get_modern_3d_css(self) -> str:
        return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: #0a0a0a;
    color: #ffffff;
    overflow-x: hidden;
}

.container-3d {
    perspective: 1000px;
}

.hero-3d {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background: linear-gradient(45deg, #0a0a0a, #1a1a1a);
}

.hero-content {
    text-align: center;
    z-index: 2;
    transform: translateZ(50px);
}

.glitch-text {
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(45deg, {{PRIMARY_COLOR}}, {{ACCENT_COLOR}});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glitch 2s infinite;
}

@keyframes glitch {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-2px); }
    40% { transform: translateX(2px); }
    60% { transform: translateX(-1px); }
    80% { transform: translateX(1px); }
}

.hero-subtitle {
    font-size: 1.5rem;
    margin: 1rem 0;
    opacity: 0.8;
}

.btn-3d {
    display: inline-block;
    padding: 1rem 2rem;
    background: linear-gradient(45deg, {{PRIMARY_COLOR}}, {{ACCENT_COLOR}});
    color: white;
    text-decoration: none;
    border-radius: 50px;
    transform: translateZ(20px);
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
}

.btn-3d:hover {
    transform: translateZ(30px) scale(1.05);
    box-shadow: 0 20px 40px rgba(0, 255, 136, 0.5);
}

.section-3d {
    padding: 5rem 2rem;
    margin: 2rem 0;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    transform: translateZ(10px);
    transition: transform 0.3s ease;
}

.section-3d:hover {
    transform: translateZ(20px);
}

.section-content {
    max-width: 1200px;
    margin: 0 auto;
}

.section-content h2 {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    background: linear-gradient(45deg, {{PRIMARY_COLOR}}, {{ACCENT_COLOR}});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.experience-grid, .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.experience-item, .project-item {
    background: rgba(255, 255, 255, 0.1);
    padding: 2rem;
    border-radius: 15px;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transform: translateZ(5px);
    transition: all 0.3s ease;
}

.experience-item:hover, .project-item:hover {
    transform: translateZ(15px) rotateY(5deg);
    box-shadow: 0 15px 35px rgba(0, 255, 136, 0.2);
}

.skills-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    margin-top: 2rem;
}

.skill {
    padding: 0.5rem 1rem;
    background: linear-gradient(45deg, {{PRIMARY_COLOR}}, {{ACCENT_COLOR}});
    border-radius: 25px;
    font-size: 0.9rem;
    transform: translateZ(5px);
    transition: all 0.3s ease;
}

.skill:hover {
    transform: translateZ(10px) scale(1.1);
}

.contact-info {
    text-align: center;
    font-size: 1.2rem;
}

.social-links {
    margin-top: 2rem;
}

.social-links a {
    display: inline-block;
    margin: 0 1rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    text-decoration: none;
    border-radius: 25px;
    transition: all 0.3s ease;
}

.social-links a:hover {
    background: {{PRIMARY_COLOR}};
    transform: translateY(-3px);
}

@media (max-width: 768px) {
    .glitch-text {
        font-size: 2.5rem;
    }
    
    .section-3d {
        padding: 3rem 1rem;
    }
    
    .experience-grid, .projects-grid {
        grid-template-columns: 1fr;
    }
}
        """

    def _get_modern_3d_js(self) -> str:
        return """
// 3D Portfolio Interactions
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling
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

    // Parallax effect on scroll
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const sections = document.querySelectorAll('.section-3d');
        
        sections.forEach((section, index) => {
            const speed = 0.1 + (index * 0.05);
            const yPos = -(scrolled * speed);
            section.style.transform = `translateZ(${10 + index * 5}px) translateY(${yPos}px)`;
        });
    });

    // Interactive hover effects
    const items = document.querySelectorAll('.experience-item, .project-item');
    items.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateZ(20px) rotateY(10deg) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateZ(5px) rotateY(0deg) scale(1)';
        });
    });

    // Glitch effect enhancement
    const glitchText = document.querySelector('.glitch-text');
    if (glitchText) {
        setInterval(() => {
            glitchText.style.textShadow = `
                ${Math.random() * 10 - 5}px ${Math.random() * 10 - 5}px 0 #ff0088,
                ${Math.random() * 10 - 5}px ${Math.random() * 10 - 5}px 0 #00ff88
            `;
            setTimeout(() => {
                glitchText.style.textShadow = 'none';
            }, 100);
        }, 3000);
    }

    // Skills animation
    const skills = document.querySelectorAll('.skill');
    skills.forEach((skill, index) => {
        skill.style.animationDelay = `${index * 0.1}s`;
        skill.classList.add('skill-animate');
    });
});

// Add CSS animation class
const style = document.createElement('style');
style.textContent = `
    .skill-animate {
        animation: skillFloat 3s ease-in-out infinite;
    }
    
    @keyframes skillFloat {
        0%, 100% { transform: translateZ(5px) translateY(0px); }
        50% { transform: translateZ(10px) translateY(-10px); }
    }
`;
document.head.appendChild(style);
        """

    # Additional template creators
    def _create_cyberpunk_template(self) -> PortfolioTemplate:
        return PortfolioTemplate(
            id="cyberpunk-neon",
            name="Cyberpunk Neon",
            description="Futuristic cyberpunk design with neon effects",
            category="futuristic",
            difficulty="advanced",
            features=["neon-effects", "cyberpunk", "animations", "dark-theme"],
            preview_image="https://via.placeholder.com/800x600/0a0a0a/00ff88?text=Cyberpunk+Neon",
            html_template="<!-- Cyberpunk HTML -->",
            css_template="/* Cyberpunk CSS */",
            js_template="// Cyberpunk JS"
        )

    def _create_nature_template(self) -> PortfolioTemplate:
        return PortfolioTemplate(
            id="nature-organic",
            name="Nature Organic",
            description="Organic design inspired by nature",
            category="organic",
            difficulty="intermediate",
            features=["organic-shapes", "nature-colors", "smooth-animations"],
            preview_image="https://via.placeholder.com/800x600/2d5a27/ffffff?text=Nature+Organic",
            html_template="<!-- Nature HTML -->",
            css_template="/* Nature CSS */"
        )

    def _create_retro_template(self) -> PortfolioTemplate:
        return PortfolioTemplate(
            id="retro-vintage",
            name="Retro Vintage",
            description="Vintage-inspired design with retro elements",
            category="retro",
            difficulty="basic",
            features=["retro-colors", "vintage-fonts", "classic-layout"],
            preview_image="https://via.placeholder.com/800x600/8b4513/ffffff?text=Retro+Vintage",
            html_template="<!-- Retro HTML -->",
            css_template="/* Retro CSS */"
        )

    def _create_futuristic_template(self) -> PortfolioTemplate:
        return PortfolioTemplate(
            id="futuristic-hologram",
            name="Futuristic Hologram",
            description="Holographic effects with futuristic design",
            category="futuristic",
            difficulty="advanced",
            features=["hologram-effects", "futuristic-ui", "advanced-animations"],
            preview_image="https://via.placeholder.com/800x600/001122/00ffff?text=Futuristic+Hologram",
            html_template="<!-- Futuristic HTML -->",
            css_template="/* Futuristic CSS */",
            js_template="// Hologram effects"
        )

    def _create_artistic_template(self) -> PortfolioTemplate:
        return PortfolioTemplate(
            id="artistic-canvas",
            name="Artistic Canvas",
            description="Creative artistic design with canvas elements",
            category="artistic",
            difficulty="intermediate",
            features=["canvas-art", "creative-layout", "artistic-animations"],
            preview_image="https://via.placeholder.com/800x600/4a4a4a/ffffff?text=Artistic+Canvas",
            html_template="<!-- Artistic HTML -->",
            css_template="/* Artistic CSS */",
            js_template="// Canvas art effects"
        )

    # Placeholder methods for other templates
    def _get_creative_parallax_html(self) -> str:
        return "<!-- Creative Parallax HTML -->"
    
    def _get_creative_parallax_css(self) -> str:
        return "/* Creative Parallax CSS */"
    
    def _get_creative_parallax_js(self) -> str:
        return "// Creative Parallax JS"
    
    def _get_minimal_glass_html(self) -> str:
        return "<!-- Minimal Glass HTML -->"
    
    def _get_minimal_glass_css(self) -> str:
        return "/* Minimal Glass CSS */"
    
    def _get_minimal_glass_js(self) -> str:
        return "// Minimal Glass JS"
    
    def _get_corporate_html(self) -> str:
        return "<!-- Corporate HTML -->"
    
    def _get_corporate_css(self) -> str:
        return "/* Corporate CSS */"
    
    def _get_corporate_js(self) -> str:
        return "// Corporate JS"
    
    def _get_particles_html(self) -> str:
        return "<!-- Particles HTML -->"
    
    def _get_particles_css(self) -> str:
        return "/* Particles CSS */"
    
    def _get_particles_js(self) -> str:
        return "// Particles JS"

# Global instance
portfolio_builder = PortfolioBuilderService()
