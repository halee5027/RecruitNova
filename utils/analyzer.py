# utils/analyzer.py
# analyzer.py  (or existing analyzer file)

from utils.extract import extract_skills
from utils.experience import estimate_experience_years, experience_percentage
from utils.ranking import calculate_final_score

def analyze_resume(resume_text: str, jd_text: str) -> dict:
    # Use your own logic here – this is just a safe default
    if not resume_text or not jd_text:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "summary": "Job description or resume text is missing.",
            "strengths": [],
            "weaknesses": [],
        }

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = sorted(list(set(resume_skills) & set(jd_skills)))
    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    # skill %, experience %, final combined %
    if jd_skills:
        skill_match_pct = (len(matched) / len(jd_skills)) * 100
    else:
        skill_match_pct = 0

    years = estimate_experience_years(resume_text)
    exp_match_pct = experience_percentage(years, job_req_years=3)
    final_score = int(round(calculate_final_score(skill_match_pct, exp_match_pct)))

    strengths, weaknesses = [], []

    if final_score >= 70:
        strengths.append("Strong overall match with the job description.")
    elif final_score >= 40:
        strengths.append("Moderate match; suitable for further review.")
        weaknesses.append("Some important requirements are only partially met.")
    else:
        weaknesses.append("Low overall match compared to the job description.")

    if matched:
        strengths.append("Matched skills: " + ", ".join(matched[:8]) + (" ..." if len(matched) > 8 else ""))
    else:
        weaknesses.append("No clear overlap between resume skills and JD skills.")

    if missing:
        weaknesses.append("Missing skills from JD: " + ", ".join(missing[:8]) + (" ..." if len(missing) > 8 else ""))
    else:
        strengths.append("All detected JD skills are present in the resume.")

    if years == 0:
        weaknesses.append("No clear experience mentioned.")
    elif years < 3:
        strengths.append(f"Has {years} year(s) of experience, a bit below the 3‑year target.")
    else:
        strengths.append(f"Has {years} year(s) of experience, meets or exceeds the target.")

    summary = (
        f"The resume matches about {final_score}% overall (skills + experience). "
        f"Skill overlap is about {skill_match_pct:.1f}%. "
        f"Detected experience: {years} year(s)."
    )

    return {
        "score": final_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
    }
