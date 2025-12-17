# utils/ranking.py
def calculate_final_score(skill_match_pct, exp_match_pct):
    """Simple weighted average: 60% skills + 40% experience = final percentage"""
    return round((skill_match_pct * 0.6 + exp_match_pct * 0.4), 1)
