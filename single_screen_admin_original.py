# single_screen.py
import os
import csv
import datetime
import streamlit as st
import utils.extract as extract
import utils.experience as experience
import utils.ranking as ranking
from utils.analyzer import analyze_resume

# the full single_screen implementation is defined further down and uses extract.extract_text_from_file()


def save_report(rows, mode='single'):
    """
    Save a list of dict rows to a CSV file under the 'reports' directory.
    Returns the path to the saved file.
    """
    os.makedirs('reports', exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"report_{mode}_{timestamp}.csv"
    path = os.path.join('reports', filename)

    # collect headers (union of keys, preserving insertion order)
    headers = []
    for row in rows:
        for k in row.keys():
            if k not in headers:
                headers.append(k)

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return path

def single_screen_admin():
    text=""
    st.header("📄 Single Resume Screening")
    
    # Job Description Box
    st.subheader("🎯 Job Description")
    job_desc = st.text_area("Paste job requirements here:", height=100, 
                           placeholder="e.g., 'Python, SQL, AWS, 3+ years experience...'")
    
    # Resume Upload
    uploaded = st.file_uploader("Upload resume (PDF/DOCX/TXT)", type=['pdf','docx','txt'])
    
    # ANALYZE BUTTON - Only process when clicked
    if st.button("🚀 ANALYZE RESUME", type="primary"):
        if not job_desc.strip():
            st.error("⚠️ Please enter Job Description first!")
        elif not uploaded:
            st.error("⚠️ Please upload a resume first!")
        else:
            with st.spinner("Analyzing resume vs job description..."):
                text = extract.extract_text_from_file(uploaded)
                skills = extract.extract_skills(text)
                exp_years = experience.estimate_experience_years(text)
                
                skill_match = extract.match_job_skills(skills, job_desc)
                exp_match = experience.experience_percentage(exp_years, 3)
                final_score = ranking.calculate_final_score(skill_match, exp_match)
                exp_label = experience.classify_experience_level(exp_years)
            
            # Results
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💪 Skill Match", f"{skill_match}%")
                st.metric("📈 Experience Match", f"{exp_match}%")
            with col2:
                st.metric("🎯 Final Score", f"{final_score}%")

                # --- AI-style block using keyword analysis ---
            result = analyze_resume(text, job_desc)

        if isinstance(result, dict):
            st.subheader("📊 Screening Results (Keyword-based)")
            score = int(result.get("score", 0))
            st.progress(score)
            st.metric("Match Score", f"{score} / 100")

            st.subheader("✅ Matched Skills")
            matched_skills = result.get("matched_skills", [])
            st.write(", ".join(matched_skills) if matched_skills else "None")

            st.subheader("❌ Missing Skills")
            missing_skills = result.get("missing_skills", [])
            st.write(", ".join(missing_skills) if missing_skills else "None")

            st.subheader("📋 Summary")
            st.write(result.get("summary", "No summary returned."))
        

            
            st.subheader("📊 Strengths & Weaknesses")
            strengths = []
            weaknesses = []
            
        if skill_match >= 70:
                strengths.append("✅ Excellent skill alignment")
        elif skill_match >= 40:
                strengths.append("✅ Good skill match")
        else:
                weaknesses.append("❌ Needs more job-specific skills")
                
        if exp_match >= 80:
                strengths.append("✅ Perfect experience level")
        elif exp_years > 0:
                strengths.append("✅ Has relevant experience")
        else:
                weaknesses.append("❌ Entry-level/no experience")
            
        if skills:
                strengths.append(f"✅ Found {len(skills)} skills")
            
        col_str, col_weak = st.columns(2)
        with col_str:
                st.success("**✅ Strengths:**")
                for s in strengths:
                    st.write(f"• {s}")
        with col_weak:
                if weaknesses:
                    st.warning("**❌ Weaknesses:**")
                    for w in weaknesses:
                        st.write(f"• {w}")
                else:
                    st.success("**No major weaknesses!**")
    else:
            st.error("Unexpected analysis response format.")    
            st.subheader("📄 Resume Preview")
            st.text_area("Resume text", value=text, height=400)
            
            # Save button
            if st.button("💾 Save Analysis"):
                row = {
                    'filename': uploaded.name,
                    'skills': skills,
                    'exp_years': exp_years,
                    'skill_match_pct': skill_match,
                    'exp_match_pct': exp_match,
                    'final_score_pct': final_score
                }
                path = save_report([row], 'single')
                st.success(f"✅ Saved to {path}")
            else:
             st.info("👆 Upload resume + Job Description → Click ANALYZE RESUME")
