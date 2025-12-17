
import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import sys


sys.path.insert(0, os.path.dirname(__file__))


# Original imports
try:
    from utils.extract import extract_text_from_file, extract_skills, match_job_skills
    from utils.experience import estimate_experience_years, experience_percentage, classify_experience_level
    from utils.ranking import calculate_final_score
    from utils.analyzer import analyze_resume
    from users_extract import show_resume_tips, show_bonus_videos, recommend_courses_from_resume
    from courses import resume_videos, interview_videos, softskill_links
except ImportError as e:
    st.error(f"Error importing original modules: {e}")


# New imports
from auth import show_auth_page, load_users, hash_password, save_users

# Lazy load dashboard modules with error handling
show_admin_dashboard = None
show_user_dashboard = None

try:
    from single_screen_admin_old import show_admin_dashboard
except Exception as e:
    print(f"⚠️ Warning: Admin dashboard import failed: {e}")

try:
    from single_screen_user_old import show_user_dashboard
except Exception as e:
    print(f"⚠️ Warning: User dashboard import failed: {e}")

from ui_components import set_page_config, show_loading_animation


load_dotenv()


# PAGE CONFIG
set_page_config()


# ==================== LOGO & TITLE ====================
# FIXED: Removed extra quotes around the path
LOGO_PATH = "/Users/akmalhaleema/Desktop/RecruitNova/assets/logo.jpeg"
PROJECT_NAME = "💻RecruitNova"
PROJECT_SUBTITLE = "Hire faster. Hire smarter."


# ==================== THEME MANAGEMENT ====================
def init_theme():
    """Initialize theme in session state"""
    if "app_theme" not in st.session_state:
        st.session_state.app_theme = "dark"  # default to dark


def get_theme_css():
    """Get CSS based on current theme"""
    if st.session_state.app_theme == "dark":
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            
            * {
                font-family: 'Poppins', sans-serif;
            }
            
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0f172a 0%, #1a2744 100%);
            }
            
            [data-testid="stSidebar"] {
                background-color: #1f2937;
            }
            
            [data-testid="stMarkdownContainer"], .stTextInput, .stTextArea, .stSelectbox, .stNumberInput {
                color: #f1f5f9;
            }
            
            .stTextInput > div > div > input,
            .stTextArea textarea,
            .stSelectbox > div > select,
            .stNumberInput > div > div > input {
                background-color: #2d3748 !important;
                color: #f1f5f9 !important;
                border: 1px solid #4a5568 !important;
            }
            
            .stButton > button {
                background: linear-gradient(135deg, #6366f1, #818cf8);
                color: white;
                border: none;
                border-radius: 8px;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #818cf8, #a5b4fc);
            }
        </style>
        """
    else:  # light mode
       
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        :root {
                --bg-primary: #f8f9fa;
                --bg-secondary: #ffffff;
                --text-primary: #1a1a1a;
                --text-secondary: #4a4a4a;
                --accent: #6366f1;
                --accent-hover: #4f46e5;
                --border: #d0d0d0;
            }
            
            body, [data-testid="stAppViewContainer"] {
                background-color: var(--bg-primary) !important;
                color: var(--text-primary) !important;
            }
            
            [data-testid="stSidebar"] {
                background-color: var(--bg-secondary) !important;
                border-right: 1px solid var(--border) !important;
            }
            
            .stButton > button, .stDownloadButton > button {
                background-color: var(--accent) !important;
                color: white !important;
                border: none !important;
            }
            
            .stButton > button:hover, .stDownloadButton > button:hover {
                background-color: var(--accent-hover) !important;
            }
            
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select {
                background-color: white !important;
                color: var(--text-primary) !important;
                border: 1px solid var(--border) !important;
                caret-color: black !important;
            }
            
            .stTextInput > div > div > input::placeholder,
            .stTextArea > div > div > textarea::placeholder {
                color: #999999 !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: var(--text-primary) !important;
            }
            
            p, span, div, label {
                color: var(--text-primary) !important;
            }
            
            .stMarkdown {
                color: var(--text-primary) !important;
            }
            
            .card {
                background-color: var(--bg-secondary) !important;
                border: 1px solid var(--border) !important;
            }
            
            /* File Uploader Styling */
            .stFileUploader > div > div {
                background-color: #f5f5f5 !important;
                border: 2px dashed var(--border) !important;
                color:white; !important;
            }
            
            .stFileUploader [data-testid="stFileUploadDropzone"] {
                background-color: white !important;
            }
            
            .stFileUploader p, .stFileUploader span {
                color: white !important;
            }
            
            /* Form Labels */
            .stForm label {
                color: var(--text-primary) !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: var(--bg-secondary) !important;
                color: var(--text-primary) !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab"] {
                color: var(--text-primary) !important;
            }
            
            /* Select Boxes */
            .stSelectbox [data-baseweb="select"] {
                background-color: white !important;
            }
            
            /* Checkbox and Radio */
            .stCheckbox label, .stRadio label {
                color: var(--text-primary) !important;
            }
            
            /* Metric */
            .stMetric {
                background-color: var(--bg-secondary) !important;
                border-radius: 8px;
                padding: 16px;
                border: 1px solid var(--border) !important;
            }
            
            .stMetric label {
                color: var(--text-secondary) !important;
            }
            
            /* Code Block */
            pre {
                background-color: #f5f5f5 !important;
                color: var(--text-primary) !important;
                border: 1px solid var(--border) !important;
            }
            
            code {
                background-color: #f0f0f0 !important;
                color: var(--text-primary) !important;
            }
            
            /* Alert/Error Messages */
            [data-testid="stAlert"] {
                background-color: var(--bg-secondary) !important;
                color: var(--text-primary) !important;
            }
            
            /* Slider */
            .stSlider [role="slider"] {
                background-color: var(--bg-secondary) !important;
            }
            
            /* Success/Error/Warning messages */
            .stSuccess, .stError, .stWarning, .stInfo {
                background-color: var(--bg-secondary) !important;
                color: var(--text-primary) !important;
            }
        </style>
        """

          


# ==================== SESSION STATE ====================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "user_mode" not in st.session_state:
    st.session_state.user_mode = None
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "admin_password" not in st.session_state:
    st.session_state.admin_password = None
if "is_admin_verified" not in st.session_state:
    st.session_state.is_admin_verified = False
if "profile_updated" not in st.session_state:
    st.session_state.profile_updated = False


init_theme()


# Apply theme CSS
st.markdown(get_theme_css(), unsafe_allow_html=True)


# ==================== PROFILE MANAGEMENT ====================
def get_image_base64(path):
    """Convert image to base64"""
    import base64
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def show_profile_avatar():
    
   
    """Display profile avatar in bottom right (only after login)"""
    if "user_email" not in st.session_state or not st.session_state.user_email:
        return

    profile_image_path = os.path.join("data", "profile_pics", f"{st.session_state.user_email}.png")
    os.makedirs(os.path.dirname(profile_image_path), exist_ok=True)

    if os.path.exists(profile_image_path):
        # Use the new get_user_profile function
        profile = get_user_profile(st.session_state.user_email)
        user_name = profile["name"] or "User"
        
        st.markdown(
            """
            <style>
            .profile-avatar-container {
                position: fixed;
                right: 16px;
                bottom: 16px;
                z-index: 99999;
                text-align: center;
            }
            .profile-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                border: 2px solid #10b981;
                object-fit: cover;
                box-shadow: 0 4px 8px rgba(0,0,0,0.25);
                cursor: pointer;
            }
            .profile-name {
                font-size: 12px;
                font-weight: 600;
                color: #f1f5f9;
                margin-top: 6px;
                white-space: nowrap;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown(f"""
            <div class="profile-avatar-container">
                <img src="data:image/png;base64,{get_image_base64(profile_image_path)}" 
                     class="profile-avatar" />
                <p class="profile-name">{user_name}</p>
            </div>
        """,
        unsafe_allow_html=True,
        )

def show_profile_edit_page():
    """Profile editing page (separate from main dashboard)"""
    st.markdown("## 📝 Edit Profile")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Profile Picture")
        uploaded = st.file_uploader(
            "Upload profile photo (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            key="profile_upload"
        )
        if uploaded is not None:
            from PIL import Image
            img = Image.open(uploaded).convert("RGB")
            img = img.resize((256, 256))
            save_path = os.path.join(
                "data", "profile_pics", f"{st.session_state.user_email}.png"
            )
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            img.save(save_path, format="PNG")
            st.session_state.profile_updated = True
            st.success("✅ Profile photo updated!")
    
    with col2:
        st.subheader("Profile Info")
        profile = get_user_profile(st.session_state.user_email)
        
        name = st.text_input("Full Name", value=profile["name"], key="profile_name")
        bio = st.text_area("Bio", value=profile["bio"], key="profile_bio")
        
        if st.button("Save Profile", type="primary", use_container_width=True):
            save_user_profile(st.session_state.user_email, name, bio)
            st.session_state.profile_updated = True
            st.success("✅ Profile saved successfully!")


# ==================== LANDING PAGE ====================
def show_landing_page():
    """Landing page with logo - FIXED TO DISPLAY LOGO PROPERLY"""
    show_loading_animation()
        
        # Check if logo file exists
    if os.path.exists(LOGO_PATH):
            try:
                # Convert logo to base64 (same as profile avatar)
                logo_base64 = get_image_base64(LOGO_PATH)
                st.markdown(f"""
                <div style="text-align: center; margin: 40px 0;">
                    <img src="data:image/jpeg;base64,{logo_base64}"  style="width:1500px;max-width:100%; height: auto; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />       
                    <h1 style="font-size: 48px; font-weight: 700; margin: 10px 0; background: linear-gradient(135deg, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                       Hiring with RecruitNova
                    </h1>
                    <p style="font-size: 18px; color: #64748b; margin: 15px 0;">
                        {PROJECT_SUBTITLE}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading logo: {e}")
                # Fallback to emoji
                st.markdown(f"""
                <div style="text-align: center; margin: 40px 0;">
                    <div style="font-size: 80px; margin: 20px 0;">ðŸ’»</div>
                    <h1 style="font-size: 48px; font-weight: 700; margin: 10px 0; background: linear-gradient(135deg, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        {PROJECT_NAME}
                    </h1>
                    <p style="font-size: 18px; color: #64748b; margin: 15px 0;">
                        {PROJECT_SUBTITLE}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
            # Fallback if logo doesn't exist
            st.markdown(f"""
            <div style="text-align: center; margin: 40px 0;">
                <div style="font-size: 80px; margin: 20px 0;">ðŸ’»</div>
                <h1 style="font-size: 48px; font-weight: 700; margin: 10px 0; background: linear-gradient(135deg, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {PROJECT_NAME}
                </h1>
                <p style="font-size: 18px; color: #64748b; margin: 15px 0;">
                    {PROJECT_SUBTITLE}
                </p>
                <p style="font-size: 12px; color: #e74c3c;">âš ï¸ Logo not found at {LOGO_PATH}</p>
            </div>
            """, unsafe_allow_html=True)
        
    col_a, col_b = st.columns(2)
    with col_a:
            if st.button("🔐 Sign In", use_container_width=True, key="signin_btn"):
                st.session_state.page = "signin"
                st.rerun()
    with col_b:
            if st.button("📝 Sign Up", use_container_width=True, key="signup_btn"):
                st.session_state.page = "signup"
                st.rerun()

               


# ==================== MODE SELECTION ====================
def show_mode_selection():
    """Show user/admin mode selection with equal card sizes"""


    st.markdown("""
        <style>
            .role-wrapper {
                background: rgba(255, 255, 255, 0.10);
                backdrop-filter: blur(12px);
                border-radius: 22px;
                padding: 40px 25px;
                border: 1px solid rgba(255, 255, 255, 0.25);
                text-align: center;
                height: 350px;             /* FIXED HEIGHT (equal boxes) */
                display: flex;
                flex-direction: column;
                justify-content: space-between;  /* Spread icon, text, button */
                box-shadow: 0 10px 30px rgba(0,0,0,0.18);
                transition: 0.25s ease;
            }


            .role-wrapper:hover {
                transform: translateY(-8px);
                box-shadow: 0 18px 40px rgba(0,0,0,0.28);
            }


            .role-title {
                font-size: 26px;
                font-weight: 700;
                color: white;
                margin-top: 10px;
            }


            .role-text {
                
                   color: #E3E7FF;
                   font-size: 15px;
                   margin-top: 10px;
                   line-height: 1.5;
                   padding: 0 8px;
            
            }


            .role-icon {
                font-size: 65px;
                margin-bottom: 5px;
            }
        </style>
    """, unsafe_allow_html=True)


    # Page title
    st.markdown("""
        <div style="text-align:center; margin-top: 40px; margin-bottom: 50px;">
            <h2 style="font-size: 38px; font-weight: 800; color: white;">
                Select Your Role
            </h2>
        </div>
    """, unsafe_allow_html=True)


    col1, col2, col3 = st.columns([1, 3, 1])


    with col2:
        card_col1, card_col2 = st.columns(2, gap="large")


        # ------------------ Candidate ------------------
        with card_col1:
            st.markdown("""
                <div class="role-wrapper">
                    <div class="role-icon">👤</div>
                    <div class="role-title">Candidate</div>
                    <div class="role-text">
                        Get resume analysis, optimization tips & interview preparation
                    </div>
                </div>
            """, unsafe_allow_html=True)


            if st.button("Enter as Candidate", use_container_width=True, key="candidate_btn"):
             st.session_state.user_mode = "user" 
             st.session_state.page = "profile_setup" 
             st.rerun()


        # ------------------ Recruiter ------------------
        with card_col2:
            st.markdown("""
                <div class="role-wrapper">
                    <div class="role-icon">🧑🏻‍💻👩🏻‍💻</div>
                    <div class="role-title">Recruiter</div>
                    <div class="role-text">
                        Screen resumes, auto-match JD, bulk processing & analytics
                    </div>
                </div>
            """, unsafe_allow_html=True)


            if st.button("Enter as Recruiter", use_container_width=True, key="recruiter_btn"):
             st.session_state.user_mode = "admin"
             st.session_state.page = "admin_password" 
             st.rerun()

# ==================== PROFILE CHECK FUNCTIONS ====================
def has_completed_profile(email):
    """Check if user has already completed their profile"""
    users = load_users()
    user = users.get(email, {})
    
    # Profile is complete if:
    # 1. Name is set AND
    # 2. Profile setup was started (either by saving or skipping)
    name_exists = user.get("name") and user.get("name").strip() != ""
    setup_started = user.get("profile_setup_started", False)
    
    return name_exists or setup_started


def mark_profile_setup_started(email):
    """Mark that user has started profile setup"""
    users = load_users()
    if email in users:
        users[email]["profile_setup_started"] = True
        save_users(users)


def save_user_profile(email, name, bio):
    """Save user profile information"""
    users = load_users()
    if email in users:
        users[email]["name"] = name
        users[email]["bio"] = bio
        users[email]["profile_setup_started"] = True
        users[email]["updated_at"] = datetime.now().isoformat()
        save_users(users)
        return True
    return False


def get_user_profile(email):
    """Get user profile data"""
    users = load_users()
    user = users.get(email, {})
    return {
        "name": user.get("name", ""),
        "bio": user.get("bio", ""),
        "setup_started": user.get("profile_setup_started", False)
    }

def show_profile_setup():
    """Ask for profile update on first login"""
    
    # If user already has profile, skip to dashboard
    if has_completed_profile(st.session_state.user_email):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.markdown("## 👤 Complete Your Profile")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Profile Picture")
        uploaded = st.file_uploader(
            "Upload profile photo (Optional)",
            type=["png", "jpg", "jpeg"],
            key="first_profile_upload"
        )
        if uploaded is not None:
            from PIL import Image
            img = Image.open(uploaded).convert("RGB")
            img = img.resize((256, 256))
            save_path = os.path.join(
                "data", "profile_pics", f"{st.session_state.user_email}.png"
            )
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            img.save(save_path, format="PNG")
            st.success("✅Photo added!")
    
    with col2:
        st.subheader("Basic Info")
        profile = get_user_profile(st.session_state.user_email)
        
        name = st.text_input("Full Name", value=profile["name"], key="first_name")
        bio = st.text_area("Short Bio (Optional)", value=profile["bio"], key="first_bio")
        
        col_skip, col_save = st.columns(2)
        with col_skip:
            if st.button("Skip for Now", use_container_width=True):
                mark_profile_setup_started(st.session_state.user_email)
                st.session_state.page = "dashboard"
                st.rerun()
        
        with col_save:
            if st.button("Save & Continue", use_container_width=True, type="primary"):
                if name and name.strip():
                    save_user_profile(st.session_state.user_email, name, bio)
                    st.session_state.page = "dashboard"
                    st.session_state.profile_updated = True
                    st.rerun()
                else:
                    st.warning("‼️ Please enter your name")





# ==================== ADMIN PASSWORD ====================
def ensure_admin_auth():
    """Admin authentication per account"""
    users = load_users()
    email = st.session_state.get("user_email")
    if not email:
        st.error("Session error: user email not found. Please log in again.")
        return False


    user = users.get(email)
    if user is None:
        st.error("User not found")
        return False


    if user.get("admin_password") is None:
        st.subheader("Set admin password for this account")
        ap1 = st.text_input("Admin password", type="password", key="adm_p1")
        ap2 = st.text_input("Confirm admin password", type="password", key="adm_p2")
        if st.button("Save admin password"):
            if not ap1 or ap1 != ap2:
                st.error("Passwords do not match")
            else:
                user["admin_password"] = hash_password(ap1)
                save_users(users)
                st.success("Admin password set. Please enter it again to continue.")
        return False
    else:
        st.subheader("Enter admin password")
        ap = st.text_input("Admin password", type="password", key="adm_login")
        if st.button("Enter admin area"):
            if user["admin_password"] == hash_password(ap):
                st.session_state.is_admin_verified = True
                st.session_state.page = "profile_setup"
                st.success("Admin access granted")
                st.rerun()
                return True
            else:
                st.error("Incorrect admin password")
                return False


# ==================== THEME SWITCHER IN SIDEBAR ====================
def show_theme_switcher():
    """Theme switcher in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Theme")
    
    theme_option = st.sidebar.radio(
        "Select Theme:",
        ["Dark", "Light"],
        index=0 if st.session_state.app_theme == "dark" else 1,
        key="theme_selector"
    )
    
    if theme_option == "Dark" and st.session_state.app_theme != "dark":
        st.session_state.app_theme = "dark"
        st.rerun()
    elif theme_option == "Light" and st.session_state.app_theme != "light":
        st.session_state.app_theme = "light"
        st.rerun()


# ==================== MAIN APP LOGIC ====================
def main():
    # Header with logo (only on non-landing pages)
    if st.session_state.page != "landing":
        col1, col2, col3 = st.columns([1, 3, 2])
        with col1:
            st.markdown(f"### {PROJECT_NAME}")


    # Show theme switcher on all pages when logged in
    if st.session_state.user_logged_in or st.session_state.admin_logged_in:
        show_theme_switcher()


    # ==================== PAGE ROUTING ====================
    if st.session_state.page == "landing":
        show_landing_page()
    
    elif st.session_state.page == "signin":
        show_auth_page("signin")
    
    elif st.session_state.page == "signup":
        show_auth_page("signup")
    
    elif st.session_state.page == "mode_selection":
        show_mode_selection()
    
    elif st.session_state.page == "profile_setup":
        show_profile_setup()
    
    elif st.session_state.page == "profile_edit":
        show_profile_edit_page()
        if st.button("⬅️ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
    
    elif st.session_state.page == "admin_password":
        st.markdown("<h2 style='text-align: center;'>🔓 Recruiter Access</h2>", unsafe_allow_html=True)
        if st.session_state.get("is_admin_verified"):
            st.session_state.page = "profile_setup"
            st.rerun()
        else:
            ensure_admin_auth()
    
    elif st.session_state.page == "dashboard":
        if st.session_state.user_mode == "user":
            # User mode with profile avatar
            show_user_dashboard()
            show_profile_avatar()
            
            # Profile edit button in sidebar
            if st.sidebar.button("✍🏽 Edit Profile", use_container_width=True):
                st.session_state.page = "profile_edit"
                st.rerun()
        
        elif st.session_state.user_mode == "admin":
            if st.session_state.get("is_admin_verified"):
                show_admin_dashboard()
                show_profile_avatar()
                
                # Profile edit button in sidebar
                if st.sidebar.button("✍🏽 Edit Profile", use_container_width=True):
                    st.session_state.page = "profile_edit"
                    st.rerun()
            else:
                st.session_state.page = "admin_password"
                st.rerun()

    # ==================== SIDEBAR ====================
        with st.sidebar:
            st.markdown("<div style='margin-top: -20px;'></div>", unsafe_allow_html=True)
            if st.session_state.user_logged_in or st.session_state.admin_logged_in:
                    if st.button("⬅️ Logout", use_container_width=True):
                      st.session_state.user_logged_in = False
                      st.session_state.admin_logged_in = False
                      st.session_state.is_admin_verified = False
                      st.session_state.page = "landing"
                      st.session_state.user_mode = None
                      st.session_state.user_email = None
                      st.rerun()
        
            st.markdown("---")
            st.markdown("### ℹ️ About RecruitNova")
            st.markdown("""
        An intelligent AI-powered recruitment screening tool designed to:
        
        **For Candidates:**
        - 📊 Resume analysis & scoring
        - 💡 Keyword optimization
        - 💼 Alternative role suggestions
        - 🗣️ AI interview prep
        
        **For Recruiters:**
        - 📑 Single & bulk resume screening
        - ✔️ JD-driven auto-matching
        - 🔁 Duplicate detection
        - 🔎Analytics & rankings
        """)
        
            st.markdown("---")
            st.markdown("""
        <div style="text-align: center; font-size: 12px; color: #64748b;">
            <p> 2025 RecruitNova</p>
            <p>Built by team RecruitNova</p>
        </div>
        """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()