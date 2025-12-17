# user_extras.py
import streamlit as st
import random
import base64
from pytube import YouTube  # type: ignore
from utils.extract import extract_skills
from utils.extract import SKILLS_DB
from courses import (

    resume_videos,
    interview_videos,
    softskill_links,
   
)



# --------- helper functions copied/simplified from old app ---------

def fetch_yt_title(link: str) -> str:

    """Return YouTube video title for a given URL."""

    try:

        yt = YouTube(link)

        title = yt.title

        thumbnail = yt.thumbnail_url

    except Exception:

        return "YouTube Video"

# -----------------------------------------------------------

# GENERIC COURSES (ADDED)

# -----------------------------------------------------------

def _show_generic_courses():

    st.markdown("### 📘 Starter Courses for Beginners")

    starter = [

        "Introduction to Python – Coursera",

        "Basic Excel for Productivity – Udemy",

        "Foundations of Data – Google",

        "Crash Course on JavaScript – Udemy",

        "Basics of SQL – Khan Academy",

    ]

    for i, c in enumerate(starter, start=1):

        st.markdown(f"{i}. {c}")

# -----------------------------------------------------------

# RESUME TIPS & SCORE

# -----------------------------------------------------------

def show_resume_tips(resume_text: str) -> int:

    if not resume_text:

        st.info("Upload a resume first to get writing tips.")

        return 0

    st.subheader("📝 Resume Tips & Ideas")

    score = 0

    checks = {

        "Objective": "Add a short career objective at the top.",

        "Declaration": "Add a brief declaration at the end.",

        "Hobbies": "Add hobbies.",

        "Interests": "Add interests.",

        "Achievements": "List important achievements.",

        "Projects": "Add academic or personal projects."

    }

    # Section-based scoring

    for section, tip in checks.items():

        if section.lower() in resume_text.lower():

            score += 20

            st.markdown(f"[+] You have added **{section}** section.")

        else:

            st.markdown(f"[-] {tip}")

    # Score bar

    st.subheader("📊 Resume Writing Score")

    bar = st.progress(0)

    for i in range(score):

        bar.progress(i + 1)

    st.success(f"Your resume score: {score} / 100")

    st.warning("This score is only based on section keywords, not content quality.")

    return score

# -----------------------------------------------------------

# COURSE RECOMMENDER (FIXED & IMPROVED)

# -----------------------------------------------------------

def recommend_courses_from_resume(resume_text: str, num_courses: int = 5):

    """
    Recommend courses based on resume skills.
    
    Args:
        resume_text: Text content of the resume
        num_courses: Number of courses to recommend (default 5)
    """

    st.subheader("🎓 Courses & Certifications to Upskill")

    # If empty resume, show generic suggestions

    if not resume_text:

        st.info("Upload a resume to get personalized recommendations.")

        _show_generic_courses()

        return

    # Extract actual skills from resume

    resume_skills = set(extract_skills(resume_text))

    # -----------------------------------

    # 1) ADVANCED COURSES (skills you have)

    # -----------------------------------

    deep_courses = []

    for skill in resume_skills:

        if skill in SKILLS_DB:

            for c in SKILLS_DB[skill].get("courses", []):

                if c not in deep_courses:

                    deep_courses.append(c)

    # Advanced courses

    if deep_courses:

        st.markdown("### 🔥 Advanced Courses Based on Your Skills")

        st.write(f"Skills detected: `{', '.join(sorted(resume_skills))}`")

        max_deep = len(deep_courses)

        n_deep = min(num_courses, max_deep) if max_deep > 0 else 0

        if n_deep > 0:

            for i, c in enumerate(deep_courses[:n_deep], start=1):

                st.markdown(f"{i}. {c}")

        else:

            st.info("No courses available for your skills.")

    else:

        st.info("No mapped advanced courses found for your current skill set.")

    st.markdown("---")

    # -----------------------------------

    # 2) TO-LEARN SKILLS (skills missing)

    # -----------------------------------

    missing_skills = [s for s in SKILLS_DB.keys() if s not in resume_skills]

    to_learn_courses = []

    for skill in missing_skills:

        for c in SKILLS_DB[skill].get("courses", []):

            if c not in to_learn_courses:

                to_learn_courses.append(c)

    # Remove duplicates more aggressively

    to_learn_courses = list(dict.fromkeys(to_learn_courses))

    if to_learn_courses:

        st.markdown("### 🚀 Courses You Can Learn & Add to Resume")

        max_learn = len(to_learn_courses)

        n_learn = min(num_courses, max_learn) if max_learn > 0 else 0

        if n_learn > 0:

            st.info(f"Showing {n_learn} out of {max_learn} available courses.")

            # Create columns for better display (3 columns)

            col1, col2, col3 = st.columns(3)

            for idx, c in enumerate(to_learn_courses[:n_learn]):

                col = [col1, col2, col3][idx % 3]

                with col:

                    st.markdown(f"**{idx + 1}. {c}**")

        else:

            st.info("No courses available.")

    else:

        st.info("All skills covered (unlikely).")

# -----------------------------------------------------------

# BONUS VIDEOS (FIXED)

# -----------------------------------------------------------

def show_bonus_videos():

    st.header("🎥 Bonus: Resume Writing Tips")

    resume_vid = random.choice(resume_videos)

    res_title = fetch_yt_title(resume_vid)

    st.subheader(f"🎬 {res_title}")

    st.video(resume_vid)

    st.header("🎥 Bonus: Interview Tips")

    interview_vid = random.choice(interview_videos)

    int_title = fetch_yt_title(interview_vid)

    st.subheader(f"🎬 {int_title}")

    st.video(interview_vid)

    st.header("🎥 Bonus: Soft Skills Development")

    softskill_vid = random.choice(softskill_links)

    soft_title = fetch_yt_title(softskill_vid)

    st.subheader(f"🎬 {soft_title}")

    st.video(softskill_vid)