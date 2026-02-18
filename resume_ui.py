
import streamlit as st
import pandas as pd
from io import BytesIO
import re
from datetime import datetime

# Import hooks - Ensure these match your project structure
try:
    from resume_fetcher import ResumeFetcher, FETCHED_RESUMES_DIR
    from utils.extract import extract_text_from_file, extract_skills, match_job_skills
    from utils.experience import estimate_experience_years, experience_percentage, classify_experience_level
    from utils.ranking import calculate_final_score
    from utils.analyzer import analyze_resume
except ImportError as e:
    st.error(f"❌ Critical Import Error: {e}")

def show_fetch_and_screen_page():
    """Main page: Fetch resumes from links and auto-screen against JD"""
    
    st.markdown("## 🔗 Fetch & Auto-Screen Resumes")
    st.info("Paste resume links → Auto-fetch → Auto-screen against JD → Get ranked results")
    st.markdown("---")
    
    # Initialize Session States to persist results across interactions
    if "screening_results" not in st.session_state:
        st.session_state.screening_results = None
    if "failed_urls" not in st.session_state:
        st.session_state.failed_urls = []
    
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
    else:
        uploaded_file = st.file_uploader("Upload CSV with resume links:", type=['csv'], key="csv_fetch")
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                url_col = next((c for c in df.columns if 'url' in c.lower() or 'link' in c.lower()), None)
                if url_col:
                    urls_to_fetch = [str(url).strip() for url in df[url_col].dropna() if str(url).strip()]
                    st.write(f"Found {len(urls_to_fetch)} URLs in CSV")
                else:
                    st.error("No URL column found in CSV")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
    
    st.markdown("---")
    
    # Fetch & Screen Action
    if st.button("🚀 Fetch & Screen Resumes", type="primary", use_container_width=True):
        if not job_desc.strip():
            st.error("❌ Please enter job description")
        elif not urls_to_fetch:
            st.error("❌ Please provide resume URLs")
        else:
            # Process and store in session state
            results, failed = process_resumes_logic(urls_to_fetch, job_desc)
            st.session_state.screening_results = results
            st.session_state.failed_urls = failed

    # If results exist in state, display them
    if st.session_state.screening_results:
        display_screening_results(st.session_state.screening_results, st.session_state.failed_urls)
def process_resumes_logic(urls, job_desc):
    """Core logic: Fetches, extracts text, and applies flexible Regex for contact info"""
    screening_results = []
    failed_urls = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, url in enumerate(urls):
        status_text.write(f"⏳ Processing: {url[:50]}...")
        progress_bar.progress((idx + 1) / len(urls))
        
        result = ResumeFetcher.fetch_from_url(url)
        
        if result['status'] == 'success':
            try:
                resume_file = BytesIO(result['content'])
                resume_file.name = result['filename']
                text = extract_text_from_file(resume_file)
                
                # --- FLEXIBLE CONTACT EXTRACTION ---
                # Improved Regex for phone numbers: Handles spaces, dots, parens, and international codes
                phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4,6}'
                phone_search = re.search(phone_pattern, text)
                contact_info = phone_search.group(0).strip() if phone_search else "Not found"
                
                email_search = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
                email = email_search.group(0) if email_search else "Not found"
                
                # Scoring and Analysis
                skills = extract_skills(text)
                exp_years = estimate_experience_years(text)
                skill_match = match_job_skills(skills, job_desc)
                exp_match = experience_percentage(exp_years, 3)
                final_score = calculate_final_score(skill_match, exp_match)
                analysis = analyze_resume(text, job_desc)
                
                fit = "Strongly Fit" if final_score >= 75 else "Mid Fit" if final_score >= 50 else "Low Fit"
                
                screening_results.append({
                    'candidate_name': result['filename'].split('.')[0],
                    'email': email,
                    'contact': contact_info, # Key fixed for KeyError
                    'experience_level': classify_experience_level(exp_years),
                    'skill_match': round(skill_match, 2),
                    'exp_match': round(exp_match, 2),
                    'overall_score': round(final_score, 2),
                    'fit': fit,
                    'matched_skills': analysis.get('matched_skills', []),
                    'missing_skills': analysis.get('missing_skills', []),
                    'summary': analysis.get('summary', 'No summary available.')
                })
            except Exception as e:
                failed_urls.append({'url': url, 'error': f"Processing Error: {str(e)}"})
        else:
            failed_urls.append({'url': url, 'error': result['message']})
            
    progress_bar.empty()
    status_text.empty()
    screening_results.sort(key=lambda x: x['overall_score'], reverse=True)
    return screening_results, failed_urls


def display_screening_results(results, failed):
    """UI Display: Metrics, Top 3, Full Table, and No-Reload Details"""
    
    st.success(f"✅ Successfully screened {len(results)} resumes!")
    
    if failed:
        with st.expander(f"⚠️ {len(failed)} Failed Fetches"):
            for item in failed:
                st.write(f"❌ {item['url'][:60]}... → {item['error']}")
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Total", len(results))
    col2.metric("💪 Strongly Fit", len([r for r in results if r['fit'] == 'Strongly Fit']))
    col3.metric("👍 Mid Fit", len([r for r in results if r['fit'] == 'Mid Fit']))
    col4.metric("👎 Low Fit", len([r for r in results if r['fit'] == 'Low Fit']))
    
    # Top 3 candidates
    st.markdown("---")
    st.subheader("🥇🥈🥉 Top 3 Candidates")
    for idx, cand in enumerate(results[:3], 1):
        c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
        c1.write(f"**#{idx}. {cand['candidate_name']}**")
        c2.write(f"📧 {cand['email']}")
        c3.write(f"📞 {cand.get('contact', 'Not found')}") # Safe get to prevent KeyError
        c4.write(f"**Score: {cand['overall_score']}%** ({cand['fit']})")
        st.divider()
    
    # Full results table
    st.subheader("📋 All Results")
    df = pd.DataFrame([{
        'Rank': i+1, 'Candidate': r['candidate_name'], 'Experience': r['experience_level'],
        'Skill %': r['skill_match'], 'Exp %': r['exp_match'], 
        'Overall %': r['overall_score'], 'Fit': r['fit']
    } for i, r in enumerate(results)])
    st.table(df)
    
    # Download Button logic (Persistent)
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Screening Results')
    st.download_button(
        "📥 Download Full Report (Excel)",
        excel_buffer.getvalue(),
        file_name=f"screening_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    
    # Detailed Analysis Section
    st.markdown("---")
    st.subheader("🔍 Detailed Candidate Analysis")

    if "fetch_selected_idx" not in st.session_state:
        st.session_state.fetch_selected_idx = 0

    selected_idx = st.selectbox(
        "Select candidate to view details:",
        range(len(results)),
        index=st.session_state.fetch_selected_idx,
        format_func=lambda i: f"#{i+1}. {results[i]['candidate_name']} ({results[i]['overall_score']}%)",
        key="detail_select_box"
    )
    st.session_state.fetch_selected_idx = selected_idx
    candidate = results[selected_idx]

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Skill Match", f"{candidate['skill_match']}%")
    m2.metric("Experience Match", f"{candidate['exp_match']}%")
    m3.metric("Overall Score", f"{candidate['overall_score']}%")
    
    # Skills Row
    s1, s2 = st.columns(2)
    with s1:
        st.write("**✅ Matched Skills:**")
        if candidate['matched_skills']:
            for s in candidate['matched_skills'][:10]: st.write(f"⚪ {s}")
        else: st.write("None")
    with s2:
        st.write("**❌ Missing Skills:**")
        if candidate['missing_skills']:
            for s in candidate['missing_skills'][:10]: st.write(f"🔴 {s}")
        else: st.write("None")
        
    st.write("**📝 Summary:**")
    st.info(candidate['summary'])