"""
Test script for Performance Predictor
Demonstrates varied scoring with different resume profiles
"""

import sys
sys.path.insert(0, '/Users/akmalhaleema/Desktop/RecruitNova copy 2')

from utils.performance_predictor import predict_performance

# Test Case 1: Entry-Level Developer
entry_level_resume = """
John Doe
Email: john@email.com

EDUCATION
Bachelor of Science in Computer Science
University of California, 2023

SKILLS
Python, JavaScript, HTML, CSS, Git

EXPERIENCE
Intern Software Developer (6 months)
Tech Startup Inc., 2023
- Worked on web development projects
- Learned React and Node.js
- Collaborated with team members
"""

# Test Case 2: Mid-Level Engineer
mid_level_resume = """
Jane Smith
Email: jane@email.com

EXPERIENCE
Software Engineer (3 years)
Tech Company, 2021-2024
- Developed microservices using Python and Go
- Implemented CI/CD pipelines
- Mentored junior developers
- Improved system performance by 40%

SKILLS
Python, Go, Docker, Kubernetes, AWS, React, PostgreSQL, Redis

EDUCATION
Master's in Computer Science
Stanford University, 2021

CERTIFICATIONS
AWS Certified Solutions Architect
"""

# Test Case 3: Senior Technical Lead
senior_resume = """
Alex Johnson
Email: alex@email.com

EXPERIENCE
Senior Technical Lead (8 years total)
Google, 2020-Present (4 years)
- Led team of 12 engineers
- Designed and delivered cloud-native architecture serving 10M+ users
- Managed $2M annual budget
- Drove strategic roadmap for AI/ML initiatives
- Hired and mentored 15+ engineers

Tech Lead
Amazon, 2016-2020 (4 years)
- Scaled distributed systems to handle 1M requests/second
- Promoted from Senior Engineer in 2018

SKILLS
Python, Go, Kubernetes, TensorFlow, AWS, GCP, System Design, 
Machine Learning, Deep Learning, Microservices, Leadership

EDUCATION
Ph.D. in Computer Science
MIT, 2016

CERTIFICATIONS
Certified Kubernetes Administrator
AWS Solutions Architect Professional
"""

print("=" * 80)
print("PERFORMANCE PREDICTOR TEST RESULTS")
print("=" * 80)

# Test Entry Level
print("\n1. ENTRY-LEVEL DEVELOPER")
print("-" * 80)
result1 = predict_performance(entry_level_resume, 0.5, ['python', 'javascript', 'html', 'css', 'git'])
print(f"Overall Score: {result1['overall_score']}/100")
print(f"Rating: {result1['rating']}")
print(f"Confidence: {result1['confidence']}")
print("\nDimension Scores:")
for dim, score in result1['dimension_scores'].items():
    print(f"  - {dim.replace('_', ' ').title()}: {score}")
print(f"\nRecommended Roles: {', '.join(result1['recommendations']['role_fit'])}")

# Test Mid Level
print("\n\n2. MID-LEVEL ENGINEER")
print("-" * 80)
result2 = predict_performance(mid_level_resume, 3.0, ['python', 'go', 'docker', 'kubernetes', 'aws', 'react', 'postgresql', 'redis'])
print(f"Overall Score: {result2['overall_score']}/100")
print(f"Rating: {result2['rating']}")
print(f"Confidence: {result2['confidence']}")
print("\nDimension Scores:")
for dim, score in result2['dimension_scores'].items():
    print(f"  - {dim.replace('_', ' ').title()}: {score}")
print(f"\nRecommended Roles: {', '.join(result2['recommendations']['role_fit'])}")

# Test Senior Level
print("\n\n3. SENIOR TECHNICAL LEAD")
print("-" * 80)
result3 = predict_performance(senior_resume, 8.0, ['python', 'go', 'kubernetes', 'tensorflow', 'aws', 'gcp', 'machine learning', 'deep learning'])
print(f"Overall Score: {result3['overall_score']}/100")
print(f"Rating: {result3['rating']}")
print(f"Confidence: {result3['confidence']}")
print("\nDimension Scores:")
for dim, score in result3['dimension_scores'].items():
    print(f"  - {dim.replace('_', ' ').title()}: {score}")
print(f"\nRecommended Roles: {', '.join(result3['recommendations']['role_fit'])}")

print("\n" + "=" * 80)
print("TEST COMPLETE - Scores should be distinctly different!")
print("=" * 80)
