import random
import re

def optimize_keywords(resume_text, job_desc):
    """Optimize resume keywords for ATS and relevance"""
    
    job_words = set(job_desc.lower().split())
    resume_words = set(resume_text.lower().split())
    
    missing_keywords = job_words - resume_words
    missing_keywords = [w for w in missing_keywords if len(w) > 3]
    
    tips = [
        "Use 'Required Skills' section early in your resume",
        "Include metrics and quantifiable achievements",
        "Use the exact job title mentioned in the posting",
        "Add relevant certifications and awards",
        "Use proper formatting with clear section headers",
        "Include keywords naturally in your work experience",
        "Customize your resume for each job posting"
    ]
    
    optimized_text = resume_text
    for keyword in missing_keywords[:5]:
        if keyword not in optimized_text.lower():
            optimized_text += f"\n\n• Proficient in {keyword}"
    
    return {
        "keywords_to_add": missing_keywords[:10],
        "tips": random.sample(tips, min(3, len(tips))),
        "optimized_text": optimized_text
    }

def generate_interview_questions(resume_text, job_title, num_questions=7, difficulty="Intermediate"):
    """Generate AI-based interview questions"""
    
    # Try to import extract_skills, fallback if not available
    try:
        from utils.extract import extract_skills
        skills = extract_skills(resume_text)
    except:
        skills = ["your technical skills"]
    
    questions = [
        {
            "question": f"Tell us about your experience with {', '.join(skills[:2] if skills else ['your technical skills'])}",
            "category": "Technical Experience",
            "sample_answer": f"I have worked extensively with {', '.join(skills[:2] if skills else ['various technologies'])} in production environments. I've built scalable solutions and mentored junior team members.",
            "evaluation_criteria": "Look for concrete examples, problem-solving approach, and communication clarity"
        },
        {
            "question": f"How would you approach a {job_title.lower()} role differently from your current experience?",
            "category": "Career Growth",
            "sample_answer": f"This role appeals to me because it combines my expertise in {', '.join(skills[:1] if skills else ['technology'])} with new challenges. I'm excited to contribute to this team and grow in this domain.",
            "evaluation_criteria": "Assess alignment with role, enthusiasm, and realistic expectations"
        },
        {
            "question": "Describe a challenging project where you had to learn a new technology quickly",
            "category": "Adaptability",
            "sample_answer": "When faced with an unfamiliar technology, I followed a structured approach: researched documentation, took online courses, and started with small implementations before full integration.",
            "evaluation_criteria": "Demonstrates learning ability, problem-solving, and initiative"
        },
        {
            "question": "How do you stay updated with the latest developments in your field?",
            "category": "Professional Development",
            "sample_answer": "I actively follow industry blogs, participate in tech communities, contribute to open-source projects, and regularly take online courses to stay current.",
            "evaluation_criteria": "Shows commitment to continuous learning and growth mindset"
        },
        {
            "question": f"What attracted you most to this {job_title} position?",
            "category": "Motivation",
            "sample_answer": "This role is aligned with my career goals and the company's mission resonates with me. I'm particularly interested in the technical challenges and the opportunity to work with a talented team.",
            "evaluation_criteria": "Check for genuine interest and research about the company"
        },
        {
            "question": "Tell us about a time you had a conflict with a team member. How did you resolve it?",
            "category": "Soft Skills",
            "sample_answer": "I communicated openly to understand their perspective, found common ground, and collaborated on a solution that satisfied both parties and benefited the project.",
            "evaluation_criteria": "Demonstrates communication, empathy, and problem-solving"
        },
        {
            "question": "What are your salary expectations for this role?",
            "category": "Compensation",
            "sample_answer": "Based on my experience and market research, I'm looking for a range of [X-Y]. I'm open to discussion based on the complete package including benefits.",
            "evaluation_criteria": "Shows realistic expectations and negotiation skills"
        }
    ]
    
    return questions[:num_questions]

def suggest_alternative_roles(resume_text):
    """Suggest alternative career paths based on skills"""
    
    try:
        from utils.extract import extract_skills, SKILLS_DB
        from utils.experience import classify_experience_level, estimate_experience_years
        skills = extract_skills(resume_text)
        exp_level = classify_experience_level(estimate_experience_years(resume_text))
    except:
        skills = []
        exp_level = "Mid-Level"
    
    role_mappings = {
        ("python", "data science"): {
            "role": "Machine Learning Engineer",
            "description": "Develop and deploy machine learning models",
            "matching_skills": ["python", "data science"],
            "missing_skills": ["deep learning", "tensorflow", "mlops"]
        },
        ("java",): {
            "role": "Backend Developer",
            "description": "Build robust server-side applications",
            "matching_skills": ["java"],
            "missing_skills": ["spring framework", "microservices", "aws"]
        },
        ("react",): {
            "role": "Frontend Developer",
            "description": "Create interactive web interfaces",
            "matching_skills": ["react", "javascript"],
            "missing_skills": ["typescript", "testing", "performance optimization"]
        },
        ("sql", "data science"): {
            "role": "Data Analyst",
            "description": "Analyze and visualize data for business insights",
            "matching_skills": ["sql", "data science"],
            "missing_skills": ["tableau", "power bi", "business acumen"]
        },
    }
    
    suggestions = []
    
    for skill_combo, role_info in role_mappings.items():
        if all(skill in skills for skill in skill_combo):
            match_score = len([s for s in skill_combo if s in skills]) / len(skill_combo) * 100
            suggestions.append({
                "role": role_info["role"],
                "description": role_info["description"],
                "match_score": int(match_score),
                "matching_skills": role_info["matching_skills"],
                "missing_skills": role_info["missing_skills"]
            })
    
    if not suggestions:
        suggestions.append({
            "role": "Full Stack Developer",
            "description": "Build complete web applications",
            "match_score": 70,
            "matching_skills": skills[:3] if skills else ["skills"],
            "missing_skills": ["full stack framework", "DevOps basics"]
        })
    
    return suggestions[:5]

def optimize_email(email_data):
    """Generate professional job application email"""
    
    template = f"""Subject: Application for {email_data['job_title']} at {email_data['company']}

Dear {email_data['hr_name']},

I am writing to express my strong interest in the {email_data['job_title']} position at {email_data['company']}. With {email_data['experience']} years of professional experience, I am confident in my ability to contribute significantly to your team.

Throughout my career, I have developed a strong foundation in my field and have consistently delivered results. My key achievements include:
- {email_data['achievements'].split(chr(10))[0] if email_data['achievements'] else 'Successfully managed multiple projects'}
- Led cross-functional teams to deliver high-impact solutions
- Consistently exceeded performance targets and KPIs

I am particularly drawn to {email_data['company']} because of your innovative approach and commitment to excellence. I am excited about the opportunity to bring my skills and experience to your organization and contribute to your continued success.

My resume is attached for your review. I would welcome the opportunity to discuss how my background, skills, and enthusiasms align with the needs of your team. I am available for an interview at your convenience.

Thank you for considering my application. I look forward to the opportunity to speak with you soon.

Best regards,
{email_data['your_name']}
"""
    
    return template.strip()

def generate_ats_score(resume_text, job_desc):
    """Generate ATS (Applicant Tracking System) compatibility score"""
    
    score = 0
    
    if "contact" in resume_text.lower() or "email" in resume_text.lower():
        score += 10
    
    if "experience" in resume_text.lower():
        score += 10
    
    if "skills" in resume_text.lower():
        score += 10
    
    if "education" in resume_text.lower():
        score += 10
    
    try:
        from utils.extract import extract_skills, match_job_skills
        resume_skills = extract_skills(resume_text)
        job_match = match_job_skills(resume_skills, job_desc)
        score += job_match * 0.5
    except:
        score += 25
    
    sections = ["summary", "objective", "certification", "project", "award"]
    for section in sections:
        if section in resume_text.lower():
            score += 2
    
    if len(resume_text) > 500:
        score += 5
    
    return min(100, score)
