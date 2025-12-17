# ui.py
import streamlit as st
from PIL import Image
import os

def set_page():
    st.set_page_config(page_title="RecruitNova", page_icon="🚀", layout='wide')

def show_header():
 col1, col2,col3 = st.columns([1, 10 ,1])
 col2.image("/Users/akmalhaleema/Pictures/Photos Library.photoslibrary/resources/derivatives/masters/D/D2ADD07D-A3E4-4661-A555-3DD8CFB43F48_4_5005_c.jpeg", width=1200)
 # you place logo here


# small CSS to improve look
def local_css():
    st.markdown("""
    <style>
    /* sidebar background */
    .sidebar .sidebar-content {
        background:linear-gradient(90deg,#3b82f6,#7c3aed);
        color: white;
    }
    /* big main title */
    .stTitle h1 {
        font-size: 44px;
    }
    /* center align the logo area */
    .reportview-container .main section {
        padding-top: 1rem;

    }
    /* custom buttons */
    .stButton>button {
        background: linear-gradient(90deg,#3b82f6,#7c3aed);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
