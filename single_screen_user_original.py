# single_screen.py
import os
import csv
import datetime
import streamlit as st
import utils.extract as extract
import utils.experience as experience
import utils.ranking as ranking
from utils.analyzer import analyze_resume
from users_extract import show_resume_tips, show_bonus_videos, recommend_courses_from_resume

def single_screen_user():
    st.header("📄 Single Resume Screening")

    # -----------------------------
    # Initialize session state flag
    # -----------------------------
    if "analyzed" not in st.session_state:
        st.session_state["analyzed"] = False

    # -----------------------------
    # Job Description + Resume Upload
    # -----------------------------
    job_desc = st.text_area(
        "🎯 Job Description",
        height=100,
        placeholder="e.g., 'Python, SQL, AWS, 3+ years experience...'"
    )

    uploaded = st.file_uploader(
        "Upload resume (PDF/DOCX/TXT)",
        type=['pdf', 'docx', 'txt'],
        key="user_single_upload"
    )

    # -----------------------------
    # ANALYZE BUTTON
    # -----------------------------
    if st.button("🚀 ANALYZE RESUME", type="primary", key="user_analyze"):
        if not job_desc.strip():
            st.error("⚠️ Please enter Job Description first!")
            return
        if not uploaded:
            st.error("⚠️ Please upload a resume first!")
            return

        st.session_state["analyzed"] = True  # Keep page persistent

        with st.spinner("Analyzing resume vs job description..."):
            text = extract.extract_text_from_file(uploaded)
            skills = extract.extract_skills(text)
            exp_years = experience.estimate_experience_years(text)

            skill_match = extract.match_job_skills(skills, job_desc)
            exp_match = experience.experience_percentage(exp_years, 3)
            final_score = ranking.calculate_final_score(skill_match, exp_match)
            exp_label = experience.classify_experience_level(exp_years)

            result = analyze_resume(text, job_desc)

        # Store analysis results
        st.session_state["resume_text"] = text
        st.session_state["skill_match"] = skill_match
        st.session_state["exp_match"] = exp_match
        st.session_state["final_score"] = final_score
        st.session_state["exp_years"] = exp_years
        st.session_state["exp_label"] = exp_label
        st.session_state["result"] = result

    # ===========================================================
    # SHOW RESULTS ONLY IF ANALYZED
    # ===========================================================
    if st.session_state["analyzed"]:
        text = st.session_state["resume_text"]
        skill_match = st.session_state["skill_match"]
        exp_match = st.session_state["exp_match"]
        final_score = st.session_state["final_score"]
        exp_years = st.session_state["exp_years"]
        exp_label = st.session_state["exp_label"]
        result = st.session_state["result"]

        # ---------- MAIN ANALYSIS ----------
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💪 Skill Match", f"{skill_match:.0f}%")
            st.metric("📈 Experience Match", f"{exp_match:.0f}%")
        with col2:
            st.metric("🎯 Final Score", f"{final_score:.1f}%")
            st.write(f"**Experience:** {exp_years} years ({exp_label})")

        if isinstance(result, dict):
            st.subheader("📊 Screening Results (Keyword-based)")
            score = int(result.get("score", 0))
            st.progress(score)
            st.metric("Match Score", f"{score} / 100")

            st.subheader("✅ Matched Skills")
            st.write(", ".join(result.get("matched_skills", [])))

            st.subheader("❌ Missing Skills")
            st.write(", ".join(result.get("missing_skills", [])))

            st.subheader("📋 Summary")
            st.write(result.get("summary", "No summary returned."))

        # ---------- Strengths / Weaknesses ----------
        st.subheader("📊 Strengths & Weaknesses")
        strengths, weaknesses = [], []

        if skill_match >= 70:
            strengths.append("Excellent skill alignment")
        elif skill_match >= 40:
            strengths.append("Good skill match")
        else:
            weaknesses.append("Needs more job-specific skills")

        if exp_match >= 80:
            strengths.append("Perfect experience level")
        elif exp_years > 0:
            strengths.append("Has relevant experience")
        else:
            weaknesses.append("Entry-level / no experience")

        if text:
            strengths.append("Resume parsed successfully")

        col_str, col_weak = st.columns(2)
        with col_str:
            st.success("**Strengths:**")
            for s in strengths:
                st.write(f"• {s}")

        with col_weak:
            if weaknesses:
                st.warning("**Weaknesses:**")
                for w in weaknesses:
                    st.write(f"• {w}")
            else:
                st.success("No major weaknesses")

        # ---------- Career Growth ----------
        st.header("✨ Career Growth Suggestions")

        show_resume_tips(text)
        recommend_courses_from_resume(text)
        show_bonus_videos()
