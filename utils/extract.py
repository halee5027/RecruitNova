# utils/extract.py
import PyPDF2
import docx
import re

SKILLS_DB = {

    # PROGRAMMING LANGUAGES
    
    "python": {
        "synonyms": [
            "python", "python programming", "python developer",
            "python3", "python 3", "core python", "python code",
            "python coder", "python scripting", "python scripts"
        ],
        "courses": [
            "Python for Everybody – Coursera",
            "Complete Python Bootcamp – Udemy",
            "Google IT Automation with Python – Coursera",
            "Python Data Structures – Coursera",
            "Python Programming Masterclass – Udemy"
        ]
    },

    "java": {
        "synonyms": [
            "java", "core java", "java programming", "java developer",
            "java8", "java 8", "java coder", "java backend"
        ],
        "courses": [
            "Java Programming Masterclass – Udemy",
            "Object Oriented Programming in Java – Coursera",
            "Java for Beginners – Udemy"
        ]
    },

    "c": {
        "synonyms": [
            "c", "c language", "c programming", "c developer",
            "c coder", "ansi c"
        ],
        "courses": [
            "C Programming For Beginners – Udemy",
            "Introduction to C – Coursera",
            "C Programming Masterclass – Udemy"
        ]
    },

    "cpp": {
        "synonyms": [
            "c++", "cpp", "c plus plus", "c++ programming",
            "c++ developer", "c++ coder", "advanced c++"
        ],
        "courses": [
            "Beginning C++ – Udemy",
            "C++ Complete Guide – Udemy",
            "Object-Oriented C++ – Coursera"
        ]
    },

    "javascript": {
        "synonyms": [
            "javascript", "js", "ecmascript", "js developer",
            "javascript programming", "node javascript"
        ],
        "courses": [
            "JavaScript: From Zero to Expert – Udemy",
            "Modern JavaScript Bootcamp – Udemy",
            "JavaScript Essentials – Coursera"
        ]
    },

    "typescript": {
        "synonyms": [
            "typescript", "ts", "typed javascript"
        ],
        "courses": [
            "Understanding TypeScript – Udemy",
            "TypeScript for Beginners – Coursera"
        ]
    },

    "sql": {
        "synonyms": [
            "sql", "mysql", "postgresql", "sql server", "mssql",
            "oracle sql", "database querying", "rdbms", "sql developer",
            "pl/sql", "postgres", "mysql database"
        ],
        "courses": [
            "SQL for Data Science – Coursera",
            "The Complete SQL Bootcamp – Udemy",
            "MySQL Bootcamp – Udemy",
            "SQL Server for Beginners – Udemy"
        ]
    },

    "html": {
        "synonyms": [
            "html", "html5", "web markup", "html coding"
        ],
        "courses": [
            "HTML & CSS Bootcamp – Udemy",
            "HTML5 Basics – Coursera"
        ]
    },

    "css": {
        "synonyms": [
            "css", "css3", "tailwind css", "bootstrap", "style sheets"
        ],
        "courses": [
            "CSS Complete Guide – Udemy",
            "Web Styling with CSS – Coursera"
        ]
    },

    "react": {
        "synonyms": [
            "react", "react js", "reactjs", "react.js",
            "react developer", "frontend react"
        ],
        "courses": [
            "React Frontend Developer – Coursera",
            "React Complete Guide – Udemy",
            "Modern React Bootcamp – Udemy"
        ]
    },

    "node": {
        "synonyms": [
            "node", "nodejs", "node.js", "node developer",
            "backend node", "express js", "expressjs"
        ],
        "courses": [
            "Node.js Developer Course – Udemy",
            "Backend Development with Node – Coursera"
        ]
    },

    "php": {
        "synonyms": [
            "php", "php developer", "php programming",
            "laravel", "php coder"
        ],
        "courses": [
            "PHP for Beginners – Udemy",
            "Laravel Masterclass – Udemy"
        ]
    },

    "swift": {
        "synonyms": [
            "swift", "swift programming", "ios swift"
        ],
        "courses": [
            "iOS App Development with Swift – Coursera",
            "Swift Programming Bootcamp – Udemy"
        ]
    },

    "kotlin": {
        "synonyms": [
            "kotlin", "android kotlin", "kotlin programming"
        ],
        "courses": [
            "Kotlin Bootcamp – Udemy",
            "Android Kotlin Course – Coursera"
        ]
    },

# DATA SCIENCE & MACHINE LEARNING


    "data science": {
        "synonyms": [
            "data science", "data scientist", "data science projects",
            "data analysis", "data analytics", "applied data science",
            "data science workflow", "data scientist role"
        ],
        "courses": [
            "IBM Data Science Professional Certificate – Coursera",
            "Google Data Analytics – Coursera",
            "Data Science A-Z – Udemy",
            "Applied Data Science with Python – Coursera"
        ]
    },

    "machine learning": {
        "synonyms": [
            "machine learning", "ml", "ml engineer", "ml algorithms",
            "supervised learning", "unsupervised learning", 
            "machine learning models", "machine learning engineer"
        ],
        "courses": [
            "Machine Learning by Andrew Ng – Coursera",
            "Complete Machine Learning Bootcamp – Udemy",
            "Machine Learning Specialization – Coursera"
        ]
    },

    "deep learning": {
        "synonyms": [
            "deep learning", "dl", "neural networks", "cnn", "rnn",
            "lstm", "transformers", "deep neural networks",
            "deeplearning", "deep learning engineer"
        ],
        "courses": [
            "Deep Learning Specialization – Coursera",
            "Neural Networks & Deep Learning – Coursera",
            "Deep Learning with PyTorch – Udemy"
        ]
    },

    "artificial intelligence": {
        "synonyms": [
            "ai", "artificial intelligence", "ai engineer",
            "ai models", "ai ml", "ai based systems"
        ],
        "courses": [
            "AI For Everyone – Coursera",
            "AI Engineering with Microsoft – Udemy",
            "Introduction to AI – Coursera"
        ]
    },

    "nlp": {
        "synonyms": [
            "nlp", "natural language processing", "text classification",
            "text mining", "nltk", "spacy", "transformer nlp"
        ],
        "courses": [
            "Natural Language Processing Specialization – Coursera",
            "NLP with Deep Learning – Udemy",
            "Advanced NLP with Transformers – Coursera"
        ]
    },

    "computer vision": {
        "synonyms": [
            "computer vision", "cv", "object detection",
            "image processing", "opencv", "image classification"
        ],
        "courses": [
            "Computer Vision with TensorFlow – Coursera",
            "OpenCV Complete Guide – Udemy",
            "Deep Learning for Computer Vision – Udemy"
        ]
    },

    "pandas": {
        "synonyms": [
            "pandas", "python pandas", "dataframe handling",
            "data wrangling", "pandas library"
        ],
        "courses": [
            "Data Analysis with Pandas – Coursera",
            "Pandas for Data Science – Udemy"
        ]
    },

    "numpy": {
        "synonyms": [
            "numpy", "numerical python", "numpy arrays",
            "matrix operations numpy"
        ],
        "courses": [
            "NumPy for Beginners – Udemy",
            "Python Scientific Computing – Coursera"
        ]
    },

    "matplotlib": {
        "synonyms": [
            "matplotlib", "data visualization python",
            "plotting python", "pyplot", "graphs python"
        ],
        "courses": [
            "Python Visualization Guide – Udemy",
            "Data Visualization with Python – Coursera"
        ]
    },

    "seaborn": {
        "synonyms": [
            "seaborn", "sns python", "python visualization seaborn"
        ],
        "courses": [
            "Seaborn Masterclass – Udemy",
            "Data Visualization with Python – Coursera"
        ]
    },

    "scikit-learn": {
        "synonyms": [
            "scikit learn", "sklearn", "machine learning sklearn",
            "ml models sklearn"
        ],
        "courses": [
            "Sklearn Machine Learning – Coursera",
            "ML with Scikit-Learn – Udemy"
        ]
    },

    "tensorflow": {
        "synonyms": [
            "tensorflow", "tf", "tensorflow keras", "tf developer"
        ],
        "courses": [
            "TensorFlow Developer Certificate – Coursera",
            "Deep Learning with TensorFlow – Udemy"
        ]
    },

    "keras": {
        "synonyms": [
            "keras", "keras neural networks", "keras deep learning"
        ],
        "courses": [
            "Advanced Keras – Udemy",
            "Deep Learning with Keras – Coursera"
        ]
    },

    "pytorch": {
        "synonyms": [
            "pytorch", "torch", "pytorch deep learning",
            "pytorch models", "pytorch neural networks"
        ],
        "courses": [
            "Deep Learning with PyTorch – Udemy",
            "PyTorch Bootcamp – Coursera"
        ]
    },

    
    # DATA ENGINEERING

    "data engineering": {
        "synonyms": [
            "data engineering", "data engineer", "etl pipelines",
            "data pipelines", "big data engineering"
        ],
        "courses": [
            "Google Cloud Data Engineering – Coursera",
            "Data Engineering Bootcamp – Udemy"
        ]
    },

    "spark": {
        "synonyms": [
            "spark", "apache spark", "pyspark", "spark sql",
            "spark data processing", "spark mllib"
        ],
        "courses": [
            "Apache Spark with Python – Udemy",
            "Big Data with Spark – Coursera"
        ]
    },

    "hadoop": {
        "synonyms": [
            "hadoop", "big data hadoop", "hdfs", "hadoop ecosystem"
        ],
        "courses": [
            "Hadoop for Big Data – Udemy",
            "Big Data Engineering – Coursera"
        ]
    },

    "airflow": {
        "synonyms": [
            "airflow", "apache airflow", "workflow orchestration airflow",
            "etl scheduling airflow"
        ],
        "courses": [
            "Apache Airflow Bootcamp – Udemy",
            "Data Pipelines with Airflow – Coursera"
        ]
    },

    "tableau": {
        "synonyms": [
            "tableau", "tableau dashboards", "tableau visualization",
            "bi tableau", "data viz tableau"
        ],
        "courses": [
            "Tableau 2024 A-Z – Udemy",
            "Data Visualization with Tableau – Coursera"
        ]
    },

    "power bi": {
        "synonyms": [
            "power bi", "microsoft powerbi", "bi dashboards",
            "powerbi reports", "power bi data modeling"
        ],
        "courses": [
            "Power BI Desktop – Udemy",
            "Data Analysis with Power BI – Coursera"
        ]
    },

        "excel": {
            "synonyms": [
                "excel", "ms excel", "microsoft excel", "excel skills",
                "advanced excel", "excel spreadsheets", "excel formulas"
            ],
            "courses": [
                "Excel Skills for Business – Coursera",
                "Advanced Excel – Udemy",
                "Excel Data Analysis – Coursera"
            ]
        },
    
        "devops": {
            "synonyms": [
                "dev ops", "dev-ops", "devops engineer",
                "ci/cd", "continuous integration", "continuous delivery",
                "infrastructure automation"
            ],
            "courses": [
                "DevOps Engineer Course – Udemy",
                "DevOps on AWS – Coursera"
            ]
        },
    
        "jenkins": {
            "synonyms": [
                "jenkins pipeline", "ci tool", "jenkins automation"
            ],
            "courses": [
                "Jenkins for DevOps – Udemy"
            ]
        },
    
        "shell scripting": {
            "synonyms": [
                "shell script", "bash scripting",
                "terminal scripting", "command line scripts"
            ],
            "courses": [
                "Shell Scripting Basics – Udemy"
            ]
        },
    
        "mongodb": {
            "synonyms": [
                "mongo db", "no sql", "nosql", "mongodb atlas"
            ],
            "courses": [
                "MongoDB Complete Guide – Udemy",
                "NoSQL Databases – Coursera"
            ]
        },
    
        "etl": {
            "synonyms": [
                "extract transform load", "data pipeline",
                "etl pipeline", "data extraction"
            ],
            "courses": [
                "ETL and Data Pipelines – Udemy"
            ]
        },
    
        "business analysis": {
            "synonyms": [
                "business analyst", "ba skills", "requirements gathering"
            ],
            "courses": [
                "Business Analysis Fundamentals – Udemy"
            ]
        },
    
        "salesforce": {
            "synonyms": [
                "sales force", "crm salesforce", "salesforce admin", "sfdc"
            ],
            "courses": [
                "Salesforce Administrator Bootcamp – Udemy"
            ]
        },
    
        "project management": {
            "synonyms": [
                "pm skills", "project planning",
                "agile project management", "agile methodology", "scrum"
            ],
            "courses": [
                "Project Management Fundamentals – Coursera",
                "Agile Project Management – Udemy"
            ]
        }
    }



def extract_text_from_file(file_like):
    name = getattr(file_like, 'name', '')
    try:
        if name.lower().endswith('.pdf'):
            reader = PyPDF2.PdfReader(file_like)
            return '\n'.join([page.extract_text() or '' for page in reader.pages])
        elif name.lower().endswith('.docx'):
            doc = docx.Document(file_like)
            return '\n'.join([p.text for p in doc.paragraphs])
        return file_like.getvalue().decode('utf-8')
    except:
        return ''

def extract_skills(text):
   
    def extract_skills(text: str):
     """Return canonical skill names found in the text using SKILLS_DB."""
    if not text:
        return []

    txt = text.lower()
    found = set()

    for skill, info in SKILLS_DB.items():
        # info is a dict like {"synonyms": [...], "courses": [...]}
        syn_list = info.get("synonyms", [])
        for syn in syn_list:
            if syn.lower() in txt:
                found.add(skill)
                break  # no need to check other synonyms for this skill

    return sorted(found)


def match_job_skills(resume_skills, job_text):
    if not job_text or not resume_skills:
        return 0

    job_skills = extract_skills(job_text)  # will now use SKILLS_DB correctly
    if not job_skills:
        return 0

    common = len(set(resume_skills) & set(job_skills))
    return min(100, (common / len(job_skills)) * 100)
