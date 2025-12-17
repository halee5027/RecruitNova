import streamlit as st
import pandas as pd
from io import BytesIO
import re
from datetime import datetime
from resume_fetcher import ResumeFetcher, FETCHED_RESUMES_DIR


def show_fetch_and_screen_page():
    """Main page: Fetch resumes from links and auto-screen against JD"""
    
    st.markdown("## 🔗 Fetch & Auto-Screen Resumes")
    st.info("Paste resume links → Auto-fetch → Auto-screen against JD → Get ranked results")
    st.markdown("---")
    
    # Step 1: Job Description
    st.subheader("Step 1: Job Description")
    job_desc = st.text_area(
        "Paste job requirements:",
        height=120,
        placeholder="Python, SQL, AWS, 3+ years experience, Machine Learning...",
        key="fetch_jd"
    )
    
    st.markdown("---")
    
    # Step 2: Resume Links
    st.subheader("Step 2: Resume Links")
    
    input_method = st.radio(
        "Choose input method:",
        ["Paste URLs", "Upload CSV"],
        horizontal=True,
        key="fetch_method"
    )
    
    urls_to_fetch = []
    
    if input_method == "Paste URLs":
        urls_text = st.text_area(
            "Paste resume URLs (one per line):",
            height=150,
            placeholder="https://drive.google.com/file/d/...\nhttps://example.com/resume.pdf",
            key="paste_urls"
        )
        urls_to_fetch = [url.strip() for url in urls_text.split('\n') if url.strip()]
    
    else:  # CSV Upload
        uploaded_file = st.file_uploader("Upload CSV with resume links:", type=['csv'], key="csv_fetch")
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                url_col = None
                for col in df.columns:
                    if 'url' in col.lower() or 'link' in col.lower():
                        url_col = col
                        break
                
                if url_col:
                    urls_to_fetch = [str(url).strip() for url in df[url_col].dropna() if str(url).strip()]
                    st.write(f"Found {len(urls_to_fetch)} URLs in CSV")
                else:
                    st.error("No URL column found in CSV")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
    
    st.markdown("---")
    
    # Fetch & Screen button
    if st.button("🚀 Fetch & Screen Resumes", type="primary", use_container_width=True):
        if not job_desc.strip():
            st.error("❌ Please enter job description")
        elif not urls_to_fetch:
            st.error("❌ Please provide resume URLs")
        else:
            fetch_and_screen_resumes(urls_to_fetch, job_desc)


def fetch_and_screen_resumes(urls, job_desc):
    """Fetch resumes and screen them against JD"""
    
    from utils.extract import extract_text_from_file, extract_skills, match_job_skills
    from utils.experience import estimate_experience_years, experience_percentage, classify_experience_level
    from utils.ranking import calculate_final_score
    from utils.analyzer import analyze_resume
    
    st.markdown("---")
    st.subheader("Processing...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    fetched_results = []
    failed_urls = []
    
    # Fetch phase
    st.write(f"📥 **Fetching {len(urls)} resumes...**")
    
    for idx, url in enumerate(urls):
        status_text.write(f"⏳ Fetching: {url[:60]}...")
        progress = (idx + 1) / (len(urls) * 2)
        progress_bar.progress(progress)
        
        result = ResumeFetcher.fetch_from_url(url)
        
        if result['status'] == 'success':
            is_valid, _ = ResumeFetcher.validate_content(result['content'])
            if is_valid:
                fetched_results.append({
                    'url': url,
                    'filename': result['filename'],
                    'content': result['content'],
                    'size': result['size']
                })
            else:
                failed_urls.append({'url': url, 'error': 'Invalid file format'})
        else:
            failed_urls.append({'url': url, 'error': result['message']})
    
    if not fetched_results:
        st.error(f"❌ Failed to fetch any resumes")
        return
    
    # Screening phase
    st.write(f"🔍 **Screening {len(fetched_results)} resumes against JD...**")
    
    screening_results = []
    
    for idx, fetched in enumerate(fetched_results):
        status_text.write(f"🔍 Screening: {fetched['filename']}")
        progress = 0.5 + (idx + 1) / (len(fetched_results) * 2)
        progress_bar.progress(progress)
        
        try:
            resume_file = BytesIO(fetched['content'])
            resume_file.name = fetched['filename']
            resume_text = extract_text_from_file(resume_file)
            
            skills = extract_skills(resume_text)
            exp_years = estimate_experience_years(resume_text)
            skill_match = match_job_skills(skills, job_desc)
            exp_match = experience_percentage(exp_years, 3)
            final_score = calculate_final_score(skill_match, exp_match)
            exp_label = classify_experience_level(exp_years)
            analysis = analyze_resume(resume_text, job_desc)
            
            email_search = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text)
            phone_search = re.search(r'(\+\d{1,3}[-.\\s]?)?(\d{3}[-.\\s]?){2}\d{4}', resume_text)
            
            email = email_search.group(0) if email_search else "Not found"
            contact = phone_search.group(0) if phone_search else "Not found"
            
            if final_score >= 75:
                fit = "Strongly Fit"
            elif final_score >= 50:
                fit = "Mid Fit"
            else:
                fit = "Low Fit"
            
            screening_results.append({
                'candidate_name': fetched['filename'].replace('.pdf', '').replace('.docx', '').replace('.txt', ''),
                'email': email,
                'contact': contact,
                'skills': ', '.join(skills[:5]) if skills else "None",
                'experience_level': exp_label,
                'skill_match': round(skill_match, 2),
                'exp_match': round(exp_match, 2),
                'overall_score': round(final_score, 2),
                'fit': fit,
                'matched_skills': analysis.get('matched_skills', []),
                'missing_skills': analysis.get('missing_skills', []),
                'summary': analysis.get('summary', '')
            })
        
        except Exception as e:
            st.warning(f"Error screening {fetched['filename']}: {str(e)}")
    
    progress_bar.progress(1.0)
    status_text.empty()
    
    screening_results.sort(key=lambda x: x['overall_score'], reverse=True)
    
    st.markdown("---")
    display_screening_results(screening_results, failed_urls)


def display_screening_results(results, failed):
    """Display screening results"""
    
    st.success(f"✅ Successfully screened {len(results)} resumes!")
    
    if failed:
        with st.expander(f"⚠️ {len(failed)} Failed Fetches"):
            for item in failed[:10]:
                st.write(f"❌ {item['url'][:60]}... → {item['error']}")
    
    # Summary metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Screened", len(results))
    with col2:
        st.metric("💪 Strongly Fit", len([r for r in results if r['fit'] == 'Strongly Fit']))
    with col3:
        st.metric("👍 Mid Fit", len([r for r in results if r['fit'] == 'Mid Fit']))
    with col4:
        st.metric("👎 Low Fit", len([r for r in results if r['fit'] == 'Low Fit']))
    
    # Top 3 candidates
    st.markdown("---")
    st.subheader("🥇🥈🥉 Top 3 Candidates")
    
    for idx, candidate in enumerate(results[:3], 1):
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            
            with col1:
                st.write(f"**#{idx}. {candidate['candidate_name']}**")
            with col2:
                st.write(f"📧 {candidate['email']}")
            with col3:
                st.write(f"📞 {candidate['contact']}")
            with col4:
                st.write(f"**Score: {candidate['overall_score']}%** ({candidate['fit']})")
            
            st.divider()
    
    # Full results table
    st.markdown("---")
    st.subheader("📋 All Results")
    
    df = pd.DataFrame([
        {
            'Rank': idx + 1,
            'Candidate': r['candidate_name'],
            'Email': r['email'],
            'Experience': r['experience_level'],
            'Skill %': r['skill_match'],
            'Exp %': r['exp_match'],
            'Overall %': r['overall_score'],
            'Fit': r['fit']
        }
        for idx, r in enumerate(results)
    ])
    
    st.dataframe(df, use_container_width=True)
    
    # Download results
    st.markdown("---")
    if st.button("📥 Download Results as Excel", use_container_width=True):
        try:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Screening Results')
            
            excel_buffer.seek(0)
            st.download_button(
                "⬇️ Download Excel Report",
                excel_buffer.getvalue(),
                file_name=f"fetched_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating Excel: {e}")
    
    # Detailed view
        st.markdown("---")
    st.subheader("🔍 Detailed Candidate Analysis")

    # keep selection in session_state so changing it doesn't reset the page
    if "fetch_selected_idx" not in st.session_state:
        st.session_state.fetch_selected_idx = 0

    selected_idx = st.selectbox(
        "Select candidate to view details:",
        range(len(results)),
        index=st.session_state.fetch_selected_idx,
        key="fetch_detail_select",
        format_func=lambda i: f"#{i+1}. {results[i]['candidate_name']} ({results[i]['overall_score']}%)"
    )

    st.session_state.fetch_selected_idx = selected_idx
    candidate = results[selected_idx]

    
    
        
    col1, col2, col3 = st.columns(3)
    with col1:
            st.metric("Skill Match", f"{candidate['skill_match']}%")
    with col2:
            st.metric("Experience Match", f"{candidate['exp_match']}%")
    with col3:
            st.metric("Overall Score", f"{candidate['overall_score']}%")
        
    col1, col2 = st.columns(2)
        
    with col1:
            st.write("**✅ Matched Skills:**")
            if candidate['matched_skills']:
                for skill in candidate['matched_skills'][:10]:
                    st.write(f"  ⚪ {skill}")
            else:
                st.write("None")
        
    with col2:
            st.write("**❌ Missing Skills:**")
            if candidate['missing_skills']:
                for skill in candidate['missing_skills'][:10]:
                    st.write(f"  🔴 {skill}")
            else:
                st.write("None")
        
    st.write("**📝 Summary:**")
    st.write(candidate['summary'])