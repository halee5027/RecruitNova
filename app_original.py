# app.py
import streamlit as st
from ui import set_page, show_header, local_css
from admin import show_admin_panel
from multiple_screen import multiple_screen
from single_screen_user_old import single_screen_user     # NEW
from admin import show_admin_panel

# -------- CUSTOM UI DESIGN --------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2f3 0%, #dfe9f3 100%);
}

[data-testid="stSidebar"] {
    background-color: #ffffff;
    box-shadow: 2px 0px 12px rgba(0,0,0,0.1);
}

.title-text {
    font-size: 42px;
    font-weight: 900;
    font-family: 'Poppins', sans-serif;
    color: #1a1e23;
    text-align: center;
}

.subtitle-text {
    font-size: 20px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    color: #3a3f45;
    text-align: center;
}

.upload-box {
    border-radius: 18px;
    padding: 40px;
    background: #ffffff;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

set_page()
local_css()

# SIDEBAR NAVIGATION (left)
st.sidebar.markdown("## RecruitNova")
mode = st.sidebar.radio("Choose User", ["User","Admin"])

# Show logo and header
show_header()
st.sidebar.markdown("---")
st.sidebar.markdown("© Developed by team RecruitNova")
st.sidebar.markdown("")

# Main area 
if mode == "User":
    st.markdown("<div style='display:flex; align-items:center; gap:30px;'>"
                "<div style='flex:1'>"
                "<h1 style='font-size:56px; margin-bottom:6px;'>Upload Your Resume</h1>"
                "<p style='color:#9CA3AF;'>Get instant analysis and skill extraction</p>"
                "</div></div>", unsafe_allow_html=True)
    # call the single user screening UI (same as single_screen but non-admin)
    single_screen_user()

else:
    # Admin chosen -> show admin panel (login & submenu)
    show_admin_panel()
