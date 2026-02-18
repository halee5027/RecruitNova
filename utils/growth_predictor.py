"""
Future Growth Predictor
Analyzes candidate resumes to predict career growth potential and trajectory
"""

import re
from typing import Dict, List, Tuple, Any
from datetime import datetime


class GrowthPredictor:
    """Predicts candidate future growth potential based on resume analysis"""
    
    def __init__(self):
        # Modern/Future tech keywords
        self.modern_tech = [
            'ai', 'machine learning', 'deep learning', 'kubernetes', 'docker',
            'react', 'vue', 'next.js', 'typescript', 'graphql', 'microservices',
            'cloud', 'aws', 'azure', 'gcp', 'terraform', 'ci/cd', 'devops',
            'python 3', 'rust', 'go', 'blockchain', 'web3'
        ]
        
        # Learning indicators
        self.learning_keywords = [
            'certification', 'certified', 'course', 'training', 'workshop',
            'bootcamp', 'udemy', 'coursera', 'pluralsight', 'learning',
            'studied', 'mastered', 'acquired', 'upskilled'
        ]
        
        # Top tier companies
        self.top_companies = [
            'google', 'microsoft', 'amazon', 'meta', 'facebook', 'apple',
            'netflix', 'tesla', 'nvidia', 'openai', 'anthropic', 'databricks'
        ]
        
        # Leadership evolution keywords
        self.leadership_levels = {
            'entry': ['team member', 'developer', 'engineer', 'analyst'],
            'intermediate': ['senior', 'lead', 'principal'],
            'advanced': ['manager', 'director', 'head of', 'vp', 'cto', 'ceo']
        }
    
    def analyze_learning_velocity(self, text: str, skills: List[str]) -> Tuple[float, Dict]:
        """Analyze how fast the candidate learns and adapts"""
        score = 40  # Base score
        details = {}
        
        text_lower = text.lower()
        
        # Modern tech adoption
        modern_count = sum(1 for tech in self.modern_tech if tech in text_lower)
        score += min(modern_count * 5, 25)
        details['modern_tech_count'] = modern_count
        
        # Learning activities
        learning_count = sum(1 for keyword in self.learning_keywords if keyword in text_lower)
        score += min(learning_count * 4, 20)
        details['learning_activities'] = learning_count
        
        # Certifications
        cert_match = len(re.findall(r'certifi(ed|cation)', text_lower))
        score += min(cert_match * 5, 15)
        details['certifications'] = cert_match
        
        return min(score, 100), details
    
    def analyze_career_trajectory(self, text: str, years: float) -> Tuple[float, Dict]:
        """Analyze career progression patterns"""
        score = 30  # Base score
        details = {}
        
        text_lower = text.lower()
        
        # Job transitions (more roles = more growth experience)
        job_keywords = ['company', 'worked at', 'position', 'role']
        job_count = sum(text_lower.count(kw) for kw in job_keywords)
        transitions = min(job_count, 6)
        score += transitions * 5
        details['job_transitions'] = transitions
        
        # Promotion indicators
        promotion_keywords = ['promoted', 'advanced', 'progressed', 'elevated']
        promotions = sum(1 for kw in promotion_keywords if kw in text_lower)
        score += min(promotions * 10, 20)
        details['promotions'] = promotions
        
        # Top company experience
        top_company_exp = any(company in text_lower for company in self.top_companies)
        if top_company_exp:
            score += 15
        details['top_company'] = top_company_exp
        
        # Years-based progression (faster growth = higher score)
        if years > 0:
            yearly_growth = (transitions + promotions) / years
            score += min(yearly_growth * 10, 25)
        
        details['years_experience'] = years
        
        return min(score, 100), details
    
    
    def analyze_adaptability(self, text: str, skills: List[str]) -> Tuple[float, Dict]:
        """Analyze ability to adapt and switch contexts"""
        score = 35  # Base score
        details = {}
        
        text_lower = text.lower()
        
        # Diverse skill set (indicates flexibility)
        skill_diversity = len(set(skills))
        score += min(skill_diversity * 3, 30)
        details['skill_diversity'] = skill_diversity
        
        # Technology stack breadth
        tech_stacks = {
            'backend': ['python', 'java', 'node', 'go', 'ruby', '.net', 'php'],
            'frontend': ['react', 'angular', 'vue', 'svelte', 'javascript', 'typescript'],
            'mobile': ['ios', 'android', 'react native', 'flutter', 'swift', 'kotlin'],
            'data': ['sql', 'nosql', 'mongodb', 'postgresql', 'bigquery', 'spark'],
            'cloud': ['aws', 'azure', 'gcp', 'kubernetes', 'docker']
        }
        
        categories_covered = sum(1 for stack, techs in tech_stacks.items() 
                                if any(tech in text_lower for tech in techs))
        score += categories_covered * 7
        details['tech_stack_breadth'] = categories_covered
        
        # Industry/domain switches
        domains = ['fintech', 'healthcare', 'ecommerce', 'saas', 'gaming', 'finance', 'retail']
        domain_count = sum(1 for domain in domains if domain in text_lower)
        score += min(domain_count * 5, 15)
        details['domain_experience'] = domain_count
        
        return min(score, 100), details
    
    def analyze_leadership_evolution(self, text: str) -> Tuple[float, Dict]:
        """Analyze growth in leadership capabilities"""
        score = 25  # Base score
        details = {}
        
        text_lower = text.lower()
        
        # Track leadership level progression
        has_entry = any(kw in text_lower for kw in self.leadership_levels['entry'])
        has_intermediate = any(kw in text_lower for kw in self.leadership_levels['intermediate'])
        has_advanced = any(kw in text_lower for kw in self.leadership_levels['advanced'])
        
        # Progression scoring
        if has_advanced:
            score += 40
            details['leadership_level'] = 'Advanced'
        elif has_intermediate:
            score += 25
            details['leadership_level'] = 'Intermediate'
        elif has_entry:
            score += 10
            details['leadership_level'] = 'Entry'
        else:
            details['leadership_level'] = 'Not Indicated'
        
        # Team management
        team_patterns = [
            r'(\d+)\s*(?:member|person|people)?\s*team',
            r'team\s*of\s*(\d+)',
            r'led\s*(\d+)',
            r'managed\s*(\d+)'
        ]
        
        max_team_size = 0
        for pattern in team_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                sizes = [int(m) for m in matches]
                max_team_size = max(max_team_size, max(sizes))
        
        if max_team_size > 0:
            score += min(max_team_size * 2, 25)
        details['max_team_size'] = max_team_size
        
        # Mentorship
        mentorship_keywords = ['mentor', 'coach', 'train', 'guide', 'develop team']
        mentorship_count = sum(1 for kw in mentorship_keywords if kw in text_lower)
        if mentorship_count > 0:
            score += 10
        details['mentorship'] = mentorship_count > 0
        
        return min(score, 100), details
    
    def analyze_impact_magnitude(self, text: str) -> Tuple[float, Dict]:
        """Analyze scale and impact of achievements"""
        score = 30  # Base score
        details = {}
        
        text_lower = text.lower()
        
        # Quantified achievements with large numbers
        impact_patterns = [
            r'(\d+)%\s*(?:improvement|increase|growth|faster)',
            r'(\d+)[kmb]?\+?\s*(?:users|customers|requests|transactions)',
            r'\$(\d+)[kmb]?\s*(?:revenue|savings|value)',
            r'(\d+)x\s*(?:faster|improvement|growth)'
        ]
        
        high_impact_count = 0
        for pattern in impact_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                # Check if numbers are significant
                for match in matches:
                    try:
                        num = float(match.replace('k', '000').replace('m', '000000').replace('b', '000000000'))
                        if num >= 100:  # Significant impact
                            high_impact_count += 1
                    except:
                        pass
        
        score += min(high_impact_count * 12, 40)
        details['quantified_achievements'] = high_impact_count
        
        # Innovation indicators
        innovation_keywords = [
            'built from scratch', 'architected', 'designed',
            'innovative', 'pioneered', 'launched', 'shipped',
            'patent', 'publication', 'open source'
        ]
        innovation_count = sum(1 for kw in innovation_keywords if kw in text_lower)
        score += min(innovation_count * 5, 20)
        details['innovation_indicators'] = innovation_count
        
        # Scale keywords
        scale_keywords = ['scale', 'scalable', 'distributed', 'millions', 'global', 'enterprise']
        scale_count = sum(1 for kw in scale_keywords if kw in text_lower)
        score += min(scale_count * 3, 10)
        details['scale_indicators'] = scale_count
        
        return min(score, 100), details
    
    def calculate_overall_growth_score(self, dimension_scores: Dict[str, float]) -> float:
        """Calculate weighted overall growth score"""
        weights = {
            'learning_velocity': 0.25,
            'career_trajectory': 0.25,
            'adaptability': 0.20,
            'leadership_evolution': 0.15,
            'impact_magnitude': 0.15
        }
        
        total = sum(dimension_scores[dim] * weights[dim] for dim in weights)
        return round(total, 1)
    
    def calculate_time_to_next_level(self, overall_score: float, career_details: Dict) -> str:
        """Estimate time to next career advancement"""
        years = career_details.get('years_experience', 0)
        transitions = career_details.get('job_transitions', 0)
        
        # Base calculation on score and current pace
        if overall_score >= 85:
            return "3-6 months"
        elif overall_score >= 75:
            return "6-12 months"
        elif overall_score >= 65:
            return "12-18 months"
        elif overall_score >= 50:
            return "18-24 months"
        else:
            return "24+ months"
    
    def identify_growth_blockers(self, dimension_scores: Dict[str, float], details: Dict) -> List[str]:
        """Identify potential obstacles to growth"""
        blockers = []
        
        if dimension_scores['learning_velocity'] < 60:
            blockers.append("Limited recent learning activity - consider pursuing certifications")
        
        if dimension_scores['career_trajectory'] < 60:
            blockers.append("Slow career progression - may need role change or increased visibility")
        
        if dimension_scores['adaptability'] < 60:
            blockers.append("Narrow skill set - expanding technical breadth recommended")
        
        if dimension_scores['leadership_evolution'] < 50:
            blockers.append("Limited leadership experience - seek mentorship or team lead opportunities")
        
        if dimension_scores['impact_magnitude'] < 55:
            blockers.append("Few quantified achievements - focus on measuring and documenting impact")
        
        return blockers if blockers else ["No significant blockers identified"]
    
    def generate_recommendations(self, dimension_scores: Dict[str, float], details: Dict) -> Dict[str, Any]:
        """Generate actionable growth recommendations"""
        recs = {}
        
        # Optimal roles based on strengths
        if dimension_scores['leadership_evolution'] >= 75 and dimension_scores['impact_magnitude'] >= 70:
            recs['optimal_roles'] = ["Engineering Manager", "Director of Engineering", "VP Engineering"]
        elif dimension_scores['learning_velocity'] >= 80 and dimension_scores['adaptability'] >= 75:
            recs['optimal_roles'] = ["Principal Engineer", "Staff Engineer", "Tech Lead"]
        elif dimension_scores['impact_magnitude'] >= 75:
            recs['optimal_roles'] = ["Senior Engineer", "Lead Engineer", "Architect"]
        else:
            recs['optimal_roles'] = ["Mid-level Engineer", "Senior Engineer", "Specialist"]
        
        # Growth accelerators (top 3 actions)
        actions = []
        
        if dimension_scores['learning_velocity'] < 75:
            actions.append("Pursue advanced certifications in modern technologies")
       
        if dimension_scores['leadership_evolution'] < 70:
            actions.append("Take on team lead or mentorship responsibilities")
        
        if dimension_scores['impact_magnitude'] < 70:
            actions.append("Focus on high-impact projects with measurable outcomes")
        
        if dimension_scores['adaptability'] < 70:
            actions.append("Learn complementary skills outside current tech stack")
        
        if not actions:
            actions = [
                "Maintain current growth trajectory",
                "Seek leadership opportunities at next level",
                "Build thought leadership through writing/speaking"
            ]
        
        recs['recommended_actions'] = actions[:3]
        
        # Success probability
        overall = self.calculate_overall_growth_score(dimension_scores)
        if overall >= 80:
            recs['success_probability'] = "Very High (85-95%)"
        elif overall >= 70:
            recs['success_probability'] = "High (75-85%)"
        elif overall >= 60:
            recs['success_probability'] = "Moderate (60-75%)"
        else:
            recs['success_probability'] = "Developing (40-60%)"
        
        return recs


def predict_growth(resume_text: str, years_exp: float, skills: List[str]) -> Dict[str, Any]:
    """
    Main function to predict candidate growth potential
    
    Args:
        resume_text: Full resume text
        years_exp: Years of experience
        skills: List of extracted skills
    
    Returns:
        Dictionary with growth predictions and recommendations
    """
    predictor = GrowthPredictor()
    
    # Analyze all dimensions
    learning_score, learning_details = predictor.analyze_learning_velocity(resume_text, skills)
    career_score, career_details = predictor.analyze_career_trajectory(resume_text, years_exp)
    adapt_score, adapt_details = predictor.analyze_adaptability(resume_text, skills)
    leadership_score, leadership_details = predictor.analyze_leadership_evolution(resume_text)
    impact_score, impact_details = predictor.analyze_impact_magnitude(resume_text)
    
    dimension_scores = {
        'learning_velocity': learning_score,
        'career_trajectory': career_score,
        'adaptability': adapt_score,
        'leadership_evolution': leadership_score,
        'impact_magnitude': impact_score
    }
    
    # Calculate overall score
    overall_score = predictor.calculate_overall_growth_score(dimension_scores)
    
    # Determine rating
    if overall_score >= 85:
        rating = "🚀 Exponential Growth"
        rating_color = "#10b981"
    elif overall_score >= 75:
        rating = "📈 High Growth Potential"
        rating_color = "#22c55e"
    elif overall_score >= 65:
        rating = "📊 Moderate Growth"
        rating_color = "#f59e0b"
    elif overall_score >= 50:
        rating = "📉 Steady Progress"
        rating_color = "#fb923c"
    else:
        rating = "⚠️ Limited Growth Indicators"
        rating_color = "#ef4444"
    
    # Generate output
    return {
        'overall_score': overall_score,
        'rating': rating,
        'rating_color': rating_color,
        'dimension_scores': dimension_scores,
        'dimension_details': {
            'learning': learning_details,
            'career': career_details,
            'adaptability': adapt_details,
            'leadership': leadership_details,
            'impact': impact_details
        },
        'time_to_next_level': predictor.calculate_time_to_next_level(overall_score, career_details),
        'growth_blockers': predictor.identify_growth_blockers(dimension_scores, {}),
        'recommendations': predictor.generate_recommendations(dimension_scores, {})
    }
