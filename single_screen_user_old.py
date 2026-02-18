import streamlit as st
import pandas as pd
from utils.extract import extract_text_from_file, extract_skills, match_job_skills
from utils.experience import estimate_experience_years, experience_percentage, classify_experience_level
from utils.ranking import calculate_final_score
from utils.analyzer import analyze_resume
from users_extract import show_resume_tips, show_bonus_videos, recommend_courses_from_resume
from new_ai_features import optimize_keywords, suggest_alternative_roles, optimize_email, generate_ats_score, generate_interview_questions
from ui_components import metric_card, show_header_with_user
from utils.radar_chart import parse_skills_to_dimensions, create_radar_chart

# Helper for Dashboard Navigation
def navigate_to(page):
    st.session_state.dashboard_page = page
    st.rerun()

def show_dashboard_home():
    """Render the main dashboard with glassmorphic cards"""
    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>🚀 Candidate Dashboard</h2>", unsafe_allow_html=True)
    
    # Row 1
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="glass-card dashboard-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📄</div>
            <h4>Resume Analysis</h4>
            <p style="font-size: 0.9rem;">Get AI-powered feedback on your resume matching job descriptions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Analysis", key="btn_resume", use_container_width=True, type="primary"):
            navigate_to("resume_analysis")

    with col2:
        st.markdown("""
        <div class="glass-card dashboard-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🔍</div>
            <h4>Keyword Optimization</h4>
            <p style="font-size: 0.9rem;">Boost your ATS score by adding missing keywords.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Optimize Keywords", key="btn_keywords", use_container_width=True, type="primary"):
            navigate_to("keyword_optimization")

    with col3:
        st.markdown("""
        <div class="glass-card dashboard-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎯</div>
            <h4>Alternative Roles</h4>
            <p style="font-size: 0.9rem;">Discover new career paths matching your skills.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Roles", key="btn_roles", use_container_width=True, type="primary"):
            navigate_to("alternative_roles")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2
    col4, col5, col6 = st.columns(3, gap="medium")
    
    with col4:
        st.markdown("""
        <div class="glass-card dashboard-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">💬</div>
            <h4>Interview Prep</h4>
            <p style="font-size: 0.9rem;">Practice with AI-generated interview questions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Prep", key="btn_interview", use_container_width=True, type="primary"):
            navigate_to("interview_prep")

    with col5:
        st.markdown("""
        <div class="glass-card dashboard-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📧</div>
            <h4>Email Templates</h4>
            <p style="font-size: 0.9rem;">Generate professional emails for job applications.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Email", key="btn_email", use_container_width=True, type="primary"):
            navigate_to("email_template")

    with col6:
        st.markdown("""
        <div class="glass-card dashboard-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📈</div>
            <h4>Career Growth</h4>
            <p style="font-size: 0.9rem;">Upskill with recommended courses and resources.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Growth", key="btn_growth", use_container_width=True, type="primary"):
            navigate_to("career_growth")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 3 - New Analytics Features (Removed Skills Profile)
    # col7, col8, col9 = st.columns(3, gap="medium")
    
    # with col7:
    #      pass # Skills profile removed

def show_user_dashboard():
    """Main user dashboard - INTERNAL NAVIGATION"""
    
    # Initialize dashboard page state
    if "dashboard_page" not in st.session_state:
        st.session_state.dashboard_page = "home"
    
    # Show Header (User Name) - kept clean
    show_header_with_user()

    # If deeper than home, show BACK button
    if st.session_state.dashboard_page != "home":
        if st.button("⬅️ Back to Dashboard"):
            navigate_to("home")
            
    # Navigation Logic
    if st.session_state.dashboard_page == "home":
        show_dashboard_home()
        
    elif st.session_state.dashboard_page == "resume_analysis":
        show_resume_analysis()
        
    elif st.session_state.dashboard_page == "keyword_optimization":
        show_keyword_optimization()
        
    elif st.session_state.dashboard_page == "alternative_roles":
        show_alternative_roles()
        
    elif st.session_state.dashboard_page == "interview_prep":
        show_interview_prep()
        
    elif st.session_state.dashboard_page == "email_template":
        show_email_template()
    
    # Skills profile route removed
    
    elif st.session_state.dashboard_page == "career_growth":
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
    """Premium Keyword Optimization Feature"""
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h2 style="margin: 0;">🔑 AI Keyword Optimizer</h2>
        <p style="opacity: 0.7; font-size: 0.95em; margin-top: 4px;">Maximize your ATS score with intelligent keyword analysis</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    col_upload, col_jd = st.columns([1, 1.5], gap="medium")

    with col_upload:
        st.markdown("##### 📄 Your Resume")
        resume_file = st.file_uploader(
            "Upload resume (PDF/DOCX/TXT):",
            type=['pdf', 'docx', 'txt'],
            key="opt_resume"
        )

    with col_jd:
        st.markdown("##### 📋 Target Job Description")
        job_desc = st.text_area(
            "Paste the job description here:",
            height=150,
            placeholder="Paste the complete job description to get the best keyword analysis..."
        )

    if st.button("🚀 Analyze & Optimize", type="primary", use_container_width=True):
        if not resume_file or not job_desc:
            st.error("❌ Please upload your resume and paste the job description.")
        elif len(job_desc.strip()) < 50:
            st.warning("⚠️ Job description seems too short. Paste the full description for better results.")
        else:
            with st.spinner("🔬 Running deep keyword analysis..."):
                try:
                    resume_text = extract_text_from_file(resume_file)
                    suggestions = optimize_keywords(resume_text, job_desc)
                    st.session_state.optimization_results = suggestions
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if 'optimization_results' in st.session_state:
        r = st.session_state.optimization_results

        # Validation
        if not isinstance(r, dict) or "keywords_to_add" not in r or "ats_before" not in r:
            del st.session_state.optimization_results
            st.rerun()
            return

        st.markdown("---")

        # ═══════════════════════════════════════════════
        # SECTION 1: Score Dashboard
        # ═══════════════════════════════════════════════
        st.markdown("### 📊 Optimization Dashboard")
        
        s1, s2, s3, s4 = st.columns(4, gap="small")
        with s1:
            st.metric("🎯 Keyword Match", f"{r['match_percentage']}%",
                       help="Percentage of job description keywords found in your resume")
        with s2:
            st.metric("📉 ATS Score (Before)", f"{r['ats_before']}%")
        with s3:
            delta = r['ats_after'] - r['ats_before']
            st.metric("📈 ATS Score (After)", f"{r['ats_after']}%", delta=f"+{delta}%")
        with s4:
            st.metric("🔑 Missing Keywords", f"{len(r['keywords_to_add'])}")

        # Progress bar for match
        st.progress(min(r['match_percentage'] / 100, 1.0))
        st.caption(f"Your resume matches **{r['match_percentage']}%** of the {r['total_job_keywords']} unique keywords in the job description.")

        st.markdown("---")

        # ═══════════════════════════════════════════════
        # SECTION 2: Categorized Missing Keywords  
        # ═══════════════════════════════════════════════
        st.markdown("### 🏷️ Keywords to Add")
        st.caption("Grouped by category for targeted resume updates.")

        cat = r.get("categorized_missing", {})

        def render_keyword_tags(keywords, color, icon):
            if not keywords:
                return
            tags = " ".join([
                f"<span style='background:{color}; color:white; padding:5px 14px; border-radius:20px; "
                f"margin:3px; display:inline-block; font-weight:600; font-size:0.88em; "
                f"letter-spacing:0.3px; box-shadow: 0 2px 6px rgba(0,0,0,0.15);'>"
                f"{icon} {kw.title()}</span>"
                for kw in keywords
            ])
            st.markdown(tags, unsafe_allow_html=True)

        tag_col1, tag_col2 = st.columns(2, gap="medium")

        with tag_col1:
            if cat.get("technical"):
                st.markdown("**💻 Technical Skills**")
                render_keyword_tags(cat["technical"], "linear-gradient(135deg, #6366f1, #818cf8)", "⚡")
            if cat.get("tools"):
                st.markdown("**🔧 Tools & Platforms**")
                render_keyword_tags(cat["tools"], "linear-gradient(135deg, #0891b2, #22d3ee)", "🛠")

        with tag_col2:
            if cat.get("soft_skills"):
                st.markdown("**🤝 Soft Skills**")
                render_keyword_tags(cat["soft_skills"], "linear-gradient(135deg, #059669, #34d399)", "✨")
            if cat.get("other"):
                st.markdown("**📌 Other Keywords**")
                render_keyword_tags(cat["other"], "linear-gradient(135deg, #d97706, #fbbf24)", "🔶")

        # If no categorized keywords at all
        if not any(cat.values()):
            st.success("🎉 Great job! Your resume covers the key terms well.")

        # ═══════════════════════════════════════════════
        # SECTION 2b: High Importance Alert
        # ═══════════════════════════════════════════════
        hi_missing = r.get("high_importance_missing", [])
        if hi_missing:
            st.markdown("---")
            st.markdown("### ⚠️ High Priority — Most Repeated in Job Description")
            st.caption("These keywords appear multiple times in the JD, meaning the employer values them highly.")
            for kw, count in hi_missing:
                st.warning(f"**{kw.title()}** — mentioned **{count}x** in job description but **missing** from your resume")
        
        st.markdown("---")

        # ═══════════════════════════════════════════════
        # SECTION 3: Matched Keywords (what you already have)
        # ═══════════════════════════════════════════════
        with st.expander("✅ Keywords You Already Have", expanded=False):
            matched = r.get("matched_keywords", [])
            if matched:
                match_tags = " ".join([
                    f"<span style='background: linear-gradient(135deg, #059669, #34d399); color: white; "
                    f"padding:5px 14px; border-radius:20px; margin:3px; display:inline-block; "
                    f"font-weight:600; font-size:0.85em; box-shadow: 0 2px 6px rgba(0,0,0,0.15);'>"
                    f"✓ {kw.title()}</span>"
                    for kw in matched
                ])
                st.markdown(match_tags, unsafe_allow_html=True)
            else:
                st.info("No direct keyword matches found.")

        st.markdown("---")

        # ═══════════════════════════════════════════════
        # SECTION 4: Tips + Optimized Preview
        # ═══════════════════════════════════════════════
        st.markdown("### 🛠️ Optimization Tools")

        tips_col, preview_col = st.columns([1, 1.2], gap="medium")

        with tips_col:
            st.markdown("##### 💡 Pro Tips")
            for i, tip in enumerate(r.get("tips", []), 1):
                st.info(f"**{i}.** {tip}")

        with preview_col:
            st.markdown("##### 📝 Optimized Resume Preview")
            st.caption("Keywords have been intelligently inserted into your resume's skills section.")
            optimized = r.get("optimized_text", "")
            st.text_area("Preview", value=optimized, height=400, disabled=True, label_visibility="collapsed")
            
        # Download
        st.markdown("<br>", unsafe_allow_html=True)
        dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
        with dl_col2:
            st.download_button(
                "📥 Download Optimized Resume",
                r.get("optimized_text", ""),
                file_name="Optimized_Resume.txt",
                use_container_width=True,
                type="primary"
            )


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
                    # Use Session State to persist results
                    st.session_state.suggested_roles = suggest_alternative_roles(resume_text)
                    st.session_state.resume_text_for_roles = resume_text # Store for learning path
                    st.success("✅ Analysis complete!")
                except Exception as e:
                    st.error(f"Error suggesting roles: {str(e)}")

    # Display Results from Session State
    if 'suggested_roles' in st.session_state and st.session_state.suggested_roles:
        roles = st.session_state.suggested_roles
        
        # Validation for backward compatibility
        if roles and (isinstance(roles[0], str) or not isinstance(roles[0], dict)):
             st.warning("⚠️ Data format updated. Please click 'Find Matching Roles' to re-analyze.")
             del st.session_state.suggested_roles
             st.rerun()
             return
        
        st.subheader("🎯 Recommended Roles for You")
        
        for idx, role in enumerate(roles, 1):
            with st.expander(f"{idx}. {role['role']} (Match: {role['match_score']}%)"):
                st.write(f"**Description:** {role['description']}")
                
                # New Metadata Columns
                meta_col1, meta_col2 = st.columns(2)
                with meta_col1:
                     st.write(f"💰 **Salary:** {role['salary_range']}")
                with meta_col2:
                     st.write(f"📈 **Growth:** {role['growth_potential']}")
                
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"✅ **Matching Skills:**")
                    if role['matching_skills']:
                        for skill in role['matching_skills']:
                            st.caption(f"• {skill}")
                    else:
                        st.caption("No direct skill matches")
                        
                with col2:
                    st.write(f"⚠️ **Skills to Learn:**")
                    for skill in role['missing_skills']:
                        st.caption(f"• {skill}")
                        
                st.divider()
                
                # Learning Path Button
                if st.button(f"🎓 View Learning Path for {role['role']}", key=f"btn_lp_{idx}"):
                    st.session_state.active_learning_path_role = role['role']
                    st.rerun()

    # Learning Path Modal / Section
    if 'active_learning_path_role' in st.session_state:
        target_role = st.session_state.active_learning_path_role
        resume_text = st.session_state.get('resume_text_for_roles', "")
        
        st.markdown("---")
        st.markdown(f"### 🚀 Learning Path: {target_role}")
        
        from new_ai_features import create_learning_path
        path = create_learning_path(resume_text, target_role)
        
        for step in path:
            st.info(f"**{step['skill']}** ({step['duration']})\n\n📚 Resources: {', '.join(step['resources'])}")
            
        if st.button("Close Learning Path"):
            del st.session_state.active_learning_path_role
            st.rerun()


def show_interview_prep():
    """Redesigned AI Interview Coach"""
    import time
    
    # Initialize Session State logic
    if "interview_active" not in st.session_state: st.session_state.interview_active = False
    if "current_question_idx" not in st.session_state: st.session_state.current_question_idx = 0
    if "show_answer" not in st.session_state: st.session_state.show_answer = False
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>AI Interview Coach 🤖</h2>", unsafe_allow_html=True)
    
    if not st.session_state.interview_active:
        # --- CONFIGURATION SCREEN ---
        col1, col2 = st.columns([1, 1], gap="medium")
        
        with col1:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); height: 100%;">
                <h3 style="margin-top:0; color: #818cf8;">📄 Context</h3>
                <p style="font-size: 0.9em; opacity: 0.8; margin-bottom: 20px;">Upload your resume so the AI can tailor questions to your actual experience and skills.</p>
                <div style="margin-top: 10px;"></div>
            </div>
            """, unsafe_allow_html=True)
            # Uploader outside the div for streamlit interactivity
            uploaded_file = st.file_uploader("Upload Resume (Optional)", type=['pdf', 'docx', 'txt'], key="int_prep_resume_new")
            if uploaded_file:
                 st.session_state.interview_resume_text = extract_text_from_file(uploaded_file)
            
        with col2:
             st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); height: 100%;">
                <h3 style="margin-top:0; color: #06b6d4;">⚙️ Settings</h3>
                <p style="font-size: 0.9em; opacity: 0.8; margin-bottom: 20px;">Customize the intensity and focus of your mock interview session.</p>
            </div>
            """, unsafe_allow_html=True)
             
             job_title = st.text_input("Target Role", value="Software Engineer", help="e.g. Product Manager")
             difficulty = st.select_slider("Difficulty Level", options=["Easy", "Intermediate", "Advanced"], value="Intermediate")
             num_q = st.slider("Number of Questions", 3, 10, 5)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center Start Button
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            if st.button("🚀 Start Interview Simulation", type="primary", use_container_width=True):
                with st.spinner("Analyzing profile and generating questions..."):
                    # Generate Questions
                    resume_txt = st.session_state.get("interview_resume_text", "")
                    questions = generate_interview_questions(resume_txt, job_title, num_q, difficulty)
                    
                    st.session_state.interview_results = questions
                    st.session_state.interview_active = True
                    st.session_state.current_question_idx = 0
                    st.session_state.show_answer = False
                    st.session_state.interview_score = 0
                    st.rerun()

    else:
        # --- ACTIVE INTERVIEW SESSION ---
        questions = st.session_state.interview_results
        idx = st.session_state.current_question_idx
        
        if idx < len(questions):
            q_data = questions[idx]
            
            # Progress Header
            progress = (idx + 1) / len(questions)
            st.progress(progress)
            st.caption(f"Question {idx + 1} of {len(questions)}")
            
            # Question Card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(6, 182, 212, 0.05) 100%); 
                        border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 40px; margin: 20px 0; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                <span style="background: rgba(99, 102, 241, 0.1); color: #818cf8; padding: 6px 16px; border-radius: 20px; font-size: 0.85em; font-weight: 600; text-transform: uppercase;">
                    {q_data['category']}
                </span>
                <h2 style="margin-top: 20px; font-size: 1.8em; font-weight: 600; line-height: 1.4;">{q_data['question']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Interaction Area
            col_left, col_right = st.columns([1, 1], gap="medium")
            
            if not st.session_state.show_answer:
                with col_left:
                    st.info("💡 **Tip:** Take a moment to think about your answer. Use the STAR method (Situation, Task, Action, Result).")
                with col_right:
                    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                    if st.button("👁️ Reveal Answer & Coaching", use_container_width=True, type="primary"):
                         st.session_state.show_answer = True
                         st.rerun()
            else:
                # Answer Revealed
                st.markdown("### 🎓 AI Coach Feedback")
                
                with st.expander("✅ Ideal Answer Strategy", expanded=True):
                    st.write(q_data['sample_answer'])
                    st.markdown(f"**Key Evaluation Criteria:** `{q_data['evaluation_criteria']}`")
                
                if q_data.get('follow_up'):
                    st.warning(f"**🔄 Follow-up Question:** {q_data['follow_up']}")
                
                # Next Navigation
                st.markdown("<br>", unsafe_allow_html=True)
                col_next_l, col_next_r = st.columns([3, 1])
                with col_next_r:
                    btn_label = "Next Question ➡" if idx < len(questions) - 1 else "🎉 Finish Session"
                    if st.button(btn_label, type="primary", use_container_width=True):
                        if idx < len(questions) - 1:
                            st.session_state.current_question_idx += 1
                            st.session_state.show_answer = False
                            st.rerun()
                        else:
                            st.balloons()
                            time.sleep(1)
                            st.session_state.interview_active = False
                            st.rerun()

        else:
            # Fallback for end state
            st.session_state.interview_active = False
            st.rerun()

        # Exit Button (Always available)
        st.markdown("<hr style='margin: 40px 0; opacity: 0.2;'>", unsafe_allow_html=True)
        if st.button("❌ End Session Early"):
            st.session_state.interview_active = False
            st.rerun()


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


# Skills Profile removed as per user request