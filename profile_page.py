import streamlit as st
from auth import update_profile, get_user_profile
import time

def show_profile_form():
    """Display the profile setup form"""
    
    # Theme config (Light/Dark awareness)
    theme = st.session_state.get("app_theme", "light")
    if theme == "dark":
        text_color = "white"
        sub_text = "#94a3b8"
    else:
        text_color = "#1e293b"
        sub_text = "#475569"

    st.markdown(f"""
    <style>
        .profile-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }}
        h2 {{ color: {text_color} !important; }}
        p {{ color: {sub_text} !important; }}
    </style>
    """, unsafe_allow_html=True)

    # Fetch existing data
    existing_profile, is_complete = get_user_profile(st.session_state.user_email)
    
    # AUTO-REDIRECT: If Candidate mode user with complete profile, skip to dashboard
    # Auto-redirect logic removed to allow profile editing
    # if is_complete and st.session_state.get("user_mode") == "user":
    #     ...
    
    # Container
    with st.container():
        st.markdown("<div class='profile-container'>", unsafe_allow_html=True)
        
        # Header
        if not is_complete:
            st.markdown("<h2>🚀 Complete Your Profile</h2>", unsafe_allow_html=True)
            st.markdown("<p>Let's get to know you better. This info helps us personalize your experience.</p>", unsafe_allow_html=True)
        else:
            col_head, col_back = st.columns([3, 1])
            with col_head:
                st.markdown("<h2>👤 Edit Profile</h2>", unsafe_allow_html=True)
            with col_back:
                if st.button("⬅ Dashboard", key="profile_back_btn"):
                    st.session_state.page = "dashboard"
                    st.session_state.dashboard_page = "home"
                    # Fix blank screen: Ensure user_mode is set
                    if not st.session_state.get("user_mode"):
                        st.session_state.user_mode = "user"
                    st.rerun()
            st.markdown("<p>Update your professional details.</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Form
        with st.form("profile_setup_form"):
            # Profile Photo Section
            col_photo, col_info = st.columns([1, 3])
            
            with col_photo:
                st.markdown("**Profile Photo**")
                uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
                if uploaded_file:
                    st.image(uploaded_file, width=100, caption="Preview")
            
            with col_info:
                col1, col2 = st.columns(2)
                with col1:
                    role = st.text_input("Current Role / Title", value=existing_profile.get("role", ""), placeholder="e.g. Software Engineer")
                    linkedin = st.text_input("LinkedIn URL", value=existing_profile.get("linkedin", ""), placeholder="https://linkedin.com/in/...")
                
                with col2:
                    experience = st.selectbox(
                        "Years of Experience", 
                        ["0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
                        index=["0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"].index(existing_profile.get("experience", "1-3 years")) if existing_profile.get("experience") else 1
                    )
                    location = st.text_input("Location", value=existing_profile.get("location", ""), placeholder="City, Country")

            skills = st.text_area("Key Skills (comma separated)", value=existing_profile.get("skills", ""), placeholder="Python, React, Leadership...")
            bio = st.text_area("Professional Bio", value=existing_profile.get("bio", ""), placeholder="Brief summary...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Save Profile", type="primary", use_container_width=True)
            
            if submitted:
                if not role or not skills:
                    st.error("Please fill in at least your Role and Skills.")
                else:
                    # Save Photo if uploaded
                    if uploaded_file:
                        try:
                            import os
                            from PIL import Image
                            img = Image.open(uploaded_file).convert("RGB")
                            # Resize for avatar usage
                            img = img.resize((300, 300))
                            
                            save_dir = os.path.join("data", "profile_pics")
                            os.makedirs(save_dir, exist_ok=True)
                            
                            save_path = os.path.join(save_dir, f"{st.session_state.user_email}.png")
                            img.save(save_path, format="PNG")
                        except Exception as e:
                            st.warning(f"Could not save photo: {e}")

                    profile_data = {
                        "role": role,
                        "linkedin": linkedin,
                        "experience": experience,
                        "location": location,
                        "skills": skills,
                        "bio": bio
                    }
                    
                    success, msg = update_profile(st.session_state.user_email, profile_data)
                    
                    if success:
                        st.success("Profile saved! Redirecting...")
                        time.sleep(1)
                        # Ensure session state is valid for dashboard
                        st.session_state.page = "dashboard"
                        st.session_state.dashboard_page = "home" 
                        if not st.session_state.get("user_mode"):
                            st.session_state.user_mode = "user" # Default to user if lost
                        st.rerun()
                    else:
                        st.error(msg)
            
            # Skip Button for users stuck in loop
            st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
            if st.form_submit_button("Skip & Go to Dashboard (Setup Later)", type="secondary", use_container_width=True):
                 st.session_state.page = "dashboard"
                 st.session_state.dashboard_page = "home"
                 if not st.session_state.get("user_mode"): st.session_state.user_mode = "user"
                 st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
