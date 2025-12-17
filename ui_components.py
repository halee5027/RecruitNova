import streamlit as st
import time

def set_page_config():
    """Configure Streamlit page"""
    st.set_page_config(
    page_title="RecruitNova - Intelligent Screening Tool",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
    )
    

def show_loading_animation():
    """Show loading animation"""
    placeholder = st.empty()
    for i in range(3):
        with placeholder.container():
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h3>Loading{}</h3>
            </div>
            """.format("." * (i + 1)), unsafe_allow_html=True)
            time.sleep(0.3)
    placeholder.empty()

def metric_card(title: str, value: str, emoji: str = "", bg_color: str = "#6366f1"):
    """Display a metric card with custom styling"""
    st.markdown(f"""
    <div style='
        background-color: {bg_color}20;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {bg_color};
        text-align: center;
    '>
        <div style='font-size: 28px; margin-bottom: 5px;'>{emoji}</div>
        <div style='font-size: 14px; color: #666; margin-bottom: 5px;'>{title}</div>
        <div style='font-size: 24px; font-weight: bold; color: {bg_color};'>{value}</div>
    </div>
    """, unsafe_allow_html=True)

def stat_boxes():
    """Display stat boxes for admin dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Screened", "0", "📊", "#6366f1")
    with col2:
        metric_card("Strongly Fit", "0", "✅", "#10b981")
    with col3:
        metric_card("Mid Fit", "0", "⚠️", "#f59e0b")
    with col4:
        metric_card("Low Fit", "0", "❌", "#ef4444")

def show_header_with_user():
    """Display header with logo and user name - NO EDIT BUTTON HERE"""
    # Initialize session state for profile update prompt
    if "profile_updated" not in st.session_state:
        st.session_state.profile_updated = False
    if "profile_prompted" not in st.session_state:
        st.session_state.profile_prompted = False
    
    # Create header with logo and user name
    col1, col2 = st.columns([1, 4])
    
    
    
    with col2:
        # Get user name from session state
        user_email = st.session_state.get("user_email", "")  
        user_mode = st.session_state.get("candidate", "")
        user_mode=st.session_state.get("recruiter","")
        
        # Display role badge with user name
        
