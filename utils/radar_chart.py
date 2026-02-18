"""
Skill Radar Chart Generator for RecruitNova
Creates interactive radar/polar charts for visualizing candidate skills across multiple dimensions
"""

import plotly.graph_objects as go
import re
from typing import Dict, List, Tuple


def parse_skills_to_dimensions(skills_text: str) -> Dict[str, int]:
    """
    Parse skills text and categorize into dimensions with scores
    
    Args:
        skills_text: Comma-separated skills string
        
    Returns:
        Dictionary mapping dimension names to scores (0-100)
    """
    if not skills_text:
        return {}
    
    # Skill categories mapping - EXPANDED for better detection
    technical_keywords = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 
                         'kubernetes', 'git', 'api', 'database', 'cloud', 'machine learning', 
                         'data science', 'ai', 'ml', 'tensorflow', 'pytorch', 'html', 'css',
                         'angular', 'vue', 'django', 'flask', 'spring', 'mongodb', 'postgresql',
                         'redis', 'kafka', 'microservices', 'devops', 'ci/cd', 'jenkins', 'terraform',
                         'linux', 'bash', 'powershell', 'azure', 'gcp', 'serverless', 'graphql',
                         'rest', 'soap', 'json', 'xml', 'c++', 'c#', 'ruby', 'php', 'go', 'rust',
                         'swift', 'kotlin', 'scala', 'r', 'matlab', 'tableau', 'power bi', 'excel',
                         'spark', 'hadoop', 'etl', 'data', 'analytics', 'visualization', 'testing',
                         'selenium', 'junit', 'pytest', 'automation', 'qa', 'security', 'networking']
    
    communication_keywords = ['communication', 'presentation', 'writing', 'public speaking', 
                             'storytelling', 'documentation', 'collaboration', 'interpersonal',
                             'verbal', 'written', 'listening', 'negotiation', 'persuasion',
                             'articulation', 'clarity', 'concise', 'effective communication']
    
    leadership_keywords = ['leadership', 'management', 'team lead', 'mentoring', 'coaching', 
                          'project management', 'agile', 'scrum', 'kanban', 'strategic',
                          'decision making', 'delegation', 'motivation', 'conflict resolution',
                          'people management', 'stakeholder management', 'vision', 'planning']
    
    problem_solving_keywords = ['problem solving', 'analytical', 'critical thinking', 'debugging', 
                               'troubleshooting', 'optimization', 'algorithm', 'logic', 'reasoning',
                               'creative', 'innovative', 'solution', 'analysis', 'research',
                               'investigation', 'root cause', 'systematic']
    
    domain_keywords = ['finance', 'healthcare', 'e-commerce', 'marketing', 'sales', 'hr', 
                      'education', 'retail', 'manufacturing', 'banking', 'insurance', 'telecom',
                      'logistics', 'supply chain', 'consulting', 'legal', 'real estate',
                      'automotive', 'aerospace', 'energy', 'media', 'entertainment', 'gaming',
                      'fintech', 'healthtech', 'edtech', 'saas', 'b2b', 'b2c', 'enterprise']
    
    adaptability_keywords = ['adaptable', 'flexible', 'learning', 'quick learner', 'versatile', 
                            'multi-tasking', 'fast-paced', 'agile', 'dynamic', 'change management',
                            'resilient', 'growth mindset', 'continuous improvement', 'self-starter',
                            'proactive', 'initiative', 'resourceful']
    
    # Parse skills
    skills_list = [s.strip().lower() for s in skills_text.split(',')]
    
    # Count matches in each category
    dimensions = {
        'Technical Skills': 0,
        'Communication': 0,
        'Leadership': 0,
        'Problem Solving': 0,
        'Domain Knowledge': 0,
        'Adaptability': 0
    }
    
    for skill in skills_list:
        if any(kw in skill for kw in technical_keywords):
            dimensions['Technical Skills'] += 1
        if any(kw in skill for kw in communication_keywords):
            dimensions['Communication'] += 1
        if any(kw in skill for kw in leadership_keywords):
            dimensions['Leadership'] += 1
        if any(kw in skill for kw in problem_solving_keywords):
            dimensions['Problem Solving'] += 1
        if any(kw in skill for kw in domain_keywords):
            dimensions['Domain Knowledge'] += 1
        if any(kw in skill for kw in adaptability_keywords):
            dimensions['Adaptability'] += 1
    
    # Normalize to 0-100 scale (cap at 10 skills per dimension = 100%)
    max_skills_per_dimension = 10
    for key in dimensions:
        dimensions[key] = min(100, (dimensions[key] / max_skills_per_dimension) * 100)
    
    # If no matches, distribute evenly based on total skill count
    if sum(dimensions.values()) == 0 and len(skills_list) > 0:
        base_score = min(100, (len(skills_list) / 6) * 100)
        for key in dimensions:
            dimensions[key] = base_score
    
    return dimensions


def calculate_dimensions_from_text(resume_text: str) -> Dict[str, int]:
    """
    Calculate dimension scores by scanning full resume text for keywords
    
    Args:
        resume_text: Full text content of the resume
        
    Returns:
        Dictionary mapping dimension names to scores (0-100)
    """
    if not resume_text:
        return {}
        
    text_lower = resume_text.lower()
    
    # Define keywords (reuse lists defined in parse_skills_to_dimensions conceptually)
    # Ideally should share these lists, but for now redefining for clarity/isolation
    # or refactoring to shared constant is better.
    # Let's extract lists to module level constants effectively by copying them here
    # to avoid major refactoring risk.
    
    technical_keywords = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 
                         'kubernetes', 'git', 'api', 'database', 'cloud', 'machine learning', 
                         'data science', 'ai', 'ml', 'tensorflow', 'pytorch', 'html', 'css',
                         'angular', 'vue', 'django', 'flask', 'spring', 'mongodb', 'postgresql',
                         'redis', 'kafka', 'microservices', 'devops', 'ci/cd', 'jenkins', 'terraform',
                         'linux', 'bash', 'powershell', 'azure', 'gcp', 'serverless', 'graphql',
                         'rest', 'soap', 'json', 'xml', 'c++', 'c#', 'ruby', 'php', 'go', 'rust',
                         'swift', 'kotlin', 'scala', 'r', 'matlab', 'tableau', 'power bi', 'excel',
                         'spark', 'hadoop', 'etl', 'data', 'analytics', 'visualization', 'testing',
                         'selenium', 'junit', 'pytest', 'automation', 'qa', 'security', 'networking']
    
    communication_keywords = ['communication', 'presentation', 'writing', 'public speaking', 
                             'storytelling', 'documentation', 'collaboration', 'interpersonal',
                             'verbal', 'written', 'listening', 'negotiation', 'persuasion',
                             'articulation', 'clarity', 'concise', 'effective communication']
    
    leadership_keywords = ['leadership', 'management', 'team lead', 'mentoring', 'coaching', 
                          'project management', 'agile', 'scrum', 'kanban', 'strategic',
                          'decision making', 'delegation', 'motivation', 'conflict resolution',
                          'people management', 'stakeholder management', 'vision', 'planning']
    
    problem_solving_keywords = ['problem solving', 'analytical', 'critical thinking', 'debugging', 
                               'troubleshooting', 'optimization', 'algorithm', 'logic', 'reasoning',
                               'creative', 'innovative', 'solution', 'analysis', 'research',
                               'investigation', 'root cause', 'systematic']
    
    domain_keywords = ['finance', 'healthcare', 'e-commerce', 'marketing', 'sales', 'hr', 
                      'education', 'retail', 'manufacturing', 'banking', 'insurance', 'telecom',
                      'logistics', 'supply chain', 'consulting', 'legal', 'real estate',
                      'automotive', 'aerospace', 'energy', 'media', 'entertainment', 'gaming',
                      'fintech', 'healthtech', 'edtech', 'saas', 'b2b', 'b2c', 'enterprise']
    
    adaptability_keywords = ['adaptable', 'flexible', 'learning', 'quick learner', 'versatile', 
                            'multi-tasking', 'fast-paced', 'agile', 'dynamic', 'change management',
                            'resilient', 'growth mindset', 'continuous improvement', 'self-starter',
                            'proactive', 'initiative', 'resourceful', 'adaptability', 'flexibility',
                            'willing to learn', 'eager to learn', 'pressure', 'deadlines', 
                            'shifting priorities', 'new technologies', 'independent', 'ownership']

    dimensions = {
        'Technical Skills': 0,
        'Communication': 0,
        'Leadership': 0,
        'Problem Solving': 0,
        'Domain Knowledge': 0,
        'Adaptability': 0
    }
    
    # Count UNIQUE keyword matches in the text
    # Technical: expect more keywords (e.g. 15 for 100%) because tech stacks are large
    # Soft skills: expect fewer (e.g. 5 for 100%)
    
    for kw in technical_keywords:
        if kw in text_lower:
            dimensions['Technical Skills'] += 1
            
    for kw in communication_keywords:
        if kw in text_lower:
            dimensions['Communication'] += 1
            
    for kw in leadership_keywords:
        if kw in text_lower:
            dimensions['Leadership'] += 1
            
    for kw in problem_solving_keywords:
        if kw in text_lower:
            dimensions['Problem Solving'] += 1
            
    for kw in domain_keywords:
        if kw in text_lower:
            dimensions['Domain Knowledge'] += 1
            
    for kw in adaptability_keywords:
        if kw in text_lower:
            dimensions['Adaptability'] += 1
            
    # Normalize scores
    # Logic: 
    # Technical: 15 keywords = 100%
    # Others: 5 keywords = 100%
    
    thresholds = {
        'Technical Skills': 15,
        'Communication': 5,
        'Leadership': 5,
        'Problem Solving': 5,
        'Domain Knowledge': 3,
        'Adaptability': 4
    }
    
    for key in dimensions:
        score = (dimensions[key] / thresholds.get(key, 5)) * 100
        dimensions[key] = min(100, int(score))
        
        # Ensure non-zero if we have at least one match, or give a tiny boost for "Technical" purely based on length?
        # No, keyword matching is cleaner.
        
    return dimensions


def create_radar_chart(
    dimensions: Dict[str, int],
    title: str = "Skill Profile",
    color: str = "#4f46e5",
    show_benchmark: bool = False,
    light_theme: bool = False
) -> go.Figure:
    """
    Create an interactive radar chart for skill visualization
    
    Args:
        dimensions: Dictionary of dimension names to scores (0-100)
        title: Chart title
        color: Primary color for the chart
        show_benchmark: Whether to show industry benchmark overlay
        light_theme: If True, use light theme for PDF export (dark text, white bg)
        
    Returns:
        Plotly Figure object
    """
    if not dimensions:
        # Return empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No skill data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        return fig
    
    categories = list(dimensions.keys())
    values = list(dimensions.values())
    
    # Close the radar chart by appending first value
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    # Set colors based on theme
    if light_theme:
        text_color = 'black'
        bg_color = 'white'
        grid_color = 'rgba(0,0,0,0.1)'
        fill_color = 'rgba(79, 70, 229, 0.3)'
    else:
        text_color = 'white'
        bg_color = 'rgba(0,0,0,0)'
        grid_color = 'rgba(255,255,255,0.1)'
        fill_color = 'rgba(79, 70, 229, 0.3)'
    
    fig = go.Figure()
    
    # Add main skill trace
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor=fill_color,
        line=dict(color=color, width=2),
        name='Your Skills',
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.0f}/100<extra></extra>'
    ))
    
    # Add benchmark if requested
    if show_benchmark:
        benchmark_values = [70, 65, 60, 75, 55, 68]  # Industry average
        benchmark_closed = benchmark_values + [benchmark_values[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=benchmark_closed,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(6, 182, 212, 0.1)',
            line=dict(color='#06b6d4', width=2, dash='dash'),
            name='Industry Benchmark',
            hovertemplate='<b>%{theta}</b><br>Benchmark: %{r:.0f}/100<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color=text_color),
                gridcolor=grid_color
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=text_color)
            ),
            bgcolor=bg_color
        ),
        showlegend=True,
        title=dict(
            text=title,
            font=dict(size=18, color=text_color),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        height=450,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    return fig


def create_comparison_radar(
    candidates_data: List[Tuple[str, Dict[str, int]]],
    title: str = "Candidate Comparison",
    light_theme: bool = False
) -> go.Figure:
    """
    Create radar chart comparing multiple candidates
    
    Args:
        candidates_data: List of tuples (candidate_name, dimensions_dict)
        title: Chart title
        light_theme: If True, use light theme for PDF export
        
    Returns:
        Plotly Figure object
    """
    if not candidates_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No candidates selected for comparison",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        return fig
    
    # Use first candidate's dimensions as reference
    categories = list(candidates_data[0][1].keys())
    categories_closed = categories + [categories[0]]
    
    # Set colors based on theme
    if light_theme:
        text_color = 'black'
        bg_color = 'white'
        grid_color = 'rgba(0,0,0,0.1)'
    else:
        text_color = 'white'
        bg_color = 'rgba(0,0,0,0)'
        grid_color = 'rgba(255,255,255,0.1)'
    
    # Color palette for different candidates
    colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']
    
    fig = go.Figure()
    
    for idx, (name, dimensions) in enumerate(candidates_data[:5]):  # Max 5 candidates
        values = [dimensions.get(cat, 0) for cat in categories]
        values_closed = values + [values[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            fillcolor=f'rgba{tuple(list(bytes.fromhex(colors[idx][1:])) + [0.2])}',
            line=dict(color=colors[idx], width=2),
            name=name,
            hovertemplate=f'<b>{name}</b><br>%{{theta}}: %{{r:.0f}}/100<extra></extra>'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color=text_color),
                gridcolor=grid_color
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=text_color)
            ),
            bgcolor=bg_color
        ),
        showlegend=True,
        title=dict(
            text=title,
            font=dict(size=18, color=text_color),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        height=500,
        margin=dict(l=80, r=80, t=100, b=80),
        legend=dict(
            orientation="h",
            xanchor="center",
            x=0.5
        )
    )
    
    return fig
