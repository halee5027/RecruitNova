# admin.py
import streamlit as st
from dotenv import load_dotenv
import os

from multiple_screen import multiple_screen
import storage  
from single_screen_admin_old import single_screen_admin

load_dotenv()

def show_admin_panel():
    # sidebar controls
    st.sidebar.title("🔐 Admin Panel")
    page = st.sidebar.radio(
        "Select mode",
        ["Login", "Single Screening", "Bulk Screening", "Statistics"]
    )

    # initialize session flag
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    # always show status at top of admin area
    st.markdown("### Admin Area")
    if st.session_state["admin_logged_in"]:
        st.success("✅ Logged in as Admin")
    else:
        st.warning("🔒 Not logged in")

    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    # ---- LOGIN PAGE ----
    if page == "Login":
        st.subheader("Admin Login")

        pwd = st.text_input("Enter password", type="password")
        if st.button("Login"):
            if pwd == admin_password:
                st.session_state["admin_logged_in"] = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Incorrect password.")

    # ---- SINGLE SCREENING ----
    elif page == "Single Screening":
        if not st.session_state["admin_logged_in"]:
            st.error("Please login first from the Login tab.")
        else:
            single_screen_admin()

    # ---- BULK SCREENING ----
    elif page == "Bulk Screening":
        if not st.session_state["admin_logged_in"]:
            st.error("Please login first from the Login tab.")
        else:
            multiple_screen()

    # ---- STATISTICS ----
    elif page == "Statistics":
        if not st.session_state["admin_logged_in"]:
            st.error("Please login first from the Login tab.")
        else:
            st.subheader("Usage statistics")
            stats = storage.read_stats()
            col1, col2 = st.columns(2)
            col1.metric("Total resumes processed", stats.get("total_processed", 0))
            try:
                reports = [
                    f for f in os.listdir("reports")
                    if f.endswith(".json")
                ]
                col2.metric("Reports generated", len(reports))
            except FileNotFoundError:
                col2.metric("Reports generated", 0)

    # logout button in sidebar (shows only when logged in)
    if st.session_state["admin_logged_in"]:
        if st.sidebar.button("Logout"):
            st.session_state["admin_logged_in"] = False
            st.rerun()

