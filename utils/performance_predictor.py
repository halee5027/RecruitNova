"""
Premium AI-Powered Performance Prediction Engine
Multi-dimensional candidate assessment with advanced analytics
"""

import re
from typing import Dict, List, Tuple, Any
from datetime import datetime

class PerformancePredictor:
    """Advanced performance prediction with 5-dimensional analysis"""
    
    def __init__(self):
        # Industry-specific skill weights
        self.future_tech_skills = {
            'ai', 'machine learning', 'deep learning', 'nlp', 'computer vision',
            'python', 'tensorflow', 'pytorch', 'kubernetes', 'docker', 'aws', 'azure', 'gcp',
            'react', 'node', 'typescript', 'go', 'rust', 'scala',
            'data science', 'big data', 'spark', 'hadoop',
            'devops', 'ci/cd', 'microservices', 'blockchain'
        }
        
        self.leadership_keywords = {
            'team lead': 25, 'manager': 25, 'director': 30, 'vp': 35, 'cto': 40, 'ceo': 40,
            'head of': 30, 'principal': 25, 'staff engineer': 20,
            'mentored': 15, 'coached': 15, 'trained': 12, 'led': 18,
            'managed team': 20, 'supervised': 15, 'hired': 18, 'recruited': 15,
            'budget': 15, 'p&l': 20, 'strategic': 18, 'roadmap': 15,
            'stakeholder': 12, 'cross-functional': 15, 'executive': 20
        }
        
        self.achievement_keywords = [
            'increased', 'decreased', 'improved', 'optimized', 'reduced',
            'achieved', 'delivered', 'launched', 'built', 'designed',
            'scaled', 'grew', 'saved', 'generated', 'revenue', 'profit'
        ]
        
        self.learning_indicators = {
            'certification': 15, 'certified': 15, 'course': 10, 'training': 10,
            'bootcamp': 15, 'workshop': 8, 'conference': 10, 'self-taught': 18,
            'learned': 8, 'studied': 8, 'upskilled': 12, 'continuous learning': 20
        }
    
    def assess_technical_excellence(self, text: str, skills: List[str]) -> Tuple[float, Dict[str, Any]]:
        """Comprehensive technical skill assessment"""
        score = 30  # Better baseline - everyone has some technical capability
        details = {
            'skill_count': len(skills),
            'future_tech_count': 0,
            'certifications': 0,
            'depth_indicators': []
        }
        
        text_lower = text.lower()
        
        # Base score from skill quantity (max 35)
        if len(skills) > 0:
            score += min(len(skills) * 6, 35)
        
        # Future technology bonus (max 20)
        future_skills_found = [s for s in skills if s.lower() in self.future_tech_skills]
        details['future_tech_count'] = len(future_skills_found)
        if future_skills_found:
            score += min(len(future_skills_found) * 8, 20)
        
        # Certification bonus (max 10)
        cert_count = text_lower.count('certified') + text_lower.count('certification') + text_lower.count('certificate')
        details['certifications'] = cert_count
        score += min(cert_count * 5, 10)
        
        # Depth indicators (max 5)
        depth_keywords = ['expert', 'advanced', 'proficient', 'specialized', 'experienced']
        depth_found = [kw for kw in depth_keywords if kw in text_lower]
        details['depth_indicators'] = depth_found
        score += len(depth_found) * 1
        
        return min(score, 100), details
    
    def assess_professional_experience(self, text: str, years: float) -> Tuple[float, Dict[str, Any]]:
        """Evaluate professional experience quality"""
        score = 25  # Baseline for having a resume
        details = {
            'years': years,
            'senior_role': False,
            'top_company': False,
            'achievements': 0
        }
        
        text_lower = text.lower()
        
        # Years-based score (max 40)
        if years > 0:
            score += min(years * 8, 40)
        else:
            # Even without explicit years, give some credit if resume has work content
            work_keywords = ['worked', 'work', 'experience', 'job', 'position', 'role', 'employed', 'company']
            if any(kw in text_lower for kw in work_keywords):
                score += 15
        
        # Senior role bonus (max 15)
        senior_roles = ['senior', 'lead', 'principal', 'architect', 'director', 'manager', 'head', 'chief']
        if any(role in text_lower for role in senior_roles):
            details['senior_role'] = True
            score += 15
        
        # Top company bonus (max 10)
        top_companies = [
            'google', 'microsoft', 'amazon', 'apple', 'meta', 'netflix',
            'uber', 'airbnb', 'tesla', 'spacex', 'stripe', 'adobe', 'ibm', 'oracle'
        ]
        if any(company in text_lower for company in top_companies):
            details['top_company'] = True
            score += 10
        
        # Achievement metrics (max 10)
        achievement_count = sum(1 for kw in self.achievement_keywords if kw in text_lower)
        details['achievements'] = achievement_count
        if achievement_count > 0:
            score += min(achievement_count * 3, 10)
        
        return min(score, 100), details
    
    def assess_cultural_fit(self, text: str) -> Tuple[float, Dict[str, Any]]:
        """Evaluate cultural and team fit indicators"""
        score = 50  # Base score
        details = {
            'collaboration_score': 0,
            'communication_score': 0,
            'team_size': 'unknown'
        }
        
        text_lower = text.lower()
        
        # Collaboration indicators (max 30)
        collab_keywords = ['team', 'collaborated', 'cooperation', 'partnership', 'cross-functional']
        collab_count = sum(1 for kw in collab_keywords if kw in text_lower)
        collab_score = min(collab_count * 6, 30)
        details['collaboration_score'] = collab_score
        score += collab_score
        
        # Communication indicators (max 20)
        comm_keywords = ['presented', 'communication', 'documented', 'stakeholder', 'client']
        comm_count = sum(1 for kw in comm_keywords if kw in text_lower)
        comm_score = min(comm_count * 4, 20)
        details['communication_score'] = comm_score
        score += comm_score
        
        # Team size indication
        team_match = re.search(r'team of (\d+)', text_lower)
        if team_match:
            team_size = int(team_match.group(1))
            details['team_size'] = f"{team_size} members"
            if team_size >= 5:
                score += 10
        
        return min(score, 100), details
    
    def assess_growth_trajectory(self, text: str) -> Tuple[float, Dict[str, Any]]:
        """Analyze career growth and learning agility"""
        score = 40  # Base score
        details = {
            'promotions': 0,
            'learning_indicators': 0,
            'trajectory': 'Steady'
        }
        
        text_lower = text.lower()
        
        # Promotion indicators (max 35)
        promotion_keywords = ['promoted', 'promotion', 'advanced', 'elevated', 'progression']
        promotion_count = sum(1 for kw in promotion_keywords if kw in text_lower)
        details['promotions'] = promotion_count
        
        if promotion_count >= 2:
            score += 35
            details['trajectory'] = 'Rapid Growth'
        elif promotion_count == 1:
            score += 20
            details['trajectory'] = 'Growing'
        
        # Learning agility (max 25)
        learning_score = 0
        learning_count = 0
        for indicator, points in self.learning_indicators.items():
            if indicator in text_lower:
                learning_score += points
                learning_count += 1
        
        details['learning_indicators'] = learning_count
        score += min(learning_score, 25)
        
        return min(score, 100), details
    
    def assess_leadership_potential(self, text: str) -> Tuple[float, Dict[str, Any]]:
        """Evaluate leadership capabilities and potential"""
        score = 20  # Baseline - everyone has some leadership potential
        details = {
            'leadership_indicators': [],
            'strategic_thinking': False,
            'people_management': False
        }
        
        text_lower = text.lower()
        indicators_found = []
        
        # Leadership keywords scoring (but cap individual contributions)
        for keyword, points in self.leadership_keywords.items():
            if keyword in text_lower:
                score += min(points, 15)  # Cap each keyword contribution
                indicators_found.append(keyword)
        
        details['leadership_indicators'] = indicators_found[:5]  # Top 5
        
        # Strategic thinking bonus
        strategic_keywords = ['strategy', 'strategic', 'vision', 'roadmap', 'planning', 'plan']
        if any(kw in text_lower for kw in strategic_keywords):
            details['strategic_thinking'] = True
            score += 10
        
        # People management
        people_keywords = ['managed team', 'supervised', 'mentored', 'coached', 'hired', 'team', 'manage']
        if any(kw in text_lower for kw in people_keywords):
            details['people_management'] = True
            score += 10
        
        return min(score, 100), details
    
    def assess_risk_factors(self, text: str, years: float) -> Tuple[float, List[str]]:
        """Identify potential risk factors"""
        risk_score = 100  # Start with 100, deduct for risks
        risks = []
        
        text_lower = text.lower()
        
        # Job hopping (frequent changes)
        job_count = len(re.findall(r'\b(company|organization|firm|employer)\b', text_lower))
        if job_count > 0 and years > 0:
            avg_tenure = years / max(job_count, 1)
            if avg_tenure < 1:
                risk_score -= 30
                risks.append("High job turnover rate (< 1 year average)")
            elif avg_tenure < 1.5:
                risk_score -= 15
                risks.append("Moderate job changes")
        
        # Skill gaps
        if len(text) < 500:
            risk_score -= 20
            risks.append("Limited resume content")
        
        # Lack of recent activity
        current_year = datetime.now().year
        if str(current_year) not in text and str(current_year - 1) not in text:
            risk_score -= 10
            risks.append("No recent work mentioned")
        
        return max(risk_score, 0), risks
    
    def generate_recommendations(self, scores: Dict[str, float], details: Dict) -> Dict[str, Any]:
        """Generate AI-powered recommendations"""
        recommendations = {
            'role_fit': [],
            'team_size': '',
            'onboarding_focus': [],
            'strengths': [],
            'development_areas': []
        }
        
        # Role fit based on scores
        if scores['technical'] >= 80 and scores['leadership'] >= 75:
            recommendations['role_fit'] = ['Technical Lead', 'Engineering Manager', 'Principal Engineer']
        elif scores['technical'] >= 75:
            recommendations['role_fit'] = ['Senior Engineer', 'Tech Lead', 'Specialist']
        elif scores['technical'] >= 60:
            recommendations['role_fit'] = ['Mid-level Engineer', 'Individual Contributor']
        else:
            recommendations['role_fit'] = ['Junior Engineer', 'Associate']
        
        # Team size recommendation
        if scores['leadership'] >= 75:
            recommendations['team_size'] = '5-15 members'
        elif scores['leadership'] >= 60:
            recommendations['team_size'] = '3-7 members'
        else:
            recommendations['team_size'] = 'Individual contributor or small team (2-3)'
        
        # Onboarding focus
        if scores['cultural_fit'] < 70:
            recommendations['onboarding_focus'].append('Team integration and collaboration')
        if scores['leadership'] < 60:
            recommendations['onboarding_focus'].append('Leadership development')
        if scores['technical'] < 70:
            recommendations['onboarding_focus'].append('Technical skill enhancement')
        
        # Strengths
        if scores['technical'] >= 75:
            recommendations['strengths'].append('Strong technical capabilities')
        if scores['growth'] >= 75:
            recommendations['strengths'].append('Excellent learning agility')
        if scores['leadership'] >= 75:
            recommendations['strengths'].append('Leadership-ready')
        if scores['cultural_fit'] >= 75:
            recommendations['strengths'].append('Great team player')
        
        # Development areas
        for dimension, score in scores.items():
            if score < 60:
                recommendations['development_areas'].append(f"{dimension.replace('_', ' ').title()}")
        
        return recommendations
    
    def predict_performance(self, resume_text: str, years_experience: float, skills: List[str]) -> Dict[str, Any]:
        """
        Main prediction engine - comprehensive multi-dimensional analysis
        """
        
        # Calculate all dimensions
        tech_score, tech_details = self.assess_technical_excellence(resume_text, skills)
        exp_score, exp_details = self.assess_professional_experience(resume_text, years_experience)
        culture_score, culture_details = self.assess_cultural_fit(resume_text)
        growth_score, growth_details = self.assess_growth_trajectory(resume_text)
        leadership_score, leadership_details = self.assess_leadership_potential(resume_text)
        risk_score, risk_factors = self.assess_risk_factors(resume_text, years_experience)
        
        # Weighted overall score
        weights = {
            'technical': 0.25,
            'experience': 0.20,
            'cultural_fit': 0.15,
            'growth': 0.20,
            'leadership': 0.20
        }
        
        overall_score = (
            tech_score * weights['technical'] +
            exp_score * weights['experience'] +
            culture_score * weights['cultural_fit'] +
            growth_score * weights['growth'] +
            leadership_score * weights['leadership']
        )
        
        # Confidence level
        data_completeness = min(len(resume_text) / 1000, 1.0)  # Based on resume length
        confidence_score = int(data_completeness * 100)
        
        if confidence_score >= 80:
            confidence = "High"
        elif confidence_score >= 60:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        # Generate recommendations
        scores_dict = {
            'technical': tech_score,
            'experience': exp_score,
            'cultural_fit': culture_score,
            'growth': growth_score,
            'leadership': leadership_score
        }
        
        recommendations = self.generate_recommendations(scores_dict, {
            'tech': tech_details,
            'exp': exp_details,
            'culture': culture_details,
            'growth': growth_details,
            'leadership': leadership_details
        })
        
        # Overall rating
        if overall_score >= 85:
            rating = "🌟 Exceptional"
            rating_color = "#10b981"
        elif overall_score >= 75:
            rating = "⭐ Excellent"
            rating_color = "#22c55e"
        elif overall_score >= 65:
            rating = "👍 Good"
            rating_color = "#f59e0b"
        elif overall_score >= 50:
            rating = "👌 Fair"
            rating_color = "#fb923c"
        else:
            rating = "⚠️ Below Average"
            rating_color = "#ef4444"
        
        return {
            'overall_score': round(overall_score, 1),
            'rating': rating,
            'rating_color': rating_color,
            'confidence': confidence,
            'confidence_score': confidence_score,
            'dimension_scores': {
                'technical_excellence': round(tech_score, 1),
                'professional_experience': round(exp_score, 1),
                'cultural_fit': round(culture_score, 1),
                'growth_trajectory': round(growth_score, 1),
                'leadership_potential': round(leadership_score, 1)
            },
            'dimension_details': {
                'technical': tech_details,
                'experience': exp_details,
                'cultural_fit': culture_details,
                'growth': growth_details,
                'leadership': leadership_details
            },
            'risk_assessment': {
                'risk_score': round(risk_score, 1),
                'risk_factors': risk_factors
            },
            'recommendations': recommendations
        }

# Factory function for easy import
def predict_performance(resume_text: str, years_experience: float, skills: List[str]) -> Dict[str, Any]:
    """Predict candidate performance using advanced AI analysis"""
    predictor = PerformancePredictor()
    return predictor.predict_performance(resume_text, years_experience, skills)
