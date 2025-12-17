import streamlit as st
import pandas as pd
from utils.extract import extract_text_from_file, extract_skills, match_job_skills
from utils.experience import estimate_experience_years, experience_percentage, classify_experience_level
from utils.ranking import calculate_final_score
from utils.analyzer import analyze_resume
from users_extract import show_resume_tips, show_bonus_videos, recommend_courses_from_resume
from new_ai_features import optimize_keywords, suggest_alternative_roles, optimize_email, generate_ats_score, generate_interview_questions
from ui_components import metric_card, show_header_with_user

def show_user_dashboard():
    """Main user dashboard - PRESERVES ALL ORIGINAL FEATURES"""
    
    # Show header with user name (NO Edit Profile button here)
    show_header_with_user()
    st.markdown("---")

    with st.sidebar:
        st.markdown("""
            <style>
            /* Reduce padding inside sidebar */
            .css-1d391kg, .css-1v0mbdj, .css-1lcbmhc {
            padding-top: 10px !important;
            }
        """, unsafe_allow_html=True)           
        st.title("👤 Candidate Dashboard")
        st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)

        user_page = st.radio(
            "Select Option",
            [
                "Resume Analysis",
                "Keyword Optimization",
                "Alternative Roles",
                "Interview Prep",
                "Email Template",
                "Career Growth"
            ]
        )

    if user_page == "Resume Analysis":
        show_resume_analysis()
    elif user_page == "Keyword Optimization":
        show_keyword_optimization()
    elif user_page == "Alternative Roles":
        show_alternative_roles()
    elif user_page == "Interview Prep":
        show_interview_prep()
    elif user_page == "Email Template":
        show_email_template()
    elif user_page == "Career Growth":
        show_career_growth()


def show_resume_analysis():
    """Resume analysis - PRESERVES YOUR ORIGINAL LOGIC"""
    st.markdown("## 📄 Resume Analysis & Screening")
    st.markdown("---")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("📝 Job Description")
        job_desc = st.text_area(
            "Paste job requirements:",
            height=150,
            placeholder="Python, SQL, AWS, 3+ years experience..."
        )

    with col2:
        st.subheader("📄 Upload Resume")
        resume_file = st.file_uploader(
            "Upload Resume (PDF/DOCX/TXT):",
            type=['pdf', 'docx', 'txt'],
            key="user_resume"
        )

    if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
        if not job_desc.strip():
            st.error("❌ Please enter job description")
        elif not resume_file:
            st.error("❌ Please upload a resume")
        else:
            with st.spinner("Analyzing your resume..."):
                try:
                    # YOUR ORIGINAL EXTRACTION LOGIC
                    resume_text = extract_text_from_file(resume_file)
                    skills = extract_skills(resume_text)
                    exp_years = estimate_experience_years(resume_text)
                    skill_match = match_job_skills(skills, job_desc)
                    exp_match = experience_percentage(exp_years, 3)
                    final_score = calculate_final_score(skill_match, exp_match)
                    exp_label = classify_experience_level(exp_years)
                    analysis = analyze_resume(resume_text, job_desc)
                    
                    # NEW FEATURE: ATS Score
                    ats_score = generate_ats_score(resume_text, job_desc)

                    # Display Results
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        metric_card("Skill Match", f"{skill_match:.1f}%", "💪", "#6366f1")
                    with col2:
                        metric_card("Experience", f"{exp_match:.1f}%", "📈", "#ec4899")
                    with col3:
                        metric_card("Overall Score", f"{final_score:.1f}%", "🎯", "#10b981")
                    with col4:
                        metric_card("ATS Score", f"{ats_score:.1f}%", "🤖", "#f59e0b")

                    st.markdown("---")

                    # YOUR ORIGINAL RESULTS DISPLAY
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("✅ Your Skills Match")
                        matched = analysis.get("matched_skills", [])
                        if matched:
                            for skill in matched[:8]:
                                st.write(f"• {skill}")
                        else:
                            st.info("No skills matched")

                    with col2:
                        st.subheader("❌ Skills to Develop")
                        missing = analysis.get("missing_skills", [])
                        if missing:
                            for skill in missing[:8]:
                                st.write(f"• {skill}")
                        else:
                            st.success("All required skills present!")

                    st.markdown("---")
                    st.subheader("📊 Analysis Summary")
                    st.write(analysis.get("summary", "No summary"))

                    st.markdown("---")
                    st.subheader("💡 Recommendations")
                    for strength in analysis.get("strengths", []):
                        st.success(f"✅ {strength}")
                    for weakness in analysis.get("weaknesses", []):
                        st.warning(f"⚠️ {weakness}")

                    # Store in session for later use
                    st.session_state.resume_text = resume_text
                    st.session_state.job_desc = job_desc
                    st.session_state.analysis = analysis

                except Exception as e:
                    st.error(f"Error analyzing resume: {str(e)}")


def show_keyword_optimization():
    """Keyword optimization"""
    st.markdown("## 🔍 Keyword Optimization")
    st.markdown("---")

    resume_file = st.file_uploader(
        "Upload your resume (PDF/DOCX/TXT):",
        type=['pdf', 'docx', 'txt'],
        key="opt_resume"
    )

    job_desc = st.text_area(
        "Paste job description:",
        height=150,
        placeholder="Copy job description here..."
    )

    if st.button("🔍 Optimize Keywords", type="primary", use_container_width=True):
        if not resume_file or not job_desc:
            st.error("❌ Please upload resume and job description")
        else:
            with st.spinner("Analyzing keywords..."):
                try:
                    resume_text = extract_text_from_file(resume_file)
                    suggestions = optimize_keywords(resume_text, job_desc)
                    st.success("✅ Optimization complete!")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("📌 Keywords to Add")
                        if suggestions.get("keywords_to_add"):
                            for kw in suggestions["keywords_to_add"][:10]:
                                st.write(f"• {kw}")
                        else:
                            st.info("No missing keywords")

                    with col2:
                        st.subheader("💡 Placement Tips")
                        if suggestions.get("tips"):
                            for tip in suggestions["tips"]:
                                st.write(f"✨ {tip}")

                    st.markdown("---")
                    st.subheader("📝 Optimized Resume Preview")
                    optimized = suggestions.get("optimized_text", resume_text)
                    st.text_area("Optimized Text", value=optimized[:1500], height=250, disabled=True)

                except Exception as e:
                    st.error(f"Error optimizing keywords: {str(e)}")


def show_alternative_roles():
    """Suggest alternative roles"""
    st.markdown("## 🎯 Alternative Role Suggestions")
    st.markdown("---")

    resume_file = st.file_uploader(
        "Upload your resume (PDF/DOCX/TXT):",
        type=['pdf', 'docx', 'txt'],
        key="alt_resume"
    )

    if st.button("🔍 Find Matching Roles", type="primary", use_container_width=True):
        if not resume_file:
            st.error("❌ Please upload resume")
        else:
            with st.spinner("Analyzing your profile..."):
                try:
                    resume_text = extract_text_from_file(resume_file)
                    roles = suggest_alternative_roles(resume_text)
                    st.success("✅ Analysis complete!")

                    st.subheader("🎯 Recommended Roles for You")
                    for idx, role in enumerate(roles, 1):
                        with st.expander(f"{idx}. {role['role']} (Match: {role['match_score']}%)"):
                            st.write(f"**Description:** {role['description']}")
                            st.write(f"**Your Skills Match:**")
                            for skill in role['matching_skills']:
                                st.write(f" • {skill}")
                            st.write(f"**Skills to Learn:**")
                            for skill in role['missing_skills'][:3]:
                                st.write(f" • {skill}")

                except Exception as e:
                    st.error(f"Error suggesting roles: {str(e)}")


def show_interview_prep():
    """Interview preparation - FIXED WITH SESSION STATE"""
    st.markdown("## 💬 AI Interview Question Generator")
    st.markdown("---")

    # Initialize session state for interview prep
    if "interview_resume_file" not in st.session_state:
        st.session_state.interview_resume_file = None
    if "interview_resume_text" not in st.session_state:
        st.session_state.interview_resume_text = None
    if "interview_results" not in st.session_state:
        st.session_state.interview_results = None

    # File uploader - store in session state
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF/DOCX/TXT):",
        type=['pdf', 'docx', 'txt'],
        key="interview_resume_uploader"
    )

    if uploaded_file is not None:
        if st.session_state.interview_resume_file != uploaded_file.name:
            st.session_state.interview_resume_file = uploaded_file.name
            st.session_state.interview_resume_text = extract_text_from_file(uploaded_file)

    job_title = st.text_input(
        "Target job title:",
        placeholder="e.g., Data Scientist, Senior Python Developer"
    )

    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("Number of questions:", 3, 15, 7, key="interview_slider")
    with col2:
        difficulty = st.select_slider("Difficulty level:", ["Beginner", "Intermediate", "Advanced"], value="Intermediate", key="interview_difficulty")

    if st.button("🎯 Generate Interview Questions", type="primary", use_container_width=True):
        if st.session_state.interview_resume_text is None or not job_title:
            st.error("❌ Please upload resume and enter job title")
        else:
            with st.spinner("Generating questions..."):
                try:
                    questions = generate_interview_questions(
                        st.session_state.interview_resume_text,
                        job_title,
                        num_questions,
                        difficulty
                    )
                    st.session_state.interview_results = questions
                    st.success("✅ Interview questions generated!")
                except Exception as e:
                    st.error(f"Error generating questions: {str(e)}")

    # Display results if they exist
    if st.session_state.interview_results is not None:
        st.markdown("---")
        for idx, q_item in enumerate(st.session_state.interview_results, 1):
            with st.expander(f"Question {idx}: {q_item['question'][:50]}..."):
                st.write(f"**Q:** {q_item['question']}")
                st.write(f"**Category:** {q_item['category']}")
                st.write(f"\n**Sample Answer:**")
                st.write(q_item['sample_answer'])
                st.write(f"\n**What they're looking for:**")
                st.write(q_item['evaluation_criteria'])


def show_email_template():
    """Email template generator"""
    st.markdown("## 📧 Email Optimization")
    st.markdown("---")

    st.subheader("Generate Professional Job Application Email")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Company name:", placeholder="TechCorp Inc.")
        job_title = st.text_input("Job title:", placeholder="Senior Python Developer")
        hr_name = st.text_input("HR/Recruiter name:", placeholder="John Smith")

    with col2:
        your_name = st.text_input("Your name:", placeholder="Your Name")
        years_exp = st.number_input("Years of experience:", 0, 50, 3)
        key_achievements = st.text_area("Your key achievements:", height=100, placeholder="List 2-3 key achievements")

    if st.button("✉️ Generate Email", type="primary", use_container_width=True):
        email_data = {
            "company": company_name,
            "job_title": job_title,
            "hr_name": hr_name,
            "your_name": your_name,
            "experience": years_exp,
            "achievements": key_achievements
        }

        email_content = optimize_email(email_data)
        st.success("✅ Email generated!")

        st.subheader("📧 Your Email Draft")
        st.text_area(
            "Email content:",
            value=email_content,
            height=300,
            disabled=True
        )

        st.download_button(
            "⬇️ Download Email",
            email_content,
            file_name="application_email.txt"
        )


def show_career_growth():
    """YOUR ORIGINAL CAREER GROWTH SECTION - FIXED WITH SESSION STATE"""
    st.markdown("## ✨ Career Growth Suggestions")
    st.markdown("---")

    # Initialize session state for career growth
    if "career_resume_file" not in st.session_state:
        st.session_state.career_resume_file = None
    if "career_resume_text" not in st.session_state:
        st.session_state.career_resume_text = None
    if "career_results_shown" not in st.session_state:
        st.session_state.career_results_shown = False
    if "career_num_courses" not in st.session_state:
        st.session_state.career_num_courses = 5

    # File uploader - store in session state
    uploaded_file = st.file_uploader(
        "Upload your resume to get personalized suggestions (PDF/DOCX/TXT):",
        type=['pdf', 'docx', 'txt'],
        key="career_growth_uploader"
    )

    if uploaded_file is not None:
        if st.session_state.career_resume_file != uploaded_file.name:
            st.session_state.career_resume_file = uploaded_file.name
            st.session_state.career_resume_text = extract_text_from_file(uploaded_file)
            st.session_state.career_results_shown = False

    # Use slider to control course recommendations
    if st.session_state.career_resume_text is not None:
        st.markdown("---")
        num_courses = st.slider(
            "Number of courses to recommend:",
            min_value=1,
            max_value=10,
            value=5,
            key="career_courses_slider"
        )
        st.session_state.career_num_courses = num_courses

    if st.button("📈 Get Career Suggestions", type="primary", use_container_width=True):
        if st.session_state.career_resume_text is None:
            st.error("❌ Please upload resume")
        else:
            with st.spinner("Analyzing your profile..."):
                try:
                    st.session_state.career_results_shown = True
                except Exception as e:
                    st.error(f"Error getting career suggestions: {str(e)}")

    # Display results if they exist
    if st.session_state.career_results_shown and st.session_state.career_resume_text is not None:
        st.markdown("---")
        st.subheader("📝 Resume Writing Tips")
        show_resume_tips(st.session_state.career_resume_text)

        st.markdown("---")
        st.subheader("🎓 Recommended Courses")
        recommend_courses_from_resume(st.session_state.career_resume_text, st.session_state.career_num_courses)

        st.markdown("---")
        st.subheader("🎥 Bonus Learning Resources")
        show_bonus_videos()