# multiple_screen.py
import streamlit as st
import utils.extract as extract
import utils.experience as experience
import utils.ranking as ranking
from utils.analyzer import analyze_resume
from storage import save_report

def multiple_screen():
    st.header("📋 Bulk Resume Screening")
    
    st.subheader("🎯 Job Description (Required)")
    job_desc = st.text_area("Paste job requirements:", height=120)
    
    uploaded_files = st.file_uploader("Upload multiple resumes", 
                                    type=['pdf','docx','txt'], 
                                    accept_multiple_files=True)
    
    # ANALYZE BUTTON - Only process when clicked
    if st.button(f"🚀 ANALYZE {len(uploaded_files) if uploaded_files else 0} RESUMES", type="primary"):
        if not job_desc.strip():
            st.error("⚠️ Please enter Job Description!")
        elif not uploaded_files:
            st.error("⚠️ Please upload resumes!")
        else:
            with st.spinner(f"Analyzing {len(uploaded_files)} resumes..."):
                rows = []
                for f in uploaded_files:
                    text = extract.extract_text_from_file(f)
                    skills = extract.extract_skills(text)
                    exp_years = experience.estimate_experience_years(text)
                    
                    skill_match = extract.match_job_skills(skills, job_desc)
                    exp_match = experience.experience_percentage(exp_years, 3)
                    final_score = ranking.calculate_final_score(skill_match, exp_match)
                    
                    rows.append({
                        'filename': f.name, 'skills': skills, 'exp_years': exp_years,
                        'skill_match': skill_match, 'exp_match': exp_match, 'final_score': final_score
                    })
                rows.sort(key=lambda x: x['final_score'], reverse=True)
            
            # Results Table
            st.subheader("📊 Ranked Results")
            df_data = []
            for r in rows:
                df_data.append({
                    'Filename': r['filename'][:25] + '...' if len(r['filename']) > 25 else r['filename'],
                    'Final Score': f"{r['final_score']}%",
                    'Skills Match': f"{r['skill_match']}%",
                    'Exp Match': f"{r['exp_match']}%",
                    'Years': r['exp_years']
                })
            st.dataframe(df_data, use_container_width=True)
            
            # Top 3
            st.subheader("🏆 Top 3 Candidates")
            for i, r in enumerate(rows[:3], 1):
                st.success(f"#{i} **{r['filename'][:30]}** - {r['final_score']}%")
            
            # Save
            if st.button("💾 Save Full Report"):
                save_report(rows, 'bulk')
                st.success("✅ Report saved!")
    else:
        st.info("👆 Enter Job Description + Upload resumes → Click ANALYZE")
