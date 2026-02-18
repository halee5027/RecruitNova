import streamlit as st
import os
import base64
import textwrap
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
from auth import show_auth_page, load_users, hash_password, save_users, get_user_profile
from profile_page import show_profile_form

# Lazy load dashboard modules with error handling
show_admin_dashboard = None
admin_dashboard_error = None
show_user_dashboard = None
user_dashboard_error = None

try:
    from single_screen_admin_old import show_admin_dashboard
except Exception as e:
    admin_dashboard_error = str(e)
    print(f"⚠️ Warning: Admin dashboard import failed: {e}")

try:
    from single_screen_user_old import show_user_dashboard
except Exception as e:
    user_dashboard_error = str(e)
    print(f"⚠️ Warning: User dashboard import failed: {e}")

from ui_components import set_page_config, show_loading_animation


load_dotenv()


# PAGE CONFIG
set_page_config()


# ==================== LOGO & TITLE ====================
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.jpeg")
PROJECT_NAME = "RecruitNova"
PROJECT_SUBTITLE = "AI-Powered Recruitment Intelligence"


# ==================== LANDING PAGE ====================
def show_landing_page():
    """Landing page with centered large logo and premium buttons"""
    # Centered Logo Container
    # Professional Native Layout
    # Professional Native Layout
    if os.path.exists(LOGO_PATH):
        # Determine Theme Colors
        theme = st.session_state.get("app_theme", "light")
        
        if theme == "dark":
            bg_gradient = "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)"
            h1_gradient = "linear-gradient(135deg, #fff 0%, #a5b4fc 100%)"
            subtitle_color = "#94a3b8"
            input_bg = "rgba(255, 255, 255, 0.05)"
            input_text = "white"
        else:
            # Light Theme Colors - Professional Blue/Purple
            bg_gradient = "linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)"
            h1_gradient = "linear-gradient(135deg, #1e293b 0%, #4338ca 100%)" # Dark Blue to Indigo
            subtitle_color = "#475569" # Slate 600
            input_bg = "rgba(255, 255, 255, 0.8)"
            input_text = "#0f172a"
        
        # Animation Logic
        anim_css = "none"
        if st.session_state.get("exit_anim"):
            anim_css = "swirlMinimize 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) forwards"
            # Hide other elements during animation
            extra_css = """
                [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] p, .stButton {
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
            """
        else:
            extra_css = ""

        # 1. Clean Styling with Theme Awareness + Animation
        st.markdown(f"""
        <style>
            @keyframes swirlMinimize {{
                0% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
                20% {{ transform: scale(1.1) rotate(-10deg); opacity: 1; }} /* Anticipation */
                100% {{ transform: scale(0) rotate(720deg); opacity: 0; }}
            }}
        
            /* Global Background */
            [data-testid="stAppViewContainer"] {{
                background: {bg_gradient} !important;
            }}
            
            /* Typography Polish */
            [data-testid="stMarkdownContainer"] h1 {{
                text-align: center;
                font-size: 3.5rem !important;
                font-weight: 800 !important;
                background: {h1_gradient};
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem !important;
            }}
            [data-testid="stMarkdownContainer"] p {{
                text-align: center;
                font-size: 1.2rem !important;
                color: {subtitle_color} !important;
            }}
            
            /* Logo Polish - Circular layout */
            [data-testid="stImage"] img {{
                border-radius: 50% !important;
                border: 2px solid rgba(255,255,255,0.1) !important;
                box-shadow: 0 0 20px rgba(99, 102, 241, 0.3) !important;
                margin: 0 auto !important;
                display: block !important;
                animation: {anim_css} !important;
            }}
            
            /* Hide Streamlit Branding */
            footer, header, [data-testid="stHeader"] {{ visibility: hidden; }}
            
            /* Layout Spacing - Zero Scroll */
            .block-container {{ padding-top: 2vh !important; }}
            [data-testid="stVerticalBlock"] {{ gap: 0.5rem !important; }}
            
            /* Button Text Visibility Fix */
            .stButton button p {{
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                color: #ffffff !important; /* Force white text on primary buttons */
                text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
            }}
            
            {extra_css}
        </style>
        """, unsafe_allow_html=True)

        # 2. Native Image Component (Safe & Reliable)
        _, col_img, _ = st.columns([1, 0.6, 1])
        with col_img:
            st.image(LOGO_PATH, use_column_width=True)
            
        # Handle Animation Exit
        if st.session_state.get("exit_anim"):
            import time
            time.sleep(1.5)
            st.session_state.page = st.session_state.target_page
            st.session_state.exit_anim = False # Reset
            st.rerun()

        # 3. Native Text Components
        st.title(PROJECT_NAME)
        st.markdown(f"<p style='text-align: center; font-size: 1.1rem; margin-top: -1rem; margin-bottom: 2rem;'>{PROJECT_SUBTITLE}</p>", unsafe_allow_html=True)
        
        # 4. Buttons (Same Color, Zero Scroll)
        col_login, col_signup = st.columns(2, gap="medium")
        with col_login:
            if st.button("🔐 Login", use_container_width=True, type="primary", key="landing_login"):
                st.session_state.exit_anim = True
                st.session_state.target_page = "signin"
                st.rerun()
        with col_signup:
            if st.button("🔑 Create Account", use_container_width=True, type="primary", key="landing_signup"):
                st.session_state.exit_anim = True
                st.session_state.target_page = "signup"
                st.rerun()

    else:
        st.title(PROJECT_NAME)
        st.subheader(PROJECT_SUBTITLE)
        
    # CSS Cleanup
    st.markdown("""
    <style>
        /* Hide Streamlit stuff */
        footer, #MainMenu, header, [data-testid="stHeader"] {visibility: hidden; display: none !important;}
        
        /* Layout Adjustments */
        .block-container { padding-top: 3rem !important; }
        
        /* Button Polish */
        .stButton button {
            border-radius: 12px !important;
            height: 50px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)


# ==================== MODE SELECTION ====================
def show_mode_selection():
    """Show user/admin mode selection - ULTRA COMPACT"""
    
    theme = st.session_state.get("app_theme", "dark")
    card_bg = "rgba(255, 255, 255, 0.05)" if theme == "dark" else "rgba(255, 255, 255, 0.9)"
    text_color = "#ffffff" if theme == "dark" else "#1e293b"

    st.markdown(f"""
        <style>
            .block-container {{ padding: 1rem !important; max-width: 900px !important; }}
            .compact-title {{ font-size: 1.8rem; margin: 0.5rem 0; text-align: center;
                background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .mode-card {{ background: {card_bg}; border-radius: 12px; padding: 1.5rem 1rem;
                text-align: center; border: 1px solid rgba(255,255,255,0.1); }}
            .mode-icon {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
            .mode-title {{ font-size: 1.3rem; font-weight: 600; color: {text_color}; margin-bottom: 0.3rem; }}
            .mode-desc {{ font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 1rem; }}
            div.stButton > button {{ background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%) !important;
                color: white !important; border: none !important; padding: 0.5rem !important; }}
        </style>
        <h1 class="compact-title">Choose Your Path</h1>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown(f"""
            <div class="mode-card">
                <div class="mode-icon">👤</div>
                <div class="mode-title">Candidate</div>
                <div class="mode-desc">Resume analysis & interview prep</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Enter as Candidate", key="btn_c", use_container_width=True):
             st.session_state.user_mode = "user"
             user_email = st.session_state.get("user_email")
             
             # Smart redirect: Profile page only for new users, Dashboard for existing
             if user_email:
                 profile_data, is_complete = get_user_profile(user_email)
                 if is_complete:
                     st.session_state.page = "dashboard"
                 else:
                     st.session_state.page = "profile"
             else:
                 st.session_state.page = "profile"
             
             st.rerun()

    with col2:
        st.markdown(f"""
            <div class="mode-card">
                <div class="mode-icon">💼</div>
                <div class="mode-title">Recruiter</div>
                <div class="mode-desc">Bulk resume screening & ranking</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Enter as Recruiter", key="btn_r", use_container_width=True):
             st.session_state.user_mode = "admin"
             st.session_state.page = "admin_password"
             st.rerun()


# ==================== FLOATING AVATAR ====================
def show_floating_avatar():
    """Show floating profile picture in bottom right"""
    if not st.session_state.get("user_logged_in"):
        return

    email = st.session_state.get("user_email")
    if not email:
        return
        
    profile_pic_path = os.path.join("data", "profile_pics", f"{email}.png")
    
    if os.path.exists(profile_pic_path):
        with open(profile_pic_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode()
            
        st.markdown(f"""
        <style>
            .floating-avatar {{
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-image: url(data:image/png;base64,{b64_img});
                background-size: cover;
                background-position: center;
                border: 3px solid #6366f1;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                z-index: 99999;
                transition: transform 0.3s ease;
                cursor: pointer;
            }}
            .floating-avatar:hover {{
                transform: scale(1.1);
                box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
            }}
        </style>
        <a href="#" id="avatar-link" onclick="window.parent.document.querySelector('button[key=nav_edit_profile]').click(); return false;">
            <div class="floating-avatar" title="Your Profile"></div>
        </a>
        """, unsafe_allow_html=True)


# ==================== NAVBAR ====================
def show_navbar():
    """Top Navigation Bar with Logo - MOCKUP MATCH"""
    
    with st.container():
        # Use columns for layout: [Logo+Name] [Spacer] [Controls]
        col_logo, col_spacer, col_controls = st.columns([2, 4, 3])
        
        # Logo Area (Left)
        with col_logo:
            if st.session_state.page != "landing":
                # Show minimized logo with name
                if os.path.exists(LOGO_PATH):
                    logo_b64 = get_image_base64(LOGO_PATH)
                    st.markdown(f"""
                        <div style='display: flex; align-items: center; gap: 10px;'>
                            <img src="data:image/png;base64,{logo_b64}" class="logo-img-small" alt="Logo">
                            <span style='font-size: 18px; font-weight: 700; color: inherit;'>{PROJECT_NAME}</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"### {PROJECT_NAME}")

        # Controls Area (Right)
        with col_controls:
            # Determine if user is logged in
            is_logged_in = st.session_state.user_logged_in or st.session_state.admin_logged_in
            
            if is_logged_in:
                # Layout: [Spacer] [Theme] [Profile] [Logout]
                c1, c2, c3, c4 = st.columns([2, 1, 1.5, 1.5]) 
                
                # Theme Toggle (Square button)
                with c2:
                    current_theme = st.session_state.app_theme
                    btn_icon = "🌞" if current_theme == "dark" else "🌙"
                    if st.button(btn_icon, key="nav_theme_toggle", help="Toggle Theme", use_container_width=False):
                        st.session_state.app_theme = "light" if current_theme == "dark" else "dark"
                        st.rerun()
                
                # Edit Profile
                with c3:
                    if st.button("👤 Profile", key="nav_edit_profile", use_container_width=True):
                        st.session_state.page = "profile"
                        st.rerun()
                
                # Logout
                with c4:
                    if st.button("🚪 Logout", key="nav_logout", use_container_width=True, type="secondary"):
                        st.session_state.user_logged_in = False
                        st.session_state.admin_logged_in = False
                        st.session_state.is_admin_verified = False
                        st.session_state.page = "landing"
                        st.session_state.user_mode = None
                        st.session_state.user_email = None
                        st.rerun()
            else:
                # Not logged in: Just Theme Toggle aligned right
                c1, c2 = st.columns([7, 1])
                with c2:
                    current_theme = st.session_state.app_theme
                    btn_icon = "🌞" if current_theme == "dark" else "🌙"
                    if st.button(btn_icon, key="nav_theme_toggle", help="Toggle Theme", use_container_width=False):
                        st.session_state.app_theme = "light" if current_theme == "dark" else "dark"
                        st.rerun()
    
    # Add spacing after navbar
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)


# ==================== MAIN APP LOGIC ====================
def main():
    # Initialize Theme
    init_theme()
    
    # Inject Global CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Show Navbar at the top of every page
    show_navbar()
    show_floating_avatar()
    
    # Spacer for separation
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # ==================== PAGE ROUTING ====================
    
    if st.session_state.page == "landing":
        show_landing_page()
    
    elif st.session_state.page == "signin":
        show_auth_page("signin")
    
    elif st.session_state.page == "signup":
        show_auth_page("signup")
    
    elif st.session_state.page == "mode_selection":
        show_mode_selection()
    
    elif st.session_state.page == "profile":
        show_profile_form()
    
    elif st.session_state.page == "profile_setup":
        # Backward compatibility - redirect to new route
        st.session_state.page = "profile"
        st.rerun()
    
    elif st.session_state.page == "admin_password":
        st.markdown("<div class='glass-card'><h2 style='text-align: center;'>🔐 Recruiter Access</h2></div>", unsafe_allow_html=True)
        if st.session_state.get("is_admin_verified"):
            st.session_state.page = "dashboard" # Redirect to dashboard directly if verified
            st.rerun()
        else:
            ensure_admin_auth()
    
    elif st.session_state.page == "dashboard":
        if st.session_state.user_mode == "user":
            if show_user_dashboard:
                show_user_dashboard()
            else:
                st.error("Failed to load User Dashboard module.")
                if user_dashboard_error:
                    st.error(f"Error details: {user_dashboard_error}")
                st.info("Please check if 'single_screen_user_old.py' and its dependencies are correct.")
        
        elif st.session_state.user_mode == "admin":
            if st.session_state.get("is_admin_verified"):
                if show_admin_dashboard:
                    show_admin_dashboard()
                else:
                    st.error("Failed to load Admin Dashboard module.")
                    if admin_dashboard_error:
                        st.error(f"Error details: {admin_dashboard_error}")
            else:
                st.session_state.page = "admin_password"
                st.rerun()










# ==================== THEME MANAGEMENT ====================
def init_theme():
    """Initialize theme in session state"""
    if "app_theme" not in st.session_state:
        st.session_state.app_theme = "dark"  # default to dark


def get_theme_css():
    """Get CSS based on current theme - EXACT MOCKUP MATCH"""
    
    # Common fonts and basics
    base_css = textwrap.dedent("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', 'Poppins', sans-serif !important;
        }
        
        /* HIDE STREAMLIT ELEMENTS */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* SIDEBAR REMOVAL */
        [data-testid="stSidebar"] { display: none !important; }
        
        /* LOGO STYLES - Swiggy-like minimization */
        .logo-img-large {
            width: 60px;
            height: 60px;
            margin-bottom: 0.5rem;
        }
        
        .logo-img-small {
            width: 32px;
            height: 32px;
            transition: all 0.3s ease;
        }
        
        /* SQUARE THEME TOGGLE BUTTON */
        .stButton > button[key="nav_theme_toggle"] {
            min-width: 40px !important;
            max-width: 40px !important;
            width: 40px !important;
            height: 40px !important;
            padding: 0 !important;
            border-radius: 8px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
    </style>
    """)

    if st.session_state.app_theme == "dark":
        return base_css + textwrap.dedent("""
        <style>
            /* SOLID DARK BACKGROUND (default for all pages) */
            [data-testid="stAppViewContainer"] {
                background: #0f172a;
                color: #ffffff;
            }
            
            /* GRADIENT BACKGROUND CLASS (for landing/auth pages only) */
            .gradient-bg {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%) !important;
                background-size: 400% 400% !important;
                animation: gradientShift 15s ease infinite !important;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* GLASS CARD STYLE */
            .glass-card {
                background: rgba(255, 255, 255, 0.15) !important;
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 20px;
                padding: 2.5rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
                transition: all 0.3s ease;
            }
            
            /* Dashboard cards only - rectangular aspect ratio to match mockup */
            .dashboard-card {
                aspect-ratio: 4 / 3;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding: 1.5rem !important;
            }
            
            .glass-card:hover {
                background: rgba(255, 255, 255, 0.2) !important;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15) !important;
                transform: translateY(-4px);
            }
            
            .glass-card h4 {
                color: #ffffff !important;
                margin: 1rem 0 0.5rem 0;
            }
            
            .glass-card p {
                color: rgba(255, 255, 255, 0.8) !important;
            }

            /* INPUT FIELDS */
            .stTextInput > div > div > input, 
            .stTextArea > div > div > textarea, 
            .stSelectbox > div > div > select {
                background-color: rgba(255, 255, 255, 0.95) !important;
                color: #1a202c !important;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 0.75rem 1rem;
                caret-color: #1a202c !important;
            }
            
            /* CRITICAL: Text visibility for disabled inputs (Email Draft, Optimization) */
            .stTextArea > div > div > textarea:disabled,
            .stTextInput > div > div > input:disabled {
                background-color: rgba(255, 255, 255, 0.85) !important;
                color: #1a202c !important;
                -webkit-text-fill-color: #1a202c !important; /* Force color override */
                opacity: 1 !important;
                border-color: rgba(255, 255, 255, 0.2) !important;
            }

            .stTextInput > div > div > input::placeholder,
            .stTextArea > div > div > textarea::placeholder {
                color: #64748b !important;
                opacity: 0.7 !important;
            }
            .stTextInput > div > div > input:focus, 
            .stTextArea > div > div > textarea:focus {
                border-color: #06b6d4;
                box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.2);
                outline: none;
            }

            /* PRIMARY BUTTON (Gradient) - ENHANCED SPECIFICITY */
            button[kind="primary"], 
            button[data-testid="baseButton-primary"],
            .stButton > button[kind="primary"],
            div[data-testid="column"] button[kind="primary"] {
                background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                padding: 0.75rem 1.5rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
            }
            button[kind="primary"]:hover,
            button[data-testid="baseButton-primary"]:hover,
            .stButton > button[kind="primary"]:hover,
            div[data-testid="column"] button[kind="primary"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
            }
            
            /* SECONDARY BUTTON (Ghost/Navbar) */
            button[kind="secondary"] {
                background-color: rgba(255, 255, 255, 0.1) !important;
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                border-radius: 10px !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
            }
            button[kind="secondary"]:hover {
                background-color: rgba(255, 255, 255, 0.2) !important;
                border-color: rgba(255, 255, 255, 0.5) !important;
            }
            
            /* FALLBACK FOR NORMAL BUTTONS */
            .stButton > button:not([kind="primary"]) {
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                color: white !important;
                border-radius: 10px !important;
            }
            .stButton > button:not([kind="primary"]):hover {
                background-color: rgba(255, 255, 255, 0.2) !important;
            }
            
            /* HEADERS */
            h1, h2, h3 {
                color: #ffffff !important;
                font-family: 'Poppins', sans-serif !important;
                font-weight: 700;
            }
            
            p, label, span, div {
                color: rgba(255, 255, 255, 0.95) !important;
            }
            
            /* TABS STYLING */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 0.5rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: rgba(255, 255, 255, 0.2) !important;
                color: white !important;
            }
            
            /* CRITICAL FIX: Tables should have DARK text on LIGHT background even in dark mode */
            table, .stTable, [data-testid="stTable"] {
                background-color: #ffffff !important;
            }
            
            table *, .stTable *, [data-testid="stTable"] * {
                color: #1f2937 !important;
                background-color: #ffffff !important;
            }
            
            thead, thead * {
                background-color: #f3f4f6 !important;
                color: #111827 !important;
            }
            
            /* CRITICAL FIX: TextAreas should have DARK text on LIGHT background */
            .stTextArea > div > div > textarea {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                opacity: 1 !important;
            }
            
            .stTextArea > div > div > textarea:disabled {
                background-color: #f9fafb !important;
                color: #374151 !important;
                opacity: 1 !important;
            }
            
            /* Nuclear option for textareas - target everything */
            textarea {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                opacity: 1 !important;
            }
            
            textarea:disabled {
                background-color: #f9fafb !important;
                color: #374151 !important;
                opacity: 1 !important;
            }
            
            /* Target Streamlit's internal textarea wrapper */
            [data-baseweb="textarea"] {
                background-color: #ffffff !important;
                color: #1f2937 !important;
            }
            
            [data-baseweb="textarea"] textarea {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                opacity: 1 !important;
            }
            
         </style>
        """)
    else:  # Light Mode
        return base_css + textwrap.dedent("""
        <style>
            /* PURE WHITE BACKGROUND (default for all pages) */
            [data-testid="stAppViewContainer"] {
                background: #ffffff !important;
                color: #1a202c;
            }
            
            /* GRADIENT BACKGROUND CLASS (for landing/auth pages only) */
            .gradient-bg {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #f5f7fa 40%, #c3cfe2 100%) !important;
                background-attachment: fixed !important;
            }
            
            /* TOP ACCENT GRADIENT (for landing/auth pages) */
            .gradient-bg::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 150px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #06b6d4 100%);
                opacity: 0.8;
                z-index: -1;
                pointer-events: none;
            }

            /* CARD STYLE - Clean white with prominent shadow */
            .glass-card {
                background: #ffffff !important;
                border: 1px solid #e5e7eb !important;
                border-radius: 16px;
                padding: 2.5rem;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08) !important;
                transition: all 0.3s ease;
            }
            
            /* Dashboard cards only - rectangular aspect ratio to match mockup */
            .dashboard-card {
                aspect-ratio: 4 / 3;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding: 1.5rem !important;
            }
            
            .glass-card:hover {
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15), 0 4px 12px rgba(0, 0, 0, 0.1) !important;
                transform: translateY(-4px);
            }
            
            .glass-card h4 {
                color: #111827 !important;
                margin: 1rem 0 0.5rem 0;
            }
            
            .glass-card p {
                color: #6b7280 !important;
            }
            
            /* CRITICAL: Text color overrides for light mode */
            h1, h2, h3, h4, h5, h6 {
                color: #111827 !important;
            }
            
            p, label, span, div, td, th, li, code {
                color: #1a202c !important;
                opacity: 1 !important;
            }
            
            /* Tables and dataframes */
            table, .dataframe {
                color: #1a202c !important;
            }
            
            thead th, .dataframe th {
                background-color: #f3f4f6 !important;
                color: #111827 !important;
                font-weight: 600 !important;
            }
            
            tbody td, .dataframe td {
                color: #374151 !important;
            }
            
            /* Streamlit specific elements */
            .stMarkdown, .stText, .element-container, .stDataFrame {
                color: #1a202c !important;
            }
            
            /* Streamlit DataFrame specific fixes */
            [data-testid="stDataFrame"] {
                color: #1a202c !important;
            }
            
            [data-testid="stDataFrame"] table {
                color: #1a202c !important;
                background-color: #ffffff !important;
            }
            
            [data-testid="stDataFrame"] thead {
                background-color: #f9fafb !important;
            }
            
            [data-testid="stDataFrame"] th {
                color: #111827 !important;
                background-color: #f3f4f6 !important;
                font-weight: 600 !important;
                border-bottom: 2px solid #e5e7eb !important;
            }
            
            [data-testid="stDataFrame"] td {
                color: #374151 !important;
                background-color: #ffffff !important;
                border-bottom: 1px solid #f3f4f6 !important;
            }
            
            [data-testid="stDataFrame"] tbody tr:hover {
                background-color: #f9fafb !important;
            }
            
            /* Additional table element targeting */
            .row-widget.stDataFrame table tbody tr td {
                color: #1f2937 !important;
                background-color: #ffffff !important;
            }
            
            .row-widget.stDataFrame table thead tr th {
                color: #111827 !important;
                background-color: #f3f4f6 !important;
            }
            
            /* Ensure all table cells have proper styling */
            .stDataFrame td div {
                color: #1f2937 !important;
            }
            
            .stDataFrame th div {
                color: #111827 !important;
            }
            
            /* Nuclear option - target ALL text in dataframes */
            [data-testid="stDataFrame"] * {
                color: #1f2937 !important;
                opacity: 1 !important;
            }
            
            [data-testid="stDataFrame"] thead * {
                color: #111827 !important;
                opacity: 1 !important;
            }
            
            /* Override any remaining white text */
            div[data-testid="stDataFrame"] div[data-testid="stDataFrameResizable"] * {
                color: #1f2937 !important;
                opacity: 1 !important;
            }
            
            /* Remove any potential overlays */
            [data-testid="stDataFrame"]::before,
            [data-testid="stDataFrame"]::after {
                display: none !important;
            }
            
            /* Ensure cells have no transparent backgrounds */
            [data-testid="stDataFrame"] td,
            [data-testid="stDataFrame"] th {
                background-color: #ffffff !important;
                opacity: 1 !important;
            }

            /* INPUT FIELDS */
            .stTextInput > div > div > input, 
            .stTextArea > div > div > textarea, 
            .stSelectbox > div > div > select {
                background-color: #ffffff !important;
                color: #1a202c !important;
                border: 1px solid #d1d5db !important;
                border-radius: 12px;
                padding: 0.75rem 1rem;
                caret-color: #1a202c !important;
            }
            
            /* CRITICAL: Disabled textareas (like Resume Preview) - ENHANCED VISIBILITY */
            .stTextArea > div > div > textarea:disabled,
            .stTextInput > div > div > input:disabled {
                background-color: #f3f4f6 !important;
                color: #1f2937 !important;
                -webkit-text-fill-color: #1f2937 !important; /* Force color */
                opacity: 1 !important;
                border: 1px solid #d1d5db !important;
            }
            
            .stTextInput > div > div > input::placeholder,
            .stTextArea > div > div > textarea::placeholder {
                color: #9ca3af !important;
                opacity: 1 !important;
            }
            .stTextInput > div > div > input:focus, 
            .stTextArea > div > div > textarea:focus {
                border-color: #4f46e5 !important;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
                outline: none;
            }

            /* PRIMARY BUTTON */
            button[kind="primary"] {
                background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                padding: 0.75rem 1.5rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
            }
            button[kind="primary"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35) !important;
            }
            
            /* SECONDARY BUTTON */
            button[kind="secondary"] {
                background-color: white !important;
                color: #1a202c !important;
                border: 1px solid #d1d5db !important;
                border-radius: 10px !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
            }
            button[kind="secondary"]:hover {
                background-color: #f9fafb !important;
                border-color: #9ca3af !important;
            }
            
            /* FALLBACK FOR NORMAL BUTTONS */
            .stButton > button:not([kind="primary"]) {
                background-color: white !important;
                border: 1px solid #d1d5db !important;
                color: #1a202c !important;
                border-radius: 10px !important;
            }
            .stButton > button:not([kind="primary"]):hover {
                background-color: #f9fafb !important;
            }
            
            /* HEADERS - Dark and visible */
            h1, h2, h3 {
                color: #111827 !important;
                font-family: 'Poppins', sans-serif !important;
                font-weight: 700;
            }

            /* TEXT - Dark gray for visibility */
            p, label, span, div, .stMarkdown {
                color: #374151 !important;
            }
            
            /* Streamlit specific text elements */
            .stMarkdown p, .stMarkdown div, .stMarkdown span {
                color: #374151 !important;
            }
            
            /* TABS STYLING */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: #f3f4f6;
                border-radius: 12px;
                padding: 0.5rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                color: #6b7280 !important;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: white !important;
                color: #111827 !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            
            /* GRADIENT TEXT EFFECT */
            .gradient-text {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
        </style>
        """)

          


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


# Legacy profile functions removed - Replaced by profile_page.py





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
                st.session_state.page = "dashboard"
                st.success("Admin access granted")
                st.rerun()
                return True
            else:
                st.error("Incorrect admin password")
                return False


# ==================== THEME SWITCHER IN SIDEBAR ====================


if __name__ == "__main__":
    main()
