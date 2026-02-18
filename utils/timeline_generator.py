"""
Career Timeline Generator for RecruitNova
Creates visual timelines showing career progression and milestones
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re


def extract_timeline_from_resume(resume_text: str) -> List[Dict[str, Any]]:
    """
    Extract career timeline milestones from resume text
    
    Args:
        resume_text: Full resume text
        
    Returns:
        List of timeline events
    """
    events = []
    
    # Common patterns for dates in resumes
    date_patterns = [
        r'(\d{4})\s*[-–—]\s*(\d{4}|\bpresent\b|\bcurrent\b)',  # 2020 - 2023
        r'([A-Za-z]{3,}\.?\s*[\'"`’]?\s*\d{2,4})\s*[-–—]\s*([A-Za-z]{3,}\.?\s*[\'"`’]?\s*\d{2,4}|\bpresent\b|\bcurrent\b|\bnow\b)',  # Jan'17 - Present, Jan 2020 - Dec 2020
    ]
    
    # Try to find work experience sections
    lines = resume_text.split('\n')
    current_year = datetime.now().year
    
    # Look for common job titles and dates
    job_keywords = ['engineer', 'developer', 'manager', 'analyst', 'consultant', 
                   'designer', 'specialist', 'lead', 'director', 'coordinator', 
                   'intern', 'architect', 'administrator', 'technician',
                   'student', 'graduate', 'captain', 'volunteer', 'secretary', 
                   'president', 'vice', 'member', 'head', 'class', 'grade', 
                   'secondary', 'higher', 'bachelor', 'master', 'phd', 'degree', 'diploma']
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if line contains a job title
        if any(keyword in line_lower for keyword in job_keywords):
            # Look for dates in this line or next few lines
            found_event = False
            for j in range(i, min(i+3, len(lines))):
                # 1. Try date ranges first
                for pattern in date_patterns:
                    match = re.search(pattern, lines[j], re.IGNORECASE)
                    if match:
                        try:
                            start_date = match.group(1)
                            end_date = match.group(2)
                            
                            # Parse years
                            if any(x in end_date.lower() for x in ['present', 'current', 'now']):
                                end_year = current_year
                            else:
                                end_match = re.search(r'\d{2,4}', end_date)
                                if end_match:
                                    end_year = int(end_match.group())
                                    if end_year < 100: end_year += 2000
                                else:
                                    continue
                            
                            start_match = re.search(r'\d{2,4}', start_date)
                            if start_match:
                                start_year = int(start_match.group())
                                if start_year < 100: start_year += 2000
                            else:
                                continue
                            
                            # Clean title
                            title = line
                            if match:
                                title = line.replace(match.group(0), '').strip()
                                title = re.sub(r'[,–-]$', '', title).strip()
                            
                            events.append({
                                'title': title[:100],
                                'start_year': start_year,
                                'end_year': end_year,
                                'type': 'work',
                                'duration': end_year - start_year
                            })
                            found_event = True
                            break
                        except:
                            continue
                
                if found_event: break
                
                # 2. Fallback: Look for isolated Single Years (e.g. "2020")
                single_match = re.search(r'\b((?:19|20)\d{2})\b', lines[j])
                if single_match:
                    try:
                        year_val = int(single_match.group(1))
                        if 1990 <= year_val <= current_year + 1:
                            # Clean title
                            title = line
                            if j == i: 
                                title = line.replace(single_match.group(0), '').strip()
                                title = re.sub(r'[,–-]$', '', title).strip()
                                
                            events.append({
                                'title': title[:100],
                                'start_year': year_val,
                                'end_year': year_val,
                                'type': 'work',
                                'duration': 0 # Will show as "< 1 year"
                            })
                            found_event = True
                            break
                    except:
                        continue
    
    # Relaxed Fallback: If no events found, scan for ANY year ranges
    # This catches unstructured resumes that mention dates but miss keywords
    if not events:
        relaxed_pattern = r'(\b(?:19|20)\d{2}\b)\s*(?:[-–—]|\s+to\s+)\s*(\b(?:19|20)\d{2}\b|\bpresent\b|\bcurrent\b|\bnow\b)'
        
        for i, line in enumerate(lines):
            match = re.search(relaxed_pattern, line, re.IGNORECASE)
            # Avoid matching random numbers or copyright notices if possible
            if match and len(line) < 100 and not any(x in line.lower() for x in ['copyright', '©']):
                start_date = match.group(1)
                end_date = match.group(2)
                
                try:
                    if any(x in end_date.lower() for x in ['present', 'current', 'now']):
                        end_year = current_year
                    else:
                        end_year = int(end_date)
                    
                    start_year = int(start_date)
                    
                    # Clean title is whatever is before the date
                    title = line.replace(match.group(0), '').strip()
                    title = re.sub(r'[,–-]$', '', title).strip()
                    if not title: title = "Experience" # Fallback title
                    
                    if start_year <= end_year and end_year <= current_year + 1:
                        events.append({
                            'title': title[:100],
                            'start_year': start_year,
                            'end_year': end_year,
                            'type': 'work',
                            'duration': end_year - start_year
                        })
                except:
                    continue
                    
        # Sort if we found any relaxed matches
        events = sorted(events, key=lambda x: x['start_year'])
    
    return sorted(events, key=lambda x: x['start_year'])


def create_career_timeline(events: List[Dict[str, Any]], candidate_name: str = "Candidate", light_theme: bool = False) -> go.Figure:
    """
    Create interactive timeline visualization
    
    Args:
        events: List of career events
        candidate_name: Name for the timeline title
        light_theme: If True, use light theme for PDF export
        
    Returns:
        Plotly Figure object
    """
    if not events:
        fig = go.Figure()
        fig.add_annotation(
            text="No timeline data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        return fig
    
    # Set colors based on theme
    text_color = 'black' if light_theme else 'white'
    bg_color = 'white' if light_theme else 'rgba(0,0,0,0)'
    grid_color = 'rgba(0,0,0,0.1)' if light_theme else 'rgba(255,255,255,0.1)'
    line_color = 'rgba(0,0,0,0.3)' if light_theme else 'rgba(255,255,255,0.3)'
    
    # Prepare data for timeline
    fig = go.Figure()
    
    colors = {
        'work': '#4f46e5',
        'education': '#06b6d4',
        'certification': '#10b981',
        'achievement': '#f59e0b'
    }
    
    for idx, event in enumerate(events):
        # Create bar for each event
        fig.add_trace(go.Bar(
            name=event['title'],
            x=[event['end_year'] - event['start_year']],
            y=[event['title']],
            base=event['start_year'],
            orientation='h',
            marker=dict(
                color=colors.get(event['type'], '#4f46e5'),
                line=dict(color=line_color, width=1)
            ),
            hovertemplate=f"<b>{event['title']}</b><br>" +
                         f"Period: {event['start_year']} - {event['end_year']}<br>" +
                         f"Duration: {event['duration']} year(s)<extra></extra>",
            showlegend=False
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"{candidate_name}'s Career Timeline",
            font=dict(size=18, color=text_color),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Year", font=dict(color=text_color)),
            gridcolor=grid_color,
            tickfont=dict(color=text_color)
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color=text_color, size=10)
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        height=max(400, len(events) * 60),
        margin=dict(l=200, r=50, t=80, b=50),
        hovermode='closest'
    )
    
    return fig


def create_skill_progression_chart(skills_data: Dict[str, List[int]]) -> go.Figure:
    """
    Create line chart showing skill progression over time
    
    Args:
        skills_data: Dictionary mapping skill names to yearly proficiency scores
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']
    
    for idx, (skill, scores) in enumerate(skills_data.items()):
        years = list(range(len(scores)))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=scores,
            mode='lines+markers',
            name=skill,
            line=dict(color=colors[idx % len(colors)], width=3),
            marker=dict(size=8),
            hovertemplate=f"<b>{skill}</b><br>Year: %{{x}}<br>Proficiency: %{{y}}/100<extra></extra>"
        ))
    
    fig.update_layout(
        title="Skill Progression Over Time",
        xaxis_title="Years of Experience",
        yaxis_title="Proficiency Level",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 100])
    )
    
    return fig


def create_vertical_timeline_html(events: List[Dict[str, Any]]) -> str:
    """
    Create a modern vertical HTML timeline visualization
    
    Args:
        events: List of timeline events
        
    Returns:
        HTML string with embedded CSS
    """
    if not events:
        return "<div style='color: gray; text-align: center; padding: 20px;'>No timeline data available</div>"
        
    # CSS Styles for the timeline - Clean Dark Theme
    css = """
<style>
.timeline-wrapper {
    font-family: 'Source Sans Pro', sans-serif;
    padding: 20px 0;
}

.timeline-container {
    position: relative;
    max-width: 100%;
    margin: 0 auto;
    padding-left: 30px;
}

/* Vertical Line */
.timeline-container::before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    left: 9px;
    width: 2px;
    background: rgba(255, 255, 255, 0.2);
}

.timeline-item {
    position: relative;
    padding-left: 35px;
    margin-bottom: 25px;
}

/* Dot */
.timeline-dot {
    position: absolute;
    left: 0;
    top: 5px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #0e1117;
    border: 4px solid #4f46e5;
    z-index: 2;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
}

.timeline-content {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 15px;
    transition: transform 0.2s, background 0.2s, border-color 0.2s;
}

.timeline-content:hover {
    transform: translateX(3px);
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.3);
}

.timeline-date {
    color: #06b6d4;
    font-weight: 600;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 5px;
    display: block;
}

.timeline-title {
    color: white;
    font-size: 1.1em;
    font-weight: 700;
    margin: 0 0 8px 0;
    line-height: 1.3;
}

.timeline-duration {
    font-size: 0.8em;
    color: rgba(255, 255, 255, 0.6);
    background: rgba(255, 255, 255, 0.08);
    padding: 3px 8px;
    border-radius: 12px;
    display: inline-block;
}

/* Type-specific styling */
.type-education .timeline-dot { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2); }
.type-education .timeline-date { color: #10b981; }

.type-intern .timeline-dot { border-color: #f59e0b; box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2); }
.type-intern .timeline-date { color: #f59e0b; }
</style>
"""
    
    html_items = []
    
    # Sort events: newest first
    sorted_events = sorted(events, key=lambda x: x['start_year'], reverse=True)
    
    for event in sorted_events:
        start = event['start_year']
        end = event['end_year']
        end_display = "Present" if end >= datetime.now().year and event.get('type') == 'work' else end # Heuristic
        if 'present' in str(end).lower(): end_display = "Present"
        
        duration = event.get('duration', 1)
        duration_display = f"{duration} year{'s' if duration != 1 else ''}"
        if duration <= 0:
            duration_display = "< 1 year"
        
        # Determine styling class
        evt_type = "type-work"
        title_lines = event['title'].lower()
        if any(x in title_lines for x in ['degree', 'bachelor', 'master', 'phd', 'diploma', 'university']):
             evt_type = "type-education"
        elif 'intern' in title_lines:
             evt_type = "type-intern"
        
        item = f"""
<div class="timeline-item {evt_type}">
    <div class="timeline-dot"></div>
    <div class="timeline-content">
        <span class="timeline-date">{start} — {end_display}</span>
        <h3 class="timeline-title">{event['title']}</h3>
        <span class="timeline-duration">📅 {duration_display}</span>
    </div>
</div>
"""
        html_items.append(item)
    
    # Minify HTML to avoid Markdown rendering issues with indentation or newlines
    items_str = ''.join([x.replace('\n', ' ').strip() for x in html_items])
    css_str = css.strip()
    
    final_html = f"{css_str}<div class='timeline-wrapper'><div class='timeline-container'>{items_str}</div></div>"
    
    return final_html
