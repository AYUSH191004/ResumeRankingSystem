"""
Create sample resumes for testing
"""
import os
from pathlib import Path

# Sample resume text
SAMPLE_RESUME_TEXT = """
John Doe
Software Engineer
Email: john.doe@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

PROFESSIONAL SUMMARY
Experienced Full-Stack Developer with 5+ years of expertise in Python, JavaScript, 
and cloud technologies. Proven track record of building scalable web applications 
and leading development teams.

TECHNICAL SKILLS
- Programming Languages: Python, JavaScript, TypeScript, Java
- Frameworks: React, Node.js, Django, FastAPI, Express.js
- Databases: PostgreSQL, MongoDB, Redis
- Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Jenkins
- Tools: Git, Jira, VS Code, Postman

WORK EXPERIENCE

Senior Software Engineer | Tech Corp Inc. | Jan 2021 - Present
- Led team of 5 engineers in developing microservices architecture
- Reduced API response time by 40% through optimization
- Implemented CI/CD pipeline reducing deployment time by 60%
- Technologies: Python, FastAPI, PostgreSQL, Docker, AWS

Software Engineer | StartupXYZ | Jun 2019 - Dec 2020
- Developed RESTful APIs serving 100K+ daily active users
- Built real-time dashboard using React and WebSockets
- Collaborated with product team on feature requirements
- Technologies: Node.js, React, MongoDB, Redis

Junior Developer | WebDev Agency | Jan 2018 - May 2019
- Created responsive web applications for clients
- Maintained and updated legacy codebases
- Technologies: JavaScript, PHP, MySQL

EDUCATION
Bachelor of Science in Computer Science
State University | 2014 - 2018
GPA: 3.7/4.0

PROJECTS
- Open Source Contributor - Contributed to popular Python libraries (500+ stars)
- Personal Blog Platform - Full-stack app with 10K+ monthly visitors
- Machine Learning Projects - Image classification using TensorFlow

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate (2022)
- Certified Scrum Master (2021)
"""

def create_sample_resume():
    """Create a sample PDF resume"""
    # For now, save as text file
    # You can convert to PDF using an online tool
    
    sample_dir = Path("backend/data/sample_data")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    sample_file = sample_dir / "sample_resume.txt"
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(SAMPLE_RESUME_TEXT)
    
    print(f"✅ Created sample resume at: {sample_file}")
    print("⚠️  Convert this to PDF using an online tool and save as sample_resume.pdf")

if __name__ == "__main__":
    create_sample_resume()