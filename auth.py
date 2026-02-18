import streamlit as st
import json
import os
from datetime import datetime
import hashlib
  
RESET_FILE = "data/password_resets.json"
def load_resets():
    if os.path.exists(RESET_FILE):
        with open(RESET_FILE, "r") as f:
            return json.load(f)
    return {}

def save_resets(data):
    with open(RESET_FILE, "w") as f:
        json.dump(data, f, indent=2)
import secrets

def create_reset_code(email):
    users = load_users()
    if email not in users:
        return False, "Email not found"

    resets = load_resets()
    code = secrets.token_hex(3).upper()  # e.g. 'A4F91C'
    resets[email] = {
        "code": code,
        "created_at": datetime.now().isoformat()
    }
    save_resets(resets)
    # IN REAL APP: send via email. For now, show it in UI so you can test.
    return True, code

def reset_password_with_code(email, code, new_password):
    users = load_users()
    resets = load_resets()

    if email not in users:
        return False, "Email not found"

    if email not in resets or resets[email]["code"] != code:
        return False, "Invalid or expired reset code"

    users[email]["password"] = hash_password(new_password)
    save_users(users)

    # Remove used code
    resets.pop(email, None)
    save_resets(resets)

    return True, "Password reset successfully"


USERS_FILE = "data/users.json"
os.makedirs("data", exist_ok=True)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(name, email, phone, password):
    """Register new user"""
    users = load_users()
    
    if email in users:
        return False, "Email already registered"
    
    users[email] = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "mode": "user",
        "profile_complete": False,
        "profile": {}
    }
    users[email]["admin_password"] = None

    save_users(users)
    return True, "User registered successfully"

def get_user_profile(email):
    """Get user profile data with smart completion check"""
    users = load_users()
    if email in users:
        profile = users[email].get("profile", {})
        is_complete = users[email].get("profile_complete", False)
        
        # Smart Check: If flag is False but critical fields exist, treat as complete
        if not is_complete:
            has_role = bool(profile.get("role"))
            has_skills = bool(profile.get("skills"))
            if has_role or has_skills:
                is_complete = True
                
        return profile, is_complete
    return {}, False

def update_profile(email, profile_data):
    """Update user profile"""
    users = load_users()
    if email in users:
        users[email]["profile"] = profile_data
        users[email]["profile_complete"] = True
        save_users(users)
        return True, "Profile updated successfully"
    return False, "User not found"

def login_user(email, password):
    """Login user"""
    users = load_users()
    
    if email not in users:
        return False, "Email not found"
    
    if users[email]["password"] != hash_password(password):
        return False, "Incorrect password"
    
    return True, "Login successful"

def show_auth_page(mode="signin"):
    """Show authentication page with Premium UI"""
    
    # Consistent Background & Layout
    
    # Determine Theme Colors
    theme = st.session_state.get("app_theme", "light")
    
    if theme == "dark":
        bg_gradient = "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)"
        text_color = "white"
        subtitle_color = "#94a3b8"
        input_bg = "rgba(255, 255, 255, 0.05)"
        input_text = "white"
        input_border = "rgba(255, 255, 255, 0.1)"
    else:
        # Light Theme Colors - Professional Blue/Purple
        bg_gradient = "linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)"
        text_color = "#1e293b"
        subtitle_color = "#475569"
        input_bg = "rgba(255, 255, 255, 0.8)"
        input_text = "#0f172a"
        input_border = "rgba(30, 41, 59, 0.1)"

    st.markdown(f"""
        <style>
            /* Global Background (Matches Landing) */
            [data-testid="stAppViewContainer"] {{
                background: {bg_gradient} !important;
            }}
            
            /* Text Auto-Adaptation */
            h2, p, label, .stTextInput label, .stExpander p {{
                color: {text_color} !important;
            }}
            p {{
                color: {subtitle_color} !important;
            }}
            
            /* Compact Spacing */
            .block-container {{ padding-top: 5vh !important; padding-bottom: 2rem !important; }}
            [data-testid="stVerticalBlock"] {{ gap: 0.5rem !important; }}
            
            /* Button Text Visibility - Target Primary Only */
            .stButton button[kind="primary"] p, .stButton button[data-testid="baseButton-primary"] p {{
                color: #ffffff !important;
                font-weight: 600 !important;
            }}
            .stButton button[kind="secondary"] p, .stButton button[data-testid="baseButton-secondary"] p {{
                color: {text_color} !important;
                font-weight: 600 !important;
            }}
            
            /* Forgot Password / Ghost Button Style */
            .stButton button[kind="secondary"] {{
                background-color: transparent !important;
                border: 1px solid {input_border} !important;
            }}
            .stButton button[kind="secondary"]:hover {{
                border-color: #818cf8 !important;
                color: #818cf8 !important;
            }}

            /* Specific Blue Link Style for Forgot Password */
            .element-container:has(#forgot-pass-btn-marker) + .element-container button {{
                border: none !important;
                padding: 0 !important;
                height: auto !important;
            }}
            .element-container:has(#forgot-pass-btn-marker) + .element-container button p {{
                color: #3b82f6 !important;
                text-decoration: underline !important;
                font-size: 0.85rem !important;
            }}
            
            /* Form Input Polish */
            .stTextInput input {{
                background-color: {input_bg} !important;
                color: {input_text} !important;
                border: 1px solid {input_border} !important;
            }}
            .stTextInput input:focus {{
                border-color: #818cf8 !important;
                box-shadow: 0 0 0 1px #818cf8 !important;
            }}
            
            /* Hide Streamlit Stuff */
            footer, header, [data-testid="stHeader"] {{ visibility: hidden; }}
        </style>
    """, unsafe_allow_html=True)
    
    # Grid Layout for Centering
    _, col_center, _ = st.columns([1, 0.8, 1])
    
    with col_center:
        # Glass Card Container
        with st.container():
            if mode == "signin":
                st.markdown("<h2 style='text-align: center; margin-bottom: 0.5rem;'>👋 Welcome Back</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; margin-bottom: 1.5rem;'>Login to your account</p>", unsafe_allow_html=True)

                email = st.text_input("Email", placeholder="name@example.com", key="login_email")
                password = st.text_input("Password", type="password", placeholder="••••••", key="login_pass")

                col_forgot, _ = st.columns([1, 0.1])
                with col_forgot:
                     st.markdown('<span id="forgot-pass-btn-marker"></span>', unsafe_allow_html=True)
                     if st.button("Forgot Password?", key="forgot_btn_top"):
                         st.session_state.show_forgot = not st.session_state.get("show_forgot", False)

                if st.session_state.get("show_forgot", False):
                    with st.expander("Reset Password", expanded=True):
                        fp_email = st.text_input("Email", key="fp_email")
                        if st.button("Send Code", key="fp_send"):
                            ok, msg = create_reset_code(fp_email)
                            if ok: st.info(f"Code: {msg}")
                            else: st.error(msg)
                        
                        rc = st.text_input("Code", key="fp_code")
                        np = st.text_input("New Pass", type="password", key="fp_new")
                        if st.button("Reset", key="fp_reset"):
                             ok, msg = reset_password_with_code(fp_email, rc, np)
                             if ok: st.success(msg)
                             else: st.error(msg)

                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                
                if st.button("🔐 Login", use_container_width=True, type="primary", key="signin_submit"):
                    if email and password:
                        success, message = login_user(email, password)
                        if success:
                            st.session_state.user_logged_in = True
                            st.session_state.user_email = email
                            
                            # Check Profile Completeness
                            _, is_complete = get_user_profile(email)
                            if not is_complete:
                                st.session_state.page = "profile"
                            else:
                                st.session_state.page = "mode_selection"
                            
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Fill fields")

                st.markdown("<div style='text-align: center; margin-top: 2rem; margin-bottom: 0.5rem; font-size: 0.9rem;'><p>New here?</p></div>", unsafe_allow_html=True)
                if st.button("✨ Create Account", use_container_width=True, type="primary", key="goto_signup"):
                    st.session_state.page = "signup"
                    st.rerun()

            else:  # SIGNUP
                st.markdown("<h2 style='text-align: center; margin-bottom: 0.5rem;'>🚀 Create Account</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; margin-bottom: 1.5rem;'>Start your journey</p>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("Name", placeholder="John Doe", key="reg_name")
                with c2:
                    phone = st.text_input("Phone", placeholder="+1234567890", key="reg_phone")
                    
                email = st.text_input("Email", placeholder="name@example.com", key="reg_email")
                
                c3, c4 = st.columns(2)
                with c3:
                    password = st.text_input("Password", type="password", placeholder="6+ chars", key="reg_pass")
                with c4:
                    confirm_pass = st.text_input("Confirm", type="password", placeholder="Re-enter", key="reg_confirm")
                
                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                
                if st.button("✨ Create Account", use_container_width=True, type="primary"):
                    if not all([name, email, phone, password, confirm_pass]):
                        st.error("Fill all fields")
                    elif password != confirm_pass:
                        st.error("Pass mismatch")
                    elif len(password) < 6:
                        st.error("Pass too short")
                    else:
                        success, message = register_user(name, email, phone, password)
                        if success:
                            st.session_state.user_logged_in = True
                            st.session_state.user_email = email
                            
                            # New user always needs profile setup
                            st.session_state.page = "profile"
                            
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                
                st.markdown("<div style='text-align: center; margin-top: 2rem; margin-bottom: 0.5rem; font-size: 0.9rem;'><p>Have an account?</p></div>", unsafe_allow_html=True)
                if st.button("🔐 Login Instead", use_container_width=True, type="primary", key="goto_signin"):
                    st.session_state.page = "signin"
                    st.rerun()
        
    # Back Home (Small, Corner)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Home", key="auth_back_home", type="primary"):
        st.session_state.page = "landing"
        st.rerun()
