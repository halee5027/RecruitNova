# utils/experience.py
import re

def estimate_experience_years(text):
    if not text:
        return 0
    txt = text.lower()
    nums = re.findall(r'(\d+)\s*\+?\s*(?:years|yrs|year)', txt)
    if nums:
        return int(nums[0])
    if 'fresher' in txt or 'no experience' in txt:
        return 0
    if 'senior' in txt or 'lead' in txt or 'manager' in txt:
        return 5
    return 1

def classify_experience_level(years):
    if years <= 0: return 'Fresher'
    if years <= 2: return 'Entry-level'
    if years <= 5: return 'Mid-level'
    return 'Senior'

def experience_percentage(years, job_req_years=3):
    """Experience match percentage (0-100)"""
    if job_req_years == 0:
        return 100
    return min(100, (years / job_req_years) * 100)
