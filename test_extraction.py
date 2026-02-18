"""
Debug script to test extraction on a real resume
"""
import sys
sys.path.insert(0, '/Users/akmalhaleema/Desktop/RecruitNova copy 2')

from utils.extract import extract_text_from_file, extract_skills
from utils.experience import estimate_experience_years

# Create a simple test resume file
test_resume = """
JOHN DOE
Email: john.doe@email.com | Phone: (555) 123-4567

SUMMARY
Senior Software Engineer with 5 years of experience in Python, JavaScript, and cloud technologies.

EXPERIENCE
Senior Software Engineer - Google Inc.
2019 - Present (5 years)
- Led development of microservices using Python and Go
- Managed team of 8 engineers
- Improved system performance by 60%

SKILLS
Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL

EDUCATION
Master of Science in Computer Science - MIT, 2019
"""

# Save to temp file
import tempfile
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write(test_resume)
    temp_path = f.name

print("Testing extraction...")
print("=" * 80)

# Test extraction
resume_text = extract_text_from_file(temp_path)
print(f"Extracted text length: {len(resume_text)} chars")
print(f"Text preview: {resume_text[:200]}...")
print()

skills_list = extract_skills(resume_text)
print(f"Skills found ({len(skills_list)}): {skills_list}")
print()

years_exp = estimate_experience_years(resume_text)
print(f"Years of experience: {years_exp}")
print()

# If all are empty/zero, there's an extraction problem
if len(resume_text) == 0:
    print("❌ ERROR: Resume text extraction failed!")
elif len(skills_list) == 0:
    print("❌ ERROR: Skills extraction returned empty!")
elif years_exp == 0:
    print("❌ ERROR: Experience estimation returned 0!")
else:
    print("✅ All extractions working")

# Clean up
import os
os.remove(temp_path)
