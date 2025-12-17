# utils/resume_screener.py

"""
Resume Screening Module
Automatically analyzes uploaded resumes and compares against job requirements.
Uses existing extract.py, experience.py, ranking.py, and analyzer.py modules.
"""

import sys
import os
from typing import Dict, Optional, Tuple
import json
from datetime import datetime

# Import existing modules
try:
    from utils.extract import extract_text_from_file, extract_skills, match_job_skills
    from utils.experience import estimate_experience_years, experience_percentage, classify_experience_level
    from utils.ranking import calculate_final_score
    from utils.analyzer import analyze_resume
except ImportError as e:
    print(f"Warning: Could not import analysis modules: {e}")


class ResumeScreener:
    """
    Automatically screens resumes against job requirements.
    Calculates match scores, extracts skills, experience, and provides AI analysis.
    """
    
    def __init__(self):
        self.screening_results = {}
    
    @staticmethod
    def screen_resume(
        resume_text: str,
        job_description: str,
        job_title: str = "",
        required_years: int = 3
    ) -> Dict:
        """
        Analyze a resume and score it against job requirements.
        
        Args:
            resume_text: Extracted resume text
            job_description: Job posting description with requirements
            job_title: Job title (for context)
            required_years: Required years of experience for the role
        
        Returns:
            Dictionary with screening results
        """
        
        screening_result = {
            'timestamp': datetime.now().isoformat(),
            'job_title': job_title,
            'success': False,
            'skills': [],
            'experience_years': 0,
            'skill_match_percentage': 0,
            'experience_match_percentage': 0,
            'final_score': 0,
            'experience_level': 'Unknown',
            'matched_skills': [],
            'missing_skills': [],
            'strengths': [],
            'weaknesses': [],
            'recommendation': 'Not Screened',
            'ai_summary': '',
            'details': {}
        }
        
        try:
            if not resume_text or not job_description:
                screening_result['error'] = "Missing resume text or job description"
                return screening_result
            
            # Extract skills from resume
            skills = extract_skills(resume_text)
            screening_result['skills'] = skills
            
            # Estimate experience years
            exp_years = estimate_experience_years(resume_text)
            screening_result['experience_years'] = round(exp_years, 1)
            
            # Calculate skill match
            skill_match = match_job_skills(skills, job_description)
            screening_result['skill_match_percentage'] = round(skill_match, 1)
            
            # Calculate experience match
            exp_match = experience_percentage(exp_years, required_years)
            screening_result['experience_match_percentage'] = round(exp_match, 1)
            
            # Calculate final score
            final_score = calculate_final_score(skill_match, exp_match)
            screening_result['final_score'] = round(final_score, 1)
            
            # Classify experience level
            exp_level = classify_experience_level(exp_years)
            screening_result['experience_level'] = exp_level
            
            # AI Analysis
            ai_result = analyze_resume(resume_text, job_description)
            
            if isinstance(ai_result, dict):
                screening_result['matched_skills'] = ai_result.get('matched_skills', [])
                screening_result['missing_skills'] = ai_result.get('missing_skills', [])
                screening_result['ai_summary'] = ai_result.get('summary', '')
                screening_result['details']['ai_score'] = int(ai_result.get('score', 0))
            
            # Generate strengths and weaknesses
            strengths = []
            weaknesses = []
            
            # Skill-based strengths/weaknesses
            if skill_match >= 80:
                strengths.append("Excellent skill alignment with job requirements")
            elif skill_match >= 60:
                strengths.append("Good match with key job skills")
            elif skill_match >= 40:
                strengths.append("Moderate skill match - some alignment")
            else:
                weaknesses.append("Low skill match - may need training")
            
            # Experience-based strengths/weaknesses
            if exp_match >= 90:
                strengths.append("Perfect experience level for the role")
            elif exp_match >= 70:
                strengths.append("Adequate experience for the position")
            elif exp_years > 0:
                if exp_years < required_years:
                    weaknesses.append(f"Below required {required_years}+ years (Has {exp_years} years)")
                else:
                    strengths.append("Has relevant experience")
            else:
                weaknesses.append("No professional experience found")
            
            # Overall assessment
            if skills:
                strengths.append(f"Found {len(skills)} relevant skills")
            
            screening_result['strengths'] = strengths
            screening_result['weaknesses'] = weaknesses
            
            # Generate recommendation
            screening_result['recommendation'] = ResumeScreener.get_recommendation(
                final_score,
                skill_match,
                exp_match
            )
            
            screening_result['success'] = True
            
        except Exception as e:
            screening_result['error'] = str(e)
            screening_result['success'] = False
        
        return screening_result
    
    @staticmethod
    def get_recommendation(final_score: float, skill_match: float, exp_match: float) -> str:
        """
        Generate hiring recommendation based on scores.
        
        Args:
            final_score: Overall match score (0-100)
            skill_match: Skill match percentage (0-100)
            exp_match: Experience match percentage (0-100)
        
        Returns:
            Recommendation string
        """
        
        if final_score >= 80:
            if skill_match >= 70 and exp_match >= 70:
                return "⭐⭐⭐ STRONG MATCH - Interview Recommended"
            else:
                return "⭐⭐ GOOD MATCH - Consider for Interview"
        
        elif final_score >= 60:
            if skill_match >= 70 or exp_match >= 80:
                return "⭐⭐ GOOD MATCH - Consider for Interview"
            else:
                return "⭐ MODERATE MATCH - Interview Optional"
        
        elif final_score >= 40:
            return "⭐ MODERATE MATCH - Not Recommended"
        
        else:
            return "❌ WEAK MATCH - Not Qualified"
    
    @staticmethod
    def format_screening_for_display(screening_result: Dict) -> Dict:
        """
        Format screening results for UI display.
        
        Args:
            screening_result: Raw screening result dictionary
        
        Returns:
            Formatted result for display
        """
        
        return {
            'status': 'Success' if screening_result.get('success') else 'Failed',
            'job_title': screening_result.get('job_title', 'N/A'),
            'final_score': screening_result.get('final_score', 0),
            'skill_match': screening_result.get('skill_match_percentage', 0),
            'experience_match': screening_result.get('experience_match_percentage', 0),
            'experience_years': screening_result.get('experience_years', 0),
            'experience_level': screening_result.get('experience_level', 'Unknown'),
            'skills_found': screening_result.get('skills', []),
            'matched_skills': screening_result.get('matched_skills', []),
            'missing_skills': screening_result.get('missing_skills', []),
            'strengths': screening_result.get('strengths', []),
            'weaknesses': screening_result.get('weaknesses', []),
            'recommendation': screening_result.get('recommendation', '❌ Not Screened'),
            'ai_summary': screening_result.get('ai_summary', ''),
            'timestamp': screening_result.get('timestamp', '')
        }
    
    @staticmethod
    def compare_candidates(screening_results: list) -> list:
        """
        Sort and rank multiple candidates by final score.
        
        Args:
            screening_results: List of screening result dictionaries
        
        Returns:
            Sorted list of candidates (highest score first)
        """
        
        valid_results = [r for r in screening_results if r.get('success')]
        sorted_results = sorted(
            valid_results,
            key=lambda x: x.get('final_score', 0),
            reverse=True
        )
        
        return sorted_results


# Export for easy import
__all__ = ['ResumeScreener']