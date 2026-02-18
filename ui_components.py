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
    """Show premium loading animation"""
    placeholder = st.empty()
    
    with placeholder.container():
        st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <div class='loader' style='
                width: 60px;
                height: 60px;
                border: 6px solid rgba(139, 92, 246, 0.2);
                border-top-color: #8b5cf6;
                border-radius: 50%;
                margin: 0 auto;
                animation: spin 1s linear infinite;
            '></div>
            <p style='margin-top: 20px; color: #64748b; font-size: 14px;'>Loading RecruitNova...</p>
        </div>
        <style>
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
        """, unsafe_allow_html=True)
        time.sleep(1)
    placeholder.empty()

def glassmorphic_card(content: str, icon: str = "", title: str = "", border_color: str = "rgba(139, 92, 246, 0.3)"):
    """Display a glassmorphic card with custom content"""
    st.markdown(f"""
    <div style='
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid {border_color};
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
        transition: all 0.3s ease;
    ' onmouseover='this.style.transform="translateY(-4px)"; this.style.borderColor="rgba(167, 139, 250, 0.5)";' 
       onmouseout='this.style.transform="translateY(0)"; this.style.borderColor="{border_color}";'>
        {f"<div style='font-size: 32px; margin-bottom: 12px;'>{icon}</div>" if icon else ""}
        {f"<h3 style='margin-bottom: 16px; background: linear-gradient(135deg, #a78bfa 0%, #ec4899 50%, #f59e0b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{title}</h3>" if title else ""}
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(title: str, value: str, emoji: str = "", bg_color: str = "#8b5cf6", subtitle: str = ""):
    """Display an enhanced metric card with glassmorphism"""
    st.markdown(f"""
    <div style='
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    ' onmouseover='this.style.transform="translateY(-6px) scale(1.02)"; this.style.borderColor="rgba(167, 139, 250, 0.4)"; this.style.boxShadow="0 12px 40px rgba(139, 92, 246, 0.4)";' 
       onmouseout='this.style.transform="translateY(0) scale(1)"; this.style.borderColor="rgba(139, 92, 246, 0.2)"; this.style.boxShadow="0 8px 32px rgba(0, 0, 0, 0.3)";'>
        <div style='font-size: 40px; margin-bottom: 10px;'>{emoji}</div>
        <div style='font-size: 14px; color: #94a3b8; margin-bottom: 8px; font-weight: 500;'>{title}</div>
        <div style='font-size: 32px; font-weight: 700; background: linear-gradient(135deg, #a78bfa, #ec4899, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px;'>{value}</div>
        {f"<div style='font-size: 12px; color: #64748b;'>{subtitle}</div>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def animated_progress_bar(progress: float, label: str = "", color: str = "#8b5cf6"):
    """Display an animated progress bar"""
    st.markdown(f"""
    <div style='margin: 16px 0;'>
        {f"<p style='color: #f1f5f9; font-size: 14px; margin-bottom: 8px; font-weight: 500;'>{label}</p>" if label else ""}
        <div style='
            background: rgba(30, 41, 59, 0.6);
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            border: 1px solid rgba(139, 92, 246, 0.2);
        '>
            <div style='
                width: {progress}%;
                height: 100%;
                background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 50%, #f59e0b 100%);
                border-radius: 10px;
                transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 0 10px rgba(139, 92, 246, 0.6);
            '></div>
        </div>
        <p style='color: #94a3b8; font-size: 12px; margin-top: 4px; text-align: right;'>{progress}%</p>
    </div>
    """, unsafe_allow_html=True)

def skeleton_loader(height: str = "40px", count: int = 3):
    """Display skeleton loading animation"""
    for i in range(count):
        st.markdown(f"""
        <div style='
            background: linear-gradient(90deg, rgba(30, 41, 59, 0.4) 25%, rgba(45, 55, 72, 0.6) 50%, rgba(30, 41, 59, 0.4) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            height: {height};
            border-radius: 8px;
            margin-bottom: 12px;
        '></div>
        <style>
            @keyframes shimmer {{
                0% {{ background-position: -200% 0; }}
                100% {{ background-position: 200% 0; }}
            }}
        </style>
        """, unsafe_allow_html=True)

def show_notification(message: str, type: str = "info", duration: int = 3):
    """Display a toast-style notification"""
    colors = {
        "success": {"bg": "rgba(16, 185, 129, 0.2)", "border": "#10b981", "icon": "✅"},
        "error": {"bg": "rgba(239, 68, 68, 0.2)", "border": "#ef4444", "icon": "❌"},
        "warning": {"bg": "rgba(245, 158, 11, 0.2)", "border": "#f59e0b", "icon": "⚠️"},
        "info": {"bg": "rgba(59, 130, 246, 0.2)", "border": "#3b82f6", "icon": "ℹ️"}
    }
    
    color_scheme = colors.get(type, colors["info"])
    
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
        <div style='
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 99999;
            background: {color_scheme["bg"]};
            backdrop-filter: blur(10px);
            border-left: 4px solid {color_scheme["border"]};
            padding: 16px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            animation: slideIn 0.3s ease;
        '>
            <span style='font-size: 18px; margin-right: 12px;'>{color_scheme["icon"]}</span>
            <span style='color: #f1f5f9; font-weight: 500;'>{message}</span>
        </div>
        <style>
            @keyframes slideIn {{
                from {{ transform: translateX(400px); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
        </style>
        """, unsafe_allow_html=True)
        time.sleep(duration)
    placeholder.empty()

def stat_boxes():
    """Display stat boxes for admin dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Screened", "0", "📊", "#8b5cf6", "All time")
    with col2:
        metric_card("Strongly Fit", "0", "✅", "#10b981", "Top candidates")
    with col3:
        metric_card("Mid Fit", "0", "⚠️", "#f59e0b", "Good potential")
    with col4:
        metric_card("Low Fit", "0", "❌", "#ef4444", "Need review")

def show_header_with_user():
    """Display header with logo and user name"""
    if "profile_updated" not in st.session_state:
        st.session_state.profile_updated = False
    if "profile_prompted" not in st.session_state:
        st.session_state.profile_prompted = False
    
    # Header removed - using centered title in dashboard instead
    pass
