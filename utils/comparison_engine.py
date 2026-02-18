"""
Candidate Comparison Engine for RecruitNova
Enables side-by-side comparison of multiple candidates with visual analytics
"""

import pandas as pd
from typing import List, Dict, Any
import plotly.graph_objects as go
from utils.radar_chart import parse_skills_to_dimensions, create_comparison_radar, calculate_dimensions_from_text


def prepare_comparison_data(candidates: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Prepare candidate data for comparison table
    
    Args:
        candidates: List of candidate dictionaries with resume data
        
    Returns:
        DataFrame with comparison metrics
    """
    comparison_data = []
    
    for candidate in candidates:
        comparison_data.append({
            'Name': candidate.get('name', 'Unknown'),
            'ATS Score': candidate.get('ats_score', 0),
            'Match %': candidate.get('match_percentage', 0),
            'Experience': candidate.get('experience', 'N/A'),
            'Skills Count': len(candidate.get('skills', [])),
            'Education': candidate.get('education', 'N/A'),
            'Overall Score': candidate.get('overall_score', 0)
        })
    
    df = pd.DataFrame(comparison_data)
    return df


def create_comparison_metrics_chart(candidates: List[Dict[str, Any]], light_theme: bool = False) -> go.Figure:
    """
    Create bar chart comparing key metrics across candidates
    
    Args:
        candidates: List of candidate dictionaries
        light_theme: If True, use light theme for PDF export
        
    Returns:
        Plotly Figure object
    """
    names = [c.get('name', f"Candidate {i+1}") for i, c in enumerate(candidates)]
    ats_scores = [c.get('ats_score', 0) for c in candidates]
    match_percentages = [c.get('match_percentage', 0) for c in candidates]
    overall_scores = [c.get('overall_score', 0) for c in candidates]
    
    # Set colors based on theme
    if light_theme:
        text_color = 'black'
        bg_color = 'white'
        grid_color = 'rgba(0,0,0,0.1)'
    else:
        text_color = 'white'
        bg_color = 'rgba(0,0,0,0)'
        grid_color = 'rgba(255,255,255,0.1)'
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='ATS Score',
        x=names,
        y=ats_scores,
        marker_color='#4f46e5',
        text=ats_scores,
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='Match %',
        x=names,
        y=match_percentages,
        marker_color='#06b6d4',
        text=match_percentages,
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='Overall Score',
        x=names,
        y=overall_scores,
        marker_color='#10b981',
        text=overall_scores,
        textposition='auto',
    ))
    
    fig.update_layout(
        title=dict(
            text='Candidate Metrics Comparison',
            font=dict(color=text_color)
        ),
        xaxis=dict(
            title=dict(text='Candidates', font=dict(color=text_color)),
            tickfont=dict(color=text_color),
            gridcolor=grid_color
        ),
        yaxis=dict(
            title=dict(text='Score', font=dict(color=text_color)),
            tickfont=dict(color=text_color),
            gridcolor=grid_color
        ),
        barmode='group',
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=text_color)
        )
    )
    
    return fig


def get_comparison_insights(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate insights from candidate comparison
    
    Args:
        candidates: List of candidate dictionaries
        
    Returns:
        Dictionary with insights
    """
    if not candidates:
        return {}
    
    # Find top candidate by overall score
    top_candidate = max(candidates, key=lambda x: x.get('overall_score', 0))
    
    # Find candidate with most skills
    most_skilled = max(candidates, key=lambda x: len(x.get('skills', [])))
    
    # Find candidate with highest ATS score
    best_ats = max(candidates, key=lambda x: x.get('ats_score', 0))
    
    # Calculate averages
    avg_ats = sum(c.get('ats_score', 0) for c in candidates) / len(candidates)
    avg_match = sum(c.get('match_percentage', 0) for c in candidates) / len(candidates)
    
    return {
        'top_candidate': top_candidate.get('name', 'Unknown'),
        'top_score': top_candidate.get('overall_score', 0),
        'most_skilled': most_skilled.get('name', 'Unknown'),
        'skill_count': len(most_skilled.get('skills', [])),
        'best_ats': best_ats.get('name', 'Unknown'),
        'best_ats_score': best_ats.get('ats_score', 0),
        'avg_ats': round(avg_ats, 1),
        'avg_match': round(avg_match, 1),
        'total_candidates': len(candidates)
    }


def create_skills_comparison_radar(candidates: List[Dict[str, Any]], light_theme: bool = False) -> go.Figure:
    """
    Create overlaid radar chart comparing skills across candidates
    
    Args:
        candidates: List of candidate dictionaries with skills
        light_theme: If True, use light theme for PDF export
        
    Returns:
        Plotly Figure object
    """
    candidates_data = []
    
    for candidate in candidates[:5]:  # Max 5 candidates for readability
        name = candidate.get('name', 'Unknown')
        resume_text = candidate.get('resume_text', '')
        skills = candidate.get('skills', [])
        
        # Prioritize full text scanning
        if resume_text:
            dimensions = calculate_dimensions_from_text(resume_text)
        elif skills:
            skills_text = ', '.join(skills)
            dimensions = parse_skills_to_dimensions(skills_text)
        else:
            dimensions = {}
            
        candidates_data.append((name, dimensions))
    
    return create_comparison_radar(candidates_data, title="Skills Comparison", light_theme=light_theme)
