"""
PDF Report Generator for RecruitNova
Creates professional PDF reports for candidate analysis and comparison
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
import plotly.io as pio
from typing import Dict, List, Any
import tempfile
import os


def generate_candidate_report_pdf(candidate_data: Dict[str, Any], charts: Dict[str, Any] = None) -> bytes:
    """
    Generate comprehensive PDF report for a single candidate
    
    Args:
        candidate_data: Dictionary with candidate information
        charts: Optional dictionary of plotly figures to include
        
    Returns:
        PDF file as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e293b'),  # Dark text
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        textColor=colors.black  # Black text for visibility
    )
    
    # Title
    title = Paragraph("Candidate Analysis Report", title_style)
    elements.append(title)
    
    # Candidate Info
    info_text = f"""
    <b>Candidate Name:</b> {candidate_data.get('name', 'N/A')}<br/>
    <b>Email:</b> {candidate_data.get('email', 'N/A')}<br/>
    <b>Experience:</b> {candidate_data.get('experience', 'N/A')}<br/>
    <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    elements.append(Paragraph(info_text, normal_style))
    elements.append(Spacer(1, 20))
    
    # Scores Section
    elements.append(Paragraph("Performance Scores", heading_style))
    
    scores_data = [
        ['Metric', 'Score'],
        ['ATS Score', f"{candidate_data.get('ats_score', 0)}/100"],
        ['Match Percentage', f"{candidate_data.get('match_percentage', 0)}%"],
        ['Overall Score', f"{candidate_data.get('overall_score', 0)}/100"],
        ['Skills Count', str(len(candidate_data.get('skills', [])))]
    ]
    
    scores_table = Table(scores_data, colWidths=[3*inch, 2*inch])
    scores_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text in table cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(scores_table)
    elements.append(Spacer(1, 20))
    
    # Skills Section
    if candidate_data.get('skills'):
        elements.append(Paragraph("Skills Profile", heading_style))
        skills_text = ", ".join(candidate_data['skills'][:20])  # Limit to 20 skills
        elements.append(Paragraph(skills_text, normal_style))
        elements.append(Spacer(1, 20))
    
    # Add charts if provided
    if charts:
        elements.append(PageBreak())
        elements.append(Paragraph("Visual Analytics", heading_style))
        
        temp_files = []  # Keep track of temp files
        
        for chart_name, fig in charts.items():
            try:
                # Convert plotly figure to image
                img_bytes = pio.to_image(fig, format='png', width=600, height=400)
                
                # Save to temp file (don't delete yet)
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                tmp.write(img_bytes)
                tmp.close()
                temp_files.append(tmp.name)
                
                # Add image to PDF
                img = Image(tmp.name, width=5*inch, height=3.3*inch)
                elements.append(img)
                elements.append(Spacer(1, 15))
                
            except Exception as e:
                elements.append(Paragraph(f"Chart '{chart_name}' could not be rendered: {str(e)}", styles['Normal']))
        
        # Clean up temp files after PDF is built
        def cleanup_temps():
            for tmp_path in temp_files:
                try:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                except:
                    pass
    
    # Recommendations Section
    elements.append(PageBreak())
    elements.append(Paragraph("Recommendations", heading_style))
    
    recommendations = candidate_data.get('recommendations', [
        "Strong technical skills alignment with job requirements",
        "Consider for technical interview round",
        "Verify experience claims during screening call"
    ])
    
    for rec in recommendations:
        elements.append(Paragraph(f"• {rec}", normal_style))
        elements.append(Spacer(1, 8))
    
    # Build PDF
    doc.build(elements)
    
    # Clean up temp files after PDF is built
    if charts:
        for tmp_path in temp_files:
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except:
                pass
    
    # Get the value of the BytesIO buffer and return it
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def generate_comparison_report_pdf(candidates: List[Dict[str, Any]], comparison_chart: Any = None) -> bytes:
    """
    Generate PDF report comparing multiple candidates
    
    Args:
        candidates: List of candidate dictionaries
        comparison_chart: Optional plotly figure for comparison
        
    Returns:
        PDF file as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        textColor=colors.black  # Black text for visibility
    )
    
    # Title
    title = Paragraph("Candidate Comparison Report", title_style)
    elements.append(title)
    
    # Report Info
    info_text = f"""
    <b>Number of Candidates:</b> {len(candidates)}<br/>
    <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    elements.append(Paragraph(info_text, normal_style))
    elements.append(Spacer(1, 20))
    
    # Comparison Table
    table_data = [['Name', 'ATS Score', 'Match %', 'Experience', 'Skills']]
    
    for candidate in candidates:
        table_data.append([
            candidate.get('name', 'N/A'),
            str(candidate.get('ats_score', 0)),
            f"{candidate.get('match_percentage', 0)}%",
            candidate.get('experience', 'N/A'),
            str(len(candidate.get('skills', [])))
        ])
    
    comparison_table = Table(table_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch, 1*inch])
    comparison_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text in table cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(comparison_table)
    elements.append(Spacer(1, 20))
    
    # Add comparison chart if provided
    if comparison_chart:
        try:
            img_bytes = pio.to_image(comparison_chart, format='png', width=700, height=450)
            
            # Save to temp file (don't delete yet)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            tmp.write(img_bytes)
            tmp.close()
            tmp_path = tmp.name
            
            img = Image(tmp_path, width=6*inch, height=3.9*inch)
            elements.append(img)
            
        except Exception as e:
            elements.append(Paragraph(f"Comparison chart could not be rendered: {str(e)}", styles['Normal']))
            tmp_path = None
    else:
        tmp_path = None
    
    # Build PDF
    doc.build(elements)
    
    # Clean up temp file after PDF is built
    if tmp_path and os.path.exists(tmp_path):
        try:
            os.unlink(tmp_path)
        except:
            pass
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
