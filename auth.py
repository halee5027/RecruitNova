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
        "mode": "user"
    }
    users[email]["admin_password"] = None

    save_users(users)
    return True, "User registered successfully"

def login_user(email, password):
    """Login user"""
    users = load_users()
    
    if email not in users:
        return False, "Email not found"
    
    if users[email]["password"] != hash_password(password):
        return False, "Incorrect password"
    
    return True, "Login successful"

def show_auth_page(mode="signin"):
    """Show authentication page"""

    if mode == "signin":
        st.markdown("<h2 style='text-align: center;'>🔐 Sign In</h2>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # normal login fields
            email = st.text_input("📧 Email", placeholder="your@email.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")

            # ---------- Forgot password block ----------
            forgot = st.checkbox("Forgot password?")
            # make sure these variables always exist
            fp_email = ""
            reset_code = ""
            new_pass = ""
            new_pass2 = ""

            if forgot:
                with st.expander("Reset your password"):
                    fp_email = st.text_input("Registered email", key="fp_email")
                    if st.button("Send reset code", key="fp_send"):
                        if not fp_email:
                            st.error("Enter your email")
                        else:
                            ok, msg = create_reset_code(fp_email)
                            if ok:
                                st.info(f"A reset code has been generated: {msg}")
                            else:
                                st.error(msg)

                    reset_code = st.text_input("Enter reset code", key="fp_code")
                    new_pass = st.text_input("New password", type="password", key="fp_new")
                    new_pass2 = st.text_input("Confirm new password", type="password", key="fp_new2")
                    if st.button("Reset password", key="fp_reset"):
                        if not fp_email:
                            st.error("Enter your email")
                        elif new_pass != new_pass2:
                            st.error("Passwords do not match")
                        else:
                            ok, msg = reset_password_with_code(fp_email, reset_code, new_pass)
                            if ok:
                                st.success(msg)
                            else:
                                st.error(msg)
            # ---------- end forgot password block ----------

            # normal sign‑in + back buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Sign In", use_container_width=True, type="primary", key="signin_submit"):
                    if email and password:
                        success, message = login_user(email, password)
                        if success:
                            st.session_state.user_logged_in = True
                            st.session_state.user_email = email
                            st.session_state.page = "mode_selection"
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("❌ Please fill all fields")

            with col_b:
                if st.button("← Back", use_container_width=True, key="signin_back"):
                    st.session_state.page = "landing"
                    st.rerun()

    
    else:  # signup
        st.markdown("<h2 style='text-align: center;'>📝 Sign Up</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            name = st.text_input("👤 Full Name", placeholder="John Doe")
            email = st.text_input("📧 Email", placeholder="your@email.com")
            phone = st.text_input("📱 Phone", placeholder="+1-800-000-0000")
            password = st.text_input("🔒 Password", type="password", placeholder="Min 6 characters")
            confirm_pass = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Sign Up", use_container_width=True, type="primary"):
                    if not all([name, email, phone, password, confirm_pass]):
                        st.error("❌ Please fill all fields")
                    elif password != confirm_pass:
                        st.error("❌ Passwords don't match")
                    elif len(password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        success, message = register_user(name, email, phone, password)
                        if success:
                            st.session_state.user_logged_in = True
                            st.session_state.user_email = email
                            st.session_state.page = "mode_selection"
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            
            with col_b:
                if st.button("← Back", use_container_width=True):
                    st.session_state.page = "landing"
                    st.rerun()
