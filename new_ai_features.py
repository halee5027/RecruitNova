import random
import re

def optimize_keywords(resume_text, job_desc):
    """Optimize resume keywords for ATS and relevance — Premium Analysis"""
    
    # --- Normalize ---
    job_words_raw = re.findall(r'\b[a-zA-Z][a-zA-Z+#./\-]{2,}\b', job_desc)
    resume_words_raw = re.findall(r'\b[a-zA-Z][a-zA-Z+#./\-]{2,}\b', resume_text)
    
    job_words = set(w.lower() for w in job_words_raw)
    resume_words = set(w.lower() for w in resume_words_raw)
    
    # Stop words
    stop_words = {
        "the", "and", "for", "with", "that", "this", "from", "have", "will",
        "your", "are", "can", "work", "team", "year", "years", "skills",
        "experience", "education", "also", "must", "should", "would", "could",
        "about", "been", "being", "into", "more", "than", "them", "then",
        "they", "their", "there", "these", "those", "what", "when", "where",
        "which", "while", "such", "each", "other", "some", "able", "well",
        "including", "within", "across", "strong", "knowledge", "using",
        "time", "role", "part", "join", "looking", "help", "plus", "like",
        "company", "position", "opportunity", "working", "related", "required",
        "preferred", "minimum", "equivalent", "bonus", "apply", "based",
    }
    
    # Find matched and missing keywords  
    matched_keywords = list(job_words & resume_words - stop_words)
    missing_keywords = list(job_words - resume_words - stop_words)
    missing_keywords = [w for w in missing_keywords if len(w) > 2 and not w.isdigit()]
    
    # Match percentage
    total_job_keywords = len(job_words - stop_words)
    match_percentage = int((len(matched_keywords) / max(total_job_keywords, 1)) * 100)
    
    # --- Categorize keywords ---
    tech_indicators = {
        "python", "java", "javascript", "typescript", "react", "angular", "vue",
        "node", "django", "flask", "spring", "sql", "nosql", "mongodb", "postgresql",
        "mysql", "redis", "graphql", "rest", "api", "microservices", "docker",
        "kubernetes", "aws", "azure", "gcp", "terraform", "jenkins", "git",
        "c++", "c#", "rust", "golang", "scala", "kotlin", "swift", "ruby",
        "html", "css", "sass", "webpack", "vite", "nextjs", "tailwind",
        "tensorflow", "pytorch", "pandas", "numpy", "spark", "hadoop", "kafka",
        "elasticsearch", "linux", "unix", "bash", "powershell", "nginx",
        "agile", "scrum", "kanban", "jira", "confluence", "ci/cd", "devops",
        "machine", "learning", "deep", "data", "analytics", "cloud", "native",
        "serverless", "lambda", "blockchain", "cybersecurity",
    }
    
    tool_indicators = {
        "figma", "sketch", "photoshop", "illustrator", "tableau", "powerbi",
        "excel", "word", "slack", "notion", "trello", "asana", "github",
        "gitlab", "bitbucket", "postman", "swagger", "datadog", "splunk",
        "grafana", "prometheus", "sentry", "newrelic", "salesforce", "hubspot",
        "zapier", "selenium", "cypress", "playwright", "jest", "mocha",
        "pytest", "junit", "maven", "gradle", "npm", "yarn", "pip",
    }
    
    soft_indicators = {
        "leadership", "communication", "collaboration", "teamwork", "problem-solving",
        "analytical", "creative", "innovative", "detail-oriented", "proactive",
        "adaptable", "flexible", "organized", "strategic", "critical", "thinking",
        "mentoring", "coaching", "stakeholder", "presentation", "negotiation",
        "interpersonal", "self-motivated", "driven", "passionate", "empathetic",
        "ownership", "accountability", "prioritization", "multitasking",
    }
    
    def categorize(keywords):
        technical = []
        tools = []
        soft_skills = []
        other = []
        for kw in keywords:
            kw_l = kw.lower()
            if kw_l in tech_indicators or any(t in kw_l for t in ["develop", "engineer", "architect", "program"]):
                technical.append(kw)
            elif kw_l in tool_indicators:
                tools.append(kw)
            elif kw_l in soft_indicators:
                soft_skills.append(kw)
            else:
                other.append(kw)
        return technical, tools, soft_skills, other
    
    # Prioritize capitalized words from job desc (proper nouns/technologies)
    job_desc_original_words = job_desc.split()
    capitalized_job_words = set(w.lower() for w in job_desc_original_words if len(w) > 2 and w[0].isupper())
    
    priority = [kw for kw in missing_keywords if kw in capitalized_job_words]
    normal = [kw for kw in missing_keywords if kw not in capitalized_job_words]
    final_missing = priority[:8] + normal[:7]
    
    missing_tech, missing_tools, missing_soft, missing_other = categorize(final_missing)
    matched_tech, matched_tools, matched_soft, matched_other = categorize(matched_keywords)
    
    # --- ATS Score Estimation (before and after) ---
    ats_before = min(95, max(15, match_percentage + random.randint(-5, 5)))
    # Estimate after: adding missing keywords would improve match
    boost = min(30, len(final_missing) * 3)
    ats_after = min(95, ats_before + boost)
    
    # --- Keyword density analysis ---
    resume_word_count = len(resume_text.split())
    job_keyword_freq = {}
    for w in job_words_raw:
        wl = w.lower()
        if wl not in stop_words and len(wl) > 2:
            job_keyword_freq[wl] = job_keyword_freq.get(wl, 0) + 1
    
    # Top repeated job keywords (high importance)
    high_importance = sorted(job_keyword_freq.items(), key=lambda x: x[1], reverse=True)[:8]
    high_importance_missing = [(kw, count) for kw, count in high_importance if kw not in resume_words]
    
    # --- Tips ---
    tips = [
        "Place technical keywords in a dedicated 'Technical Skills' section",
        "Mirror the exact phrasing from the job description (e.g., 'CI/CD pipelines' not just 'CI/CD')",
        "Weave keywords into achievement bullets: 'Leveraged **[Keyword]** to reduce deploy time by 40%'",
        "Quantify your impact with each skill when possible",
        "Mention tools in context of results, not just as a list",
    ]
    
    # --- Smart Insertion ---
    optimized_text = resume_text
    keywords_str = ", ".join(kw.title() for kw in final_missing)
    
    skills_pattern = re.compile(r'(skills|technical skills|technologies|core competencies)', re.IGNORECASE)
    match = skills_pattern.search(optimized_text)
    
    if match:
        end_pos = match.end()
        next_newline = optimized_text.find('\n', end_pos)
        insertion_point = next_newline if next_newline != -1 else end_pos
        insertion = f"\n• Recommended Additions: {keywords_str}"
        optimized_text = optimized_text[:insertion_point] + insertion + optimized_text[insertion_point:]
    else:
        optimized_text = "RECOMMENDED SKILLS TO ADD:\n• " + keywords_str + "\n\n" + optimized_text

    return {
        "keywords_to_add": final_missing,
        "matched_keywords": matched_keywords[:15],
        "match_percentage": match_percentage,
        "ats_before": ats_before,
        "ats_after": ats_after,
        "categorized_missing": {
            "technical": missing_tech,
            "tools": missing_tools,
            "soft_skills": missing_soft,
            "other": missing_other,
        },
        "categorized_matched": {
            "technical": matched_tech,
            "tools": matched_tools,
            "soft_skills": matched_soft,
            "other": matched_other,
        },
        "high_importance_missing": high_importance_missing,
        "tips": tips,
        "optimized_text": optimized_text,
        "total_job_keywords": total_job_keywords,
        "resume_word_count": resume_word_count,
    }


def suggest_alternative_roles(resume_text):
    """Suggest alternative career paths based on skills with detailed recommendations"""
    
    try:
        from utils.extract import extract_skills
        skills = extract_skills(resume_text)
    except:
        skills = []
    
    skills_lower = set(s.lower() for s in skills)
    
    # Expanded Role Database
    role_mappings = [
        {
            "role": "Machine Learning Engineer",
            "keywords": {"python", "data", "statistics", "calculus", "linear algebra", "algorithms"},
            "description": "Develop and deploy ML models for production systems.",
            "salary_range": "$110k - $160k",
            "growth_potential": "Very High",
            "matching_skills": [],
            "missing_skills": ["TensorFlow/PyTorch", "MLOps", "Model Deployment", "Deep Learning"]
        },
        {
            "role": "Data Scientist",
            "keywords": {"python", "r", "sql", "data analysis", "visualization", "statistics"},
            "description": "Analyze complex data to help organizations make better decisions.",
            "salary_range": "$100k - $150k",
            "growth_potential": "High",
            "matching_skills": [],
            "missing_skills": ["A/B Testing", "Big Data (Spark)", "Tableau", "Featured Engineering"]
        },
        {
            "role": "Backend Developer",
            "keywords": {"java", "python", "node", "sql", "api", "database", "server", "architecture"},
            "description": "Build robust, scalable server-side applications and APIs.",
            "salary_range": "$90k - $145k",
            "growth_potential": "High",
            "matching_skills": [],
            "missing_skills": ["System Design", "Microservices", "Cloud (AWS/Azure)", "Docker/K8s"]
        },
        {
            "role": "Frontend Developer",
            "keywords": {"javascript", "react", "html", "css", "ui", "ux", "web", "design"},
            "description": "Create dynamic, responsive, and user-friendly web interfaces.",
            "salary_range": "$85k - $135k",
            "growth_potential": "High",
            "matching_skills": [],
            "missing_skills": ["TypeScript", "State Management (Redux)", "Performance Optimization", "Accessibility"]
        },
        {
            "role": "Full Stack Developer",
            "keywords": {"javascript", "python", "java", "html", "css", "sql", "react", "node"},
            "description": "Build complete web applications, handling both client and server logic.",
            "salary_range": "$95k - $150k",
            "growth_potential": "High",
            "matching_skills": [],
            "missing_skills": ["End-to-End Testing", "CI/CD", "Security Best Practices", "Cloud Deployment"]
        },
        {
            "role": "DevOps Engineer",
            "keywords": {"linux", "aws", "cloud", "automation", "scripting", "ci/cd", "jenkins"},
            "description": "Automate infrastructure, deployment, and operations.",
            "salary_range": "$105k - $160k",
            "growth_potential": "Very High",
            "matching_skills": [],
            "missing_skills": ["Kubernetes", "Terraform", "Monitoring (Prometheus/Grafana)", "Network Security"]
        },
        {
            "role": "Product Manager",
            "keywords": {"management", "strategy", "roadmap", "agile", "communication", "analysis", "user"},
            "description": "Guide the success of a product and lead the cross-functional team that is responsible for improving it.",
            "salary_range": "$110k - $170k",
            "growth_potential": "High",
            "matching_skills": [],
            "missing_skills": ["Product Strategy", "Market Research", "User Interviewing", "Data-Driven Decision Making"]
        },
        {
            "role": "Data Analyst",
            "keywords": {"sql", "excel", "data", "reporting", "tableau", "power bi", "visualization"},
            "description": "Translate numbers into plain English to help businesses make better decisions.",
            "salary_range": "$70k - $110k",
            "growth_potential": "Medium-High",
            "matching_skills": [],
            "missing_skills": ["Advanced SQL", "Python for Data Analysis", "Statistical Modeling", "Business Intelligence"]
        },
        {
            "role": "QA Automation Engineer",
            "keywords": {"testing", "automation", "python", "java", "selenium", "quality", "test"},
            "description": "Design and write programs that run automatic tests on new software.",
            "salary_range": "$80k - $130k",
            "growth_potential": "Medium-High",
            "matching_skills": [],
            "missing_skills": ["Test Frameworks (PyTest/JUnit)", "CI Integration", "Load Testing", "Mobile Testing"]
        },
        {
            "role": "Cybersecurity Analyst",
            "keywords": {"security", "network", "firewall", "vulnerability", "risk", "compliance", "linux"},
            "description": "Protect an organization's computer networks and systems.",
            "salary_range": "$95k - $155k",
            "growth_potential": "Very High",
            "matching_skills": [],
            "missing_skills": ["Ethical Hacking", "Security Tools (Splunk)", "Incident Response", "Cryptography"]
        },
         {
            "role": "Mobile Developer (iOS/Android)",
            "keywords": {"java", "kotlin", "swift", "objective-c", "mobile", "app", "ios", "android"},
            "description": "Create applications for mobile devices.",
            "salary_range": "$95k - $155k",
            "growth_potential": "High",
            "matching_skills": [],
            "missing_skills": ["React Native/Flutter", "App Store Deployment", "Mobile UI Guidelines", "Offline Storage"]
        }
    ]
    
    scored_suggestions = []
    
    for role_info in role_mappings:
        # Calculate match
        role_keywords = role_info["keywords"]
        matches = [kw for kw in role_keywords if any(kw in s for s in skills_lower)]
        role_info["matching_skills"] = matches
        
        # Heuristic scoring
        if len(role_keywords) > 0:
            match_score = int((len(matches) / len(role_keywords)) * 100)
        else:
            match_score = 0
            
        # Boost score slightly if they have > 2 matches
        if len(matches) > 2:
            match_score += 15
            
        # Cap at 95
        match_score = min(95, match_score)
        
        # Add to list if there's any relevance (non-zero match or generic fallback)
        if match_score > 20: 
             scored_suggestions.append({
                "role": role_info["role"],
                "description": role_info["description"],
                "match_score": match_score,
                "matching_skills": role_info["matching_skills"],
                "missing_skills": role_info["missing_skills"],
                "salary_range": role_info["salary_range"],
                "growth_potential": role_info["growth_potential"]
            })
    
    # Sort by score
    scored_suggestions.sort(key=lambda x: x["match_score"], reverse=True)
    
    # If no decent matches, return generic
    if not scored_suggestions:
        return []

    return scored_suggestions[:6]

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
{email_data['your_name']}"""
    
    return template.strip()

def generate_ats_score(resume_text, job_desc):
    """Generate ATS (Applicant Tracking System) compatibility score"""
    
    score = 0
    
    # Contact information (10 points)
    if "contact" in resume_text.lower() or "email" in resume_text.lower() or "@" in resume_text:
        score += 10
    
    # Experience section (10 points)
    if "experience" in resume_text.lower():
        score += 10
    
    # Skills section (10 points)
    if "skills" in resume_text.lower():
        score += 10
    
    # Education section (10 points)
    if "education" in resume_text.lower():
        score += 10
    
    # Keyword matching (up to 50 points)
    try:
        from utils.extract import extract_skills, match_job_skills
        resume_skills = extract_skills(resume_text)
        job_match = match_job_skills(resume_skills, job_desc)
        score += min(50, job_match * 0.5)
    except:
        score += 25
    
    # Additional sections (10 points)
    sections = ["summary", "objective", "certification", "project", "award"]
    for section in sections:
        if section in resume_text.lower():
            score += 2
    
    # Document length (5 points)
    if len(resume_text) > 500:
        score += 5
    
    return min(100, int(score))

def generate_interview_questions(resume_text, job_title, num_questions=5, difficulty="Intermediate"):
    """Generate tailored interview questions based on resume and job title"""
    
    try:
        from utils.extract import extract_skills
        skills = extract_skills(resume_text)
    except:
        skills = []
    
    # Question templates by category
    question_bank = {
        "Technical": [
            {"question": f"Can you explain your experience with {skills[0] if skills else 'your primary technology'}?", 
             "category": "Technical", 
             "sample_answer": "Describe specific projects, technologies used, and measurable outcomes.",
             "evaluation_criteria": "Technical depth, practical experience, problem-solving",
             "follow_up": "What challenges did you face and how did you overcome them?"},
            {"question": f"How would you design a scalable system for a {job_title} role?",
             "category": "Technical",
             "sample_answer": "Start with requirements, discuss architecture patterns, databases, caching, and monitoring.",
             "evaluation_criteria": "System design knowledge, scalability thinking",
             "follow_up": "How would you handle a sudden 10x increase in traffic?"},
            {"question": "Describe a technical problem you solved that you're proud of.",
             "category": "Technical",
             "sample_answer": "Use STAR method: describe the situation, your approach, tools used, and the result.",
             "evaluation_criteria": "Problem-solving ability, technical communication",
             "follow_up": "What would you do differently if you faced the same problem today?"},
            {"question": f"What tools and technologies do you consider essential for a {job_title}?",
             "category": "Technical",
             "sample_answer": "List relevant tools, explain why each is important, and share your experience with them.",
             "evaluation_criteria": "Industry awareness, tool proficiency",
             "follow_up": "How do you stay updated with new technologies?"},
        ],
        "Behavioral": [
            {"question": "Tell me about a time you had to work with a difficult team member.",
             "category": "Behavioral",
             "sample_answer": "Describe the situation, your approach to communication, and the positive outcome.",
             "evaluation_criteria": "Conflict resolution, teamwork, emotional intelligence",
             "follow_up": "What did you learn from that experience?"},
            {"question": "Describe a situation where you had to meet a tight deadline.",
             "category": "Behavioral",
             "sample_answer": "Explain prioritization, time management strategies, and how you delivered quality work.",
             "evaluation_criteria": "Time management, prioritization, stress handling",
             "follow_up": "How do you prevent deadline crunches in the future?"},
            {"question": "Tell me about a project that failed. What did you learn?",
             "category": "Behavioral",
             "sample_answer": "Be honest about the failure, focus on lessons learned and how you applied them.",
             "evaluation_criteria": "Self-awareness, growth mindset, accountability",
             "follow_up": "How has this experience changed your approach?"},
        ],
        "Situational": [
            {"question": f"If you were hired as a {job_title}, what would your first 90 days look like?",
             "category": "Situational",
             "sample_answer": "Break into phases: learning (30 days), contributing (60 days), leading initiatives (90 days).",
             "evaluation_criteria": "Strategic thinking, planning, initiative",
             "follow_up": "How would you measure your success?"},
            {"question": "How would you handle receiving critical feedback on your work?",
             "category": "Situational",
             "sample_answer": "Listen actively, ask clarifying questions, create an action plan for improvement.",
             "evaluation_criteria": "Receptiveness, professional maturity, growth mindset",
             "follow_up": "Can you give an example of when feedback improved your work?"},
            {"question": "If you disagreed with your manager's technical decision, what would you do?",
             "category": "Situational",
             "sample_answer": "Present data-driven alternatives respectfully, but ultimately support the team decision.",
             "evaluation_criteria": "Communication, professionalism, assertiveness",
             "follow_up": "What if the decision led to problems you predicted?"},
        ]
    }
    
    # Difficulty adjustments
    difficulty_prefix = {
        "Easy": "In simple terms, ",
        "Intermediate": "",
        "Advanced": "In depth, "
    }
    prefix = difficulty_prefix.get(difficulty, "")
    
    # Build question pool
    all_questions = []
    for category, questions in question_bank.items():
        for q in questions:
            q_copy = q.copy()
            if prefix:
                q_copy["question"] = prefix + q_copy["question"][0].lower() + q_copy["question"][1:]
            all_questions.append(q_copy)
    
    # Shuffle and select
    random.shuffle(all_questions)
    selected = all_questions[:num_questions]
    
    return selected

def estimate_salary_range(resume_text, job_title):
    """Estimate salary range based on skills and experience"""
    
    try:
        from utils.experience import estimate_experience_years
        years = estimate_experience_years(resume_text)
    except:
        years = 2
    
    try:
        from utils.extract import extract_skills
        skills = extract_skills(resume_text)
        skill_count = len(skills)
    except:
        skill_count = 5
    
    # Base salary calculation
    base_salary = 50000
    
    # Experience multiplier (5k per year, capped at 15 years)
    exp_bonus = min(years, 15) * 5000
    
    # Skills multiplier (2k per skill, capped at 20 skills)
    skill_bonus = min(skill_count, 20) * 2000
    
    # Job title premium
    title_premiums = {
        "senior": 20000,
        "lead": 25000,
        "principal": 35000,
        "architect": 30000,
        "manager": 28000,
        "director": 45000,
        "engineer": 10000,
        "developer": 8000,
        "analyst": 5000
    }
    
    title_bonus = 0
    for keyword, premium in title_premiums.items():
        if keyword in job_title.lower():
            title_bonus = max(title_bonus, premium)
    
    # Calculate range
    estimated_base = base_salary + exp_bonus + skill_bonus + title_bonus
    min_salary = int(estimated_base * 0.85)
    max_salary = int(estimated_base * 1.25)
    
    return {
        "min": f"${min_salary:,}",
        "max": f"${max_salary:,}",
        "median": f"${estimated_base:,}",
        "factors": {
            "experience_years": years,
            "skill_count": skill_count,
            "title_level": title_bonus > 0
        }
    }

def analyze_resume_strength(resume_text):
    """Analyze resume strengths and weaknesses"""
    
    strengths = []
    weaknesses = []
    score = 0
    
    # Check for quantifiable achievements
    if re.search(r'\d+%|\d+ percent|increased by|improved|reduced by', resume_text.lower()):
        strengths.append("Contains quantifiable achievements")
        score += 15
    else:
        weaknesses.append("Missing quantifiable achievements (add metrics like 'Improved performance by 30%')")
    
    # Check for action verbs
    action_verbs = ['led', 'developed', 'created', 'implemented', 'designed', 'achieved', 'managed', 'delivered']
    found_verbs = [verb for verb in action_verbs if verb in resume_text.lower()]
    if len(found_verbs) >= 3:
        strengths.append(f"Uses strong action verbs ({len(found_verbs)} found)")
        score += 10
    else:
        weaknesses.append("Use more action verbs (Led, Developed, Achieved, etc.)")
    
    # Check resume length
    word_count = len(resume_text.split())
    if 400 <= word_count <= 800:
        strengths.append(f"Appropriate length ({word_count} words)")
        score += 10
    elif word_count < 400:
        weaknesses.append(f"Resume too short ({word_count} words) - add more details")
    else:
        weaknesses.append(f"Resume too long ({word_count} words) - be more concise")
    
    # Check for key sections
    required_sections = ['experience', 'education', 'skills']
    found_sections = [sec for sec in required_sections if sec in resume_text.lower()]
    score += len(found_sections) * 10
    if len(found_sections) == 3:
        strengths.append("Contains all essential sections")
    else:
        missing = [sec for sec in required_sections if sec not in found_sections]
        weaknesses.append(f"Missing sections: {', '.join(missing)}")
    
    # Check for certifications/projects
    if 'certification' in resume_text.lower() or 'certified' in resume_text.lower():
        strengths.append("Includes certifications")
        score += 10
    
    if 'project' in resume_text.lower():
        strengths.append("Includes project details")
        score += 10
    
    # Check for technical skills diversity
    try:
        from utils.extract import extract_skills
        skills = extract_skills(resume_text)
        if len(skills) >= 8:
            strengths.append(f"Rich skill set ({len(skills)} skills)")
            score += 15
        elif len(skills) < 5:
            weaknesses.append("Add more relevant technical skills")
    except:
        pass
    
    # Final score capping
    score = min(100, score)
    
    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "overall_rating": "Excellent" if score >= 80 else "Good" if score >= 60 else "Needs Improvement"
    }

def create_learning_path(resume_text, target_role):
    """Create personalized learning path for career growth"""
    
    try:
        from utils.extract import extract_skills
        current_skills = set([s.lower() for s in extract_skills(resume_text)])
    except:
        current_skills = set()
    
    learning_paths = {
        "Machine Learning Engineer": [
            {"skill": "Python Advanced", "duration": "2 months", "resources": ["Python for Data Science", "Advanced Python Programming"]},
            {"skill": "Deep Learning", "duration": "3 months", "resources": ["Deep Learning Specialization", "Fast.ai Course"]},
            {"skill": "MLOps", "duration": "2 months", "resources": ["MLOps Course", "Model Deployment Guide"]},
            {"skill": "Cloud Platforms", "duration": "1 month", "resources": ["AWS ML Services", "Google Cloud ML"]}
        ],
        "Frontend Developer": [
            {"skill": "React Advanced", "duration": "2 months", "resources": ["React Documentation", "Advanced React Patterns"]},
            {"skill": "TypeScript", "duration": "1 month", "resources": ["TypeScript Handbook", "TypeScript Deep Dive"]},
            {"skill": "Testing", "duration": "1 month", "resources": ["Jest Testing", "React Testing Library"]},
            {"skill": "Performance Optimization", "duration": "2 weeks", "resources": ["Web Performance", "React Performance"]}
        ],
        "Backend Developer": [
            {"skill": "System Design", "duration": "2 months", "resources": ["Designing Data-Intensive Applications", "System Design Primer"]},
            {"skill": "Microservices", "duration": "1.5 months", "resources": ["Microservices Patterns", "Spring Boot Microservices"]},
            {"skill": "Database Optimization", "duration": "1 month", "resources": ["Database Internals", "SQL Performance Tuning"]},
            {"skill": "Cloud & DevOps", "duration": "1 month", "resources": ["AWS Certified Developer", "Docker & Kubernetes"]}
        ],
        "Full Stack Developer": [
            {"skill": "Frontend Frameworks", "duration": "2 months", "resources": ["React or Vue.js", "Modern JavaScript"]},
            {"skill": "Backend Technologies", "duration": "2 months", "resources": ["Node.js & Express", "RESTful APIs"]},
            {"skill": "Databases", "duration": "1 month", "resources": ["SQL & NoSQL", "MongoDB University"]},
            {"skill": "DevOps Basics", "duration": "1 month", "resources": ["Git & CI/CD", "Docker Essentials"]}
        ]
    }
    
    path = learning_paths.get(target_role, learning_paths["Full Stack Developer"])
    
    # Filter out skills the user already has
    filtered_path = []
    for item in path:
        skill_keywords = item["skill"].lower().split()
        if not any(keyword in current_skills for keyword in skill_keywords):
            filtered_path.append(item)
    
    return filtered_path if filtered_path else path
