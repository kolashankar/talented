from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models import FooterPage
from database import get_database

footer_router = APIRouter(prefix="/pages", tags=["footer-pages"])

@footer_router.get("/{slug}")
async def get_page_by_slug(slug: str):
    """Get a page by its slug"""
    try:
        db = await get_database()
        
        page = await db.footer_pages.find_one({"slug": slug, "is_published": True})
        if not page:
            raise HTTPException(status_code=404, detail="Page not found")
        
        return {"page": page}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

def convert_objectid_to_str(doc):
    """Convert MongoDB ObjectId to string for JSON serialization"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@footer_router.get("/")
async def get_all_pages():
    """Get all published footer pages"""
    try:
        db = await get_database()
        
        pages = await db.footer_pages.find({"is_published": True}).sort("title", 1).to_list(100)
        
        # Convert ObjectIds to strings
        pages = [convert_objectid_to_str(page) for page in pages]
        
        return {"pages": pages}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pages: {str(e)}")

# Initialize default footer pages
async def initialize_footer_pages():
    """Initialize default footer pages"""
    try:
        db = await get_database()
        
        default_pages = [
            {
                "title": "Privacy Policy",
                "slug": "privacy-policy",
                "content": """
<h1>Privacy Policy</h1>
<p>Last updated: January 2024</p>

<h2>Information We Collect</h2>
<p>We collect information you provide directly to us, such as when you create an account, apply for jobs, or contact us.</p>

<h3>Personal Information</h3>
<ul>
<li>Name and contact information</li>
<li>Resume and profile information</li>
<li>Job preferences and search history</li>
<li>Communication records</li>
</ul>

<h2>How We Use Your Information</h2>
<p>We use the information we collect to:</p>
<ul>
<li>Provide, maintain, and improve our services</li>
<li>Match you with relevant job opportunities</li>
<li>Communicate with you about our services</li>
<li>Analyze usage patterns to enhance user experience</li>
</ul>

<h2>Information Sharing</h2>
<p>We may share your information with:</p>
<ul>
<li>Employers when you apply for jobs</li>
<li>Service providers who assist in our operations</li>
<li>Legal authorities when required by law</li>
</ul>

<h2>Data Security</h2>
<p>We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.</p>

<h2>Your Rights</h2>
<p>You have the right to:</p>
<ul>
<li>Access and update your personal information</li>
<li>Delete your account and associated data</li>
<li>Opt-out of marketing communications</li>
<li>Request a copy of your data</li>
</ul>

<h2>Contact Us</h2>
<p>If you have questions about this Privacy Policy, please contact us at privacy@talentd.com</p>
                """,
                "meta_description": "TalentD Privacy Policy - Learn how we collect, use, and protect your personal information."
            },
            {
                "title": "Terms of Service",
                "slug": "terms-of-service",
                "content": """
<h1>Terms of Service</h1>
<p>Last updated: January 2024</p>

<h2>Acceptance of Terms</h2>
<p>By accessing or using TalentD's services, you agree to be bound by these Terms of Service.</p>

<h2>Description of Service</h2>
<p>TalentD is a career platform that connects job seekers with employers, provides career resources, and offers professional development tools.</p>

<h2>User Accounts</h2>
<h3>Registration</h3>
<ul>
<li>You must provide accurate and complete information</li>
<li>You are responsible for maintaining account security</li>
<li>One account per person</li>
</ul>

<h3>Prohibited Activities</h3>
<ul>
<li>Posting false or misleading information</li>
<li>Harassing other users</li>
<li>Violating intellectual property rights</li>
<li>Using automated systems to scrape content</li>
</ul>

<h2>Content and Intellectual Property</h2>
<p>Users retain ownership of their content but grant TalentD a license to use it for service operation.</p>

<h2>Privacy</h2>
<p>Your privacy is important to us. Please review our Privacy Policy to understand our practices.</p>

<h2>Termination</h2>
<p>We may terminate accounts that violate these terms or for other business reasons.</p>

<h2>Disclaimer</h2>
<p>Services are provided "as is" without warranties. We are not responsible for job placement outcomes.</p>

<h2>Contact Information</h2>
<p>For questions about these Terms, contact us at legal@talentd.com</p>
                """,
                "meta_description": "TalentD Terms of Service - Understand the rules and regulations for using our platform."
            },
            {
                "title": "Support & Help",
                "slug": "support",
                "content": """
<h1>Support & Help</h1>
<p>Need help? We're here to assist you with any questions or issues.</p>

<h2>Frequently Asked Questions</h2>

<h3>Account & Profile</h3>
<h4>How do I create an account?</h4>
<p>Click "Sign Up" and follow the registration process. You can register with email or use Google authentication.</p>

<h4>How do I update my profile?</h4>
<p>Go to your Profile section and click "Edit Profile" to update your information.</p>

<h3>Job Applications</h3>
<h4>How do I apply for jobs?</h4>
<p>Browse jobs and click "Apply Now" on positions that interest you. Make sure your profile is complete.</p>

<h4>Can I track my applications?</h4>
<p>Yes, visit your Dashboard to see all your job applications and their status.</p>

<h3>Resume & Portfolio</h3>
<h4>How does the Resume Reviewer work?</h4>
<p>Upload your resume and our AI will analyze it, providing feedback and suggestions for improvement.</p>

<h4>Can I create multiple portfolios?</h4>
<p>Yes, you can create portfolios using our different templates to showcase your work effectively.</p>

<h2>DSA Practice</h2>
<h4>How do I solve DSA problems?</h4>
<p>Go to DSA Corner, select a problem, and use our built-in code editor to solve it.</p>

<h4>Can I see solutions to problems?</h4>
<p>Solutions are available after you attempt the problem. You can also participate in discussions.</p>

<h2>Contact Support</h2>
<p>Still need help? Reach out to us:</p>
<ul>
<li><strong>Email:</strong> support@talentd.com</li>
<li><strong>Response Time:</strong> We typically respond within 24 hours</li>
<li><strong>Business Hours:</strong> Monday-Friday, 9 AM - 6 PM IST</li>
</ul>

<h3>Report Issues</h3>
<p>Found a bug or technical issue? Please include:</p>
<ul>
<li>Description of the problem</li>
<li>Steps to reproduce the issue</li>
<li>Browser and device information</li>
<li>Screenshots if applicable</li>
</ul>

<h2>Feature Requests</h2>
<p>Have an idea for improving TalentD? We'd love to hear from you at feedback@talentd.com</p>
                """,
                "meta_description": "Get help and support for using TalentD. Find answers to common questions and contact information."
            },
            {
                "title": "About Us",
                "slug": "about",
                "content": """
<h1>About TalentD</h1>
<p>Empowering careers through technology and connecting talent with opportunities.</p>

<h2>Our Mission</h2>
<p>To democratize access to career opportunities and provide tools that help professionals grow, learn, and succeed in their chosen fields.</p>

<h2>What We Offer</h2>

<h3>For Job Seekers</h3>
<ul>
<li><strong>Job Discovery:</strong> Find relevant jobs and internships from top companies</li>
<li><strong>Resume Enhancement:</strong> AI-powered resume review and optimization</li>
<li><strong>Portfolio Builder:</strong> Create stunning portfolios to showcase your work</li>
<li><strong>Skill Development:</strong> Practice DSA problems and read expert articles</li>
<li><strong>Career Guidance:</strong> Access roadmaps and industry insights</li>
</ul>

<h3>For Employers</h3>
<ul>
<li><strong>Talent Pool:</strong> Access to qualified and motivated candidates</li>
<li><strong>Easy Posting:</strong> Simple job and internship posting process</li>
<li><strong>Company Profiles:</strong> Showcase your company culture and values</li>
</ul>

<h2>Our Values</h2>
<ul>
<li><strong>Transparency:</strong> Clear processes and honest communication</li>
<li><strong>Innovation:</strong> Using cutting-edge technology to solve career challenges</li>
<li><strong>Accessibility:</strong> Making career tools available to everyone</li>
<li><strong>Growth:</strong> Supporting continuous learning and development</li>
</ul>

<h2>Technology Stack</h2>
<p>Built with modern technologies to ensure reliability and performance:</p>
<ul>
<li>React.js for dynamic user interfaces</li>
<li>FastAPI for robust backend services</li>
<li>MongoDB for scalable data storage</li>
<li>AI/ML integration for smart features</li>
</ul>

<h2>Team</h2>
<p>Our team consists of experienced developers, career counselors, and industry experts who are passionate about helping people succeed in their careers.</p>

<h2>Contact Us</h2>
<p>Have questions or want to learn more? Reach out to us:</p>
<ul>
<li><strong>Email:</strong> hello@talentd.com</li>
<li><strong>Business Inquiries:</strong> business@talentd.com</li>
<li><strong>Press:</strong> press@talentd.com</li>
</ul>
                """,
                "meta_description": "Learn about TalentD - our mission, values, and commitment to empowering careers through technology."
            },
            {
                "title": "Careers",
                "slug": "careers",
                "content": """
<h1>Join Our Team</h1>
<p>Build the future of career development with us.</p>

<h2>Why Work at TalentD?</h2>
<ul>
<li><strong>Impact:</strong> Help millions of people advance their careers</li>
<li><strong>Innovation:</strong> Work with cutting-edge technologies</li>
<li><strong>Growth:</strong> Continuous learning and development opportunities</li>
<li><strong>Culture:</strong> Collaborative and inclusive work environment</li>
<li><strong>Benefits:</strong> Competitive compensation and comprehensive benefits</li>
</ul>

<h2>Current Openings</h2>
<p>We're always looking for talented individuals to join our team. Check our job listings for current opportunities.</p>

<h3>Remote-First Culture</h3>
<p>We believe in flexibility and offer remote work options to help you achieve work-life balance.</p>

<h2>Apply</h2>
<p>Interested in joining us? Send your resume and a cover letter to careers@talentd.com</p>

<p>We are an equal opportunity employer committed to diversity and inclusion.</p>
                """,
                "meta_description": "Join the TalentD team and help build the future of career development. View current job openings."
            },
            {
                "title": "Contact Us",
                "slug": "contact",
                "content": """
<h1>Contact Us</h1>
<p>We'd love to hear from you. Get in touch with us for any questions, feedback, or support.</p>

<h2>Get in Touch</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0;">
    <div>
        <h3>General Inquiries</h3>
        <p><strong>Email:</strong> hello@talentd.com</p>
        <p>For general questions about our platform and services.</p>
    </div>
    
    <div>
        <h3>Support</h3>
        <p><strong>Email:</strong> support@talentd.com</p>
        <p>Technical issues, account help, and user support.</p>
    </div>
    
    <div>
        <h3>Business Partnerships</h3>
        <p><strong>Email:</strong> partnerships@talentd.com</p>
        <p>Collaboration opportunities and business inquiries.</p>
    </div>
    
    <div>
        <h3>Press & Media</h3>
        <p><strong>Email:</strong> press@talentd.com</p>
        <p>Media inquiries, press releases, and interviews.</p>
    </div>
</div>

<h2>Office Hours</h2>
<p><strong>Monday - Friday:</strong> 9:00 AM - 6:00 PM (IST)</p>
<p><strong>Weekend:</strong> Limited support available</p>

<h2>Response Time</h2>
<ul>
<li><strong>Support Requests:</strong> Within 24 hours</li>
<li><strong>Business Inquiries:</strong> Within 48 hours</li>
<li><strong>General Questions:</strong> Within 72 hours</li>
</ul>

<h2>Follow Us</h2>
<p>Stay updated with the latest news and updates:</p>
<ul>
<li><strong>LinkedIn:</strong> /company/talentd</li>
<li><strong>Twitter:</strong> @talentd</li>
<li><strong>Facebook:</strong> /talentd</li>
</ul>
                """,
                "meta_description": "Contact TalentD for support, partnerships, or general inquiries. Find all our contact information here."
            }
        ]
        
        for page_data in default_pages:
            # Check if page already exists
            existing_page = await db.footer_pages.find_one({"slug": page_data["slug"]})
            if not existing_page:
                from models import FooterPage
                page = FooterPage(**page_data)
                await db.footer_pages.insert_one(page.dict())
        
        print("Footer pages initialized successfully")
        
    except Exception as e:
        print(f"Error initializing footer pages: {str(e)}")