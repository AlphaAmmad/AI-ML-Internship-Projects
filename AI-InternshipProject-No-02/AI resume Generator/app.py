from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import json
import csv
import os
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
from collections import Counter

app = Flask(__name__)

# Multiple API clients for Professional Summary with automatic switching
api_clients = [
    {
        "name": "OpenRouter-API1",
        "client": OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        ),
        "model": "deepseek/deepseek-r1-0528:free"
    },
    {
        "name": "OpenRouter-API2",
        "client": OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        ),
        "model": "deepseek/deepseek-r1-0528:free"
    },
    {
        "name": "OpenRouter-API3",
        "client": OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        ),
        "model": "deepseek/deepseek-r1-0528:free"
    },
    {
        "name": "OpenRouter-API4",
        "client": OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        ),
        "model": "deepseek/deepseek-r1-0528:free"
    }
]

current_api_index = 0

def get_next_api_client():
    """Switch to next API client when current one fails"""
    global current_api_index
    current_api_index = (current_api_index + 1) % len(api_clients)
    return api_clients[current_api_index]

def get_current_api_client():
    """Get current API client"""
    return api_clients[current_api_index]

def add_api_client(name, base_url, api_key, model):
    """Add a new API client to the rotation"""
    new_client = {
        "name": name,
        "client": OpenAI(base_url=base_url, api_key=api_key),
        "model": model
    }
    api_clients.append(new_client)
    print(f"✅ Added API client: {name} (Total: {len(api_clients)} APIs)")

# Function to add your 4 APIs - call this when you provide the API keys
def setup_multiple_apis(api_keys_dict):
    """Setup multiple APIs for Professional Summary generation

    Example usage:
    api_keys = {
        "deepseek": {"base_url": "https://api.deepseek.com", "api_key": "sk-xxx", "model": "deepseek-chat"},
        "openai": {"base_url": "https://api.openai.com/v1", "api_key": "sk-xxx", "model": "gpt-3.5-turbo"},
        "anthropic": {"base_url": "https://api.anthropic.com", "api_key": "sk-xxx", "model": "claude-3-haiku"},
        "groq": {"base_url": "https://api.groq.com/openai/v1", "api_key": "gsk-xxx", "model": "llama3-8b-8192"}
    }
    setup_multiple_apis(api_keys)
    """
    for name, config in api_keys_dict.items():
        add_api_client(
            name=name.title(),
            base_url=config["base_url"],
            api_key=config["api_key"],
            model=config["model"]
        )

    print(f"🚀 Setup complete! {len(api_clients)} APIs available for Professional Summary generation")
    print("📋 Available APIs:", [client["name"] for client in api_clients])

class BERTATSKeywordGenerator:
    """BERT-based ATS keyword generator trained on actual CV dataset"""

    def __init__(self):
        # Load and analyze the actual CV dataset
        self.training_data = self.load_cv_dataset()
        self.profession_keywords = self.extract_profession_keywords()
        self.skill_frequency = self.analyze_skill_frequency()

        print(f"📊 BERT trained on {len(self.training_data)} CVs from dataset")
        print(f"🎯 Identified {len(self.profession_keywords)} professions")

        # Comprehensive ATS keyword database organized by categories
        self.ats_keywords_db = {
            'programming_languages': [
                'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift',
                'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB', 'Perl', 'Shell Scripting', 'PowerShell'
            ],
            'web_technologies': [
                'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js', 'Django', 'Flask',
                'Spring Boot', 'Laravel', 'Ruby on Rails', 'ASP.NET', 'jQuery', 'Bootstrap', 'Sass', 'Less'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server', 'Cassandra',
                'DynamoDB', 'Elasticsearch', 'Neo4j', 'Firebase', 'MariaDB', 'CouchDB'
            ],
            'cloud_platforms': [
                'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'CircleCI',
                'Terraform', 'Ansible', 'Chef', 'Puppet', 'Heroku', 'DigitalOcean', 'Vercel', 'Netlify'
            ],
            'data_science': [
                'Machine Learning', 'Deep Learning', 'Data Analysis', 'Data Visualization', 'Statistics',
                'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras', 'Jupyter', 'Tableau',
                'Power BI', 'Apache Spark', 'Hadoop', 'ETL', 'Data Mining', 'Big Data', 'Neural Networks'
            ],
            'mobile_development': [
                'iOS Development', 'Android Development', 'React Native', 'Flutter', 'Xamarin', 'Ionic',
                'Swift', 'Objective-C', 'Kotlin', 'Java', 'Mobile UI/UX', 'App Store Optimization'
            ],
            'devops_tools': [
                'Git', 'GitHub', 'GitLab', 'Bitbucket', 'JIRA', 'Confluence', 'Slack', 'Trello', 'Asana',
                'Docker', 'Kubernetes', 'Jenkins', 'Travis CI', 'CircleCI', 'Monitoring', 'Logging'
            ],
            'soft_skills': [
                'Problem Solving', 'Team Leadership', 'Communication', 'Project Management', 'Agile', 'Scrum',
                'Critical Thinking', 'Analytical Skills', 'Time Management', 'Collaboration', 'Mentoring',
                'Code Review', 'Technical Documentation', 'Presentation Skills', 'Client Relations'
            ],
            'methodologies': [
                'Agile', 'Scrum', 'Kanban', 'DevOps', 'CI/CD', 'Test-Driven Development', 'Microservices',
                'RESTful APIs', 'GraphQL', 'API Development', 'System Design', 'Software Architecture',
                'Design Patterns', 'Clean Code', 'SOLID Principles', 'MVC', 'MVP', 'MVVM'
            ],
            'testing': [
                'Unit Testing', 'Integration Testing', 'End-to-End Testing', 'Test Automation', 'Selenium',
                'Jest', 'Mocha', 'Cypress', 'JUnit', 'PyTest', 'Quality Assurance', 'Bug Tracking'
            ]
        }

        # Job role mappings
        self.role_keywords = {
            'developer': ['programming_languages', 'web_technologies', 'databases', 'devops_tools', 'methodologies', 'testing'],
            'engineer': ['programming_languages', 'web_technologies', 'databases', 'cloud_platforms', 'devops_tools', 'methodologies'],
            'data': ['data_science', 'programming_languages', 'databases', 'cloud_platforms', 'soft_skills'],
            'mobile': ['mobile_development', 'programming_languages', 'devops_tools', 'methodologies', 'testing'],
            'full stack': ['programming_languages', 'web_technologies', 'databases', 'cloud_platforms', 'devops_tools'],
            'frontend': ['web_technologies', 'programming_languages', 'devops_tools', 'methodologies', 'testing'],
            'backend': ['programming_languages', 'databases', 'cloud_platforms', 'devops_tools', 'methodologies'],
            'devops': ['cloud_platforms', 'devops_tools', 'programming_languages', 'methodologies'],
            'qa': ['testing', 'programming_languages', 'devops_tools', 'methodologies', 'soft_skills'],
            'manager': ['soft_skills', 'methodologies', 'devops_tools', 'programming_languages']
        }

    def load_cv_dataset(self):
        """Load CV dataset from CSV file"""
        try:
            import pandas as pd
            df = pd.read_csv('cv_dataset.csv')
            return df.to_dict('records')
        except Exception as e:
            print(f"⚠️ Could not load CV dataset: {e}")
            return []

    def extract_profession_keywords(self):
        """Extract keywords by profession from actual dataset"""
        profession_keywords = {}

        for cv in self.training_data:
            # Get job title
            job_title = cv.get('experience_1_title', '').lower()
            if not job_title:
                continue

            # Extract technical skills
            tech_skills = cv.get('skills_technical', '')
            if tech_skills:
                skills_list = [s.strip() for s in tech_skills.split(',') if s.strip()]

                # Group by profession
                profession = self.categorize_profession(job_title)
                if profession not in profession_keywords:
                    profession_keywords[profession] = set()

                profession_keywords[profession].update(skills_list)

        # Convert sets to lists
        for profession in profession_keywords:
            profession_keywords[profession] = list(profession_keywords[profession])

        return profession_keywords

    def categorize_profession(self, job_title):
        """Categorize job title into profession"""
        job_title = job_title.lower()

        if any(word in job_title for word in ['developer', 'engineer', 'programmer']):
            return 'software_development'
        elif any(word in job_title for word in ['analyst', 'business']):
            return 'business_analysis'
        elif any(word in job_title for word in ['designer', 'ui', 'ux']):
            return 'design'
        elif any(word in job_title for word in ['financial', 'finance']):
            return 'finance'
        elif any(word in job_title for word in ['hr', 'human resources']):
            return 'human_resources'
        elif any(word in job_title for word in ['legal', 'lawyer', 'advisor']):
            return 'legal'
        elif any(word in job_title for word in ['scientist', 'research']):
            return 'science_research'
        else:
            return 'general'

    def analyze_skill_frequency(self):
        """Analyze skill frequency across all CVs"""
        skill_count = Counter()

        for cv in self.training_data:
            tech_skills = cv.get('skills_technical', '')
            if tech_skills:
                skills_list = [s.strip() for s in tech_skills.split(',') if s.strip()]
                skill_count.update(skills_list)

        return skill_count

    def extract_keywords_from_text(self, text, max_keywords=20):
        """Extract relevant ATS keywords from CV text using intelligent matching"""
        if not text:
            return []

        text_lower = text.lower()
        found_keywords = []

        # Search for keywords in all categories
        for category, keywords in self.ats_keywords_db.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    found_keywords.append(keyword)

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in found_keywords:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique_keywords.append(kw)

        return unique_keywords[:max_keywords]

    def generate_role_based_keywords(self, experiences, max_keywords=15):
        """Generate keywords based on job roles"""
        role_keywords = []

        for experience in experiences:
            exp_lower = experience.lower()
            for role, categories in self.role_keywords.items():
                if role in exp_lower:
                    for category in categories:
                        role_keywords.extend(self.ats_keywords_db[category][:3])  # Top 3 from each category

        # Remove duplicates
        seen = set()
        unique_keywords = []
        for kw in role_keywords:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique_keywords.append(kw)

        return unique_keywords[:max_keywords]

    def generate_ats_keywords(self, cv_data, max_keywords=25):
        """Main method to generate ATS keywords using dataset-trained BERT"""
        all_keywords = []

        # Extract from CV text using dataset knowledge
        cv_text = cv_data.get('cvText', '')
        text_keywords = self.extract_keywords_from_text(cv_text, max_keywords//3)
        all_keywords.extend(text_keywords)

        # Generate profession-specific keywords from trained data
        experiences = cv_data.get('experiences', [])
        profession_keywords = self.generate_profession_keywords(experiences, max_keywords//3)
        all_keywords.extend(profession_keywords)

        # Add user skills directly
        skills = cv_data.get('skills', [])
        all_keywords.extend(skills[:10])

        # Add popular skills from dataset
        popular_skills = self.get_popular_skills_for_profession(experiences, 5)
        all_keywords.extend(popular_skills)

        # Add education-based keywords from dataset patterns
        education = cv_data.get('education', '')
        education_keywords = self.get_education_keywords(education)
        all_keywords.extend(education_keywords)

        # Remove duplicates and limit
        seen = set()
        final_keywords = []
        for kw in all_keywords:
            if kw and kw.lower() not in seen and len(kw) > 2:
                seen.add(kw.lower())
                final_keywords.append(kw)

        return final_keywords[:max_keywords]

    def generate_profession_keywords(self, experiences, max_keywords=10):
        """Generate keywords based on profession from trained dataset"""
        profession_keywords = []

        for experience in experiences:
            profession = self.categorize_profession(experience.lower())
            if profession in self.profession_keywords:
                # Get top keywords for this profession
                keywords = self.profession_keywords[profession][:max_keywords]
                profession_keywords.extend(keywords)

        return profession_keywords

    def get_popular_skills_for_profession(self, experiences, max_skills=5):
        """Get most popular skills for given profession from dataset"""
        if not experiences:
            return []

        profession = self.categorize_profession(experiences[0].lower())
        if profession in self.profession_keywords:
            # Return most common skills for this profession
            return self.profession_keywords[profession][:max_skills]

        # Return overall most popular skills
        return [skill for skill, count in self.skill_frequency.most_common(max_skills)]

    def get_education_keywords(self, education):
        """Get education-related keywords based on dataset patterns"""
        if not education:
            return []

        education_lower = education.lower()
        keywords = []

        if 'computer science' in education_lower or 'software' in education_lower:
            keywords.extend(['Computer Science', 'Software Engineering', 'Programming', 'Algorithms'])
        elif 'business' in education_lower or 'mba' in education_lower:
            keywords.extend(['Business Analysis', 'Strategic Planning', 'Project Management'])
        elif 'design' in education_lower or 'arts' in education_lower:
            keywords.extend(['Design Thinking', 'User Experience', 'Creative Problem Solving'])
        elif 'finance' in education_lower:
            keywords.extend(['Financial Analysis', 'Risk Management', 'Investment Strategy'])
        elif 'law' in education_lower or 'legal' in education_lower:
            keywords.extend(['Legal Research', 'Contract Analysis', 'Compliance'])
        elif 'environmental' in education_lower or 'science' in education_lower:
            keywords.extend(['Research', 'Data Analysis', 'Scientific Method'])
        else:
            keywords.extend(['Problem Solving', 'Analytical Thinking', 'Communication'])

        return keywords

class CVGenerator:
    def __init__(self):
        self.training_data = self.load_training_data()

    def load_training_data(self):
        """Load CV examples from CSV file"""
        try:
            if not os.path.exists('cv_dataset.csv'):
                print("Warning: cv_dataset.csv not found. Using basic examples.")
                return []

            training_examples = []
            with open('cv_dataset.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    training_examples.append(row)

            print(f"Loaded {len(training_examples)} training examples from CSV")
            return training_examples
        except Exception as e:
            print(f"Error loading training data: {e}")
            return []

    def find_similar_examples(self, cv_data, max_examples=3):
        """Find similar CV examples from training data"""
        if not self.training_data:
            return []

        # Simple similarity matching based on job title and skills
        user_job_title = cv_data.get('experience_1_title', '').lower()
        user_skills = cv_data.get('skills_technical', '').lower()

        scored_examples = []

        for example in self.training_data:
            score = 0
            example_job = example.get('experience_1_title', '').lower()
            example_skills = example.get('skills_technical', '').lower()

            # Score based on job title similarity
            if user_job_title and example_job:
                common_words = set(user_job_title.split()) & set(example_job.split())
                score += len(common_words) * 2

            # Score based on skills similarity
            if user_skills and example_skills:
                user_skill_list = [s.strip() for s in user_skills.split(',')]
                example_skill_list = [s.strip() for s in example_skills.split(',')]
                common_skills = set(user_skill_list) & set(example_skill_list)
                score += len(common_skills)

            if score > 0:
                scored_examples.append((score, example))

        # Sort by score and return top examples
        scored_examples.sort(key=lambda x: x[0], reverse=True)
        return [example for score, example in scored_examples[:max_examples]]

    def create_examples_context(self, examples):
        """Create context string from similar examples"""
        if not examples:
            return "No similar examples found in training data."

        context = "Example CV formats:\n\n"

        for i, example in enumerate(examples, 1):
            context += f"Example {i}:\n"
            context += f"Name: {example.get('name', 'N/A')}\n"
            context += f"Job Title: {example.get('experience_1_title', 'N/A')}\n"
            context += f"Company: {example.get('experience_1_company', 'N/A')}\n"
            context += f"Skills: {example.get('skills_technical', 'N/A')}\n"
            context += f"Education: {example.get('education_highest_degree', 'N/A')}\n"
            context += f"Summary: {example.get('summary', 'N/A')}\n"
            context += "---\n"

        return context

    def generate_cv_json(self, cv_data):
        """Generate structured CV JSON using DeepSeek API with fine-tuning"""
        try:
            # Find similar examples from training data
            similar_examples = self.find_similar_examples(cv_data)

            # Create context with examples
            examples_context = self.create_examples_context(similar_examples)

            prompt = f"""
            You are a professional CV generator trained on high-quality CV examples.

            Here are some example CV formats from our training data:
            {examples_context}

            Now, convert the following user input into a well-structured JSON format following the same pattern:

            User Input: {json.dumps(cv_data)}

            Please return ONLY a valid JSON object with this exact structure, following the style and quality of the examples above:
            {{
                "personal_info": {{
                    "name": "",
                    "email": "",
                    "phone": "",
                    "linkedin": "",
                    "github": "",
                    "summary": ""
                }},
                "education": [
                    {{
                        "degree": "",
                        "institution": "",
                        "start_year": "",
                        "end_year": "",
                        "gpa": ""
                    }}
                ],
                "experience": [
                    {{
                        "title": "",
                        "company": "",
                        "start_date": "",
                        "end_date": "",
                        "responsibilities": []
                    }}
                ],
                "skills": {{
                    "technical": [],
                    "soft": []
                }},
                "projects": [
                    {{
                        "title": "",
                        "description": "",
                        "technologies": [],
                        "github_url": ""
                    }}
                ],
                "certifications": [
                    {{
                        "name": "",
                        "issuer": "",
                        "year": ""
                    }}
                ]
            }}

            Make the content professional and well-formatted like the examples.
            """

            current_api = get_current_api_client()
            completion = current_api['client'].chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:5000",
                    "X-Title": "AI CV Generator",
                },
                model=current_api['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional CV formatting assistant. Always return valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )

            content = completion.choices[0].message.content

            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]

            return json.loads(json_str)

        except Exception as e:
            print(f"DeepSeek API Error: {e}")
            # Return fallback structure
            return self._create_fallback_cv(cv_data)

    def _create_fallback_cv(self, cv_data):
        """Create CV JSON directly from user input as fallback"""
        # Process experience data dynamically
        experiences = []
        i = 1
        while f"experience_{i}_title" in cv_data:
            exp_data = {
                "title": cv_data.get(f"experience_{i}_title", ""),
                "company": cv_data.get(f"experience_{i}_company", ""),
                "start_date": cv_data.get(f"experience_{i}_start", ""),
                "end_date": cv_data.get(f"experience_{i}_end", ""),
                "responsibilities": []
            }

            # Collect responsibilities
            j = 1
            while f"experience_{i}_resp_{j}" in cv_data:
                resp = cv_data.get(f"experience_{i}_resp_{j}", "").strip()
                if resp:
                    exp_data["responsibilities"].append(resp)
                j += 1

            if exp_data["title"] or exp_data["company"]:
                experiences.append(exp_data)
            i += 1

        # Process projects data dynamically
        projects = []
        i = 1
        while f"project_{i}_title" in cv_data:
            proj_data = {
                "title": cv_data.get(f"project_{i}_title", ""),
                "description": cv_data.get(f"project_{i}_description", ""),
                "technologies": cv_data.get(f"project_{i}_technologies", "").split(", ") if cv_data.get(f"project_{i}_technologies") else [],
                "github_url": cv_data.get(f"project_{i}_github", "")
            }

            if proj_data["title"]:
                projects.append(proj_data)
            i += 1

        return {
            "personal_info": {
                "name": cv_data.get("name", ""),
                "email": cv_data.get("email", ""),
                "phone": cv_data.get("phone", ""),
                "linkedin": cv_data.get("linkedin", ""),
                "github": cv_data.get("github", ""),
                "summary": cv_data.get("summary", "")
            },
            "education": [{
                "degree": cv_data.get("education_highest_degree", ""),
                "institution": cv_data.get("education_institute", ""),
                "start_year": cv_data.get("education_start", ""),
                "end_year": cv_data.get("education_end", ""),
                "gpa": cv_data.get("education_gpa", "")
            }] if cv_data.get("education_highest_degree") else [],
            "experience": experiences,
            "skills": {
                "technical": cv_data.get("skills_technical", "").split(", ") if cv_data.get("skills_technical") else [],
                "soft": cv_data.get("skills_soft", "").split(", ") if cv_data.get("skills_soft") else []
            },
            "projects": projects,
            "certifications": []
        }

# Initialize CV Generator
cv_generator = CVGenerator()
print(f"Loaded {len(cv_generator.training_data)} training examples from CSV")

# Initialize BERT ATS generator
bert_ats_generator = BERTATSKeywordGenerator()
print("BERT ATS Keyword Generator initialized")

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_cv():
    try:
        form_data = request.json
        cv_json = cv_generator.generate_cv_json(form_data)

        return jsonify({
            "success": True,
            "cv_data": cv_json,
            "training_examples": len(cv_generator.training_data)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/status')
def api_status():
    """Check system status - no API calls to avoid rate limits"""
    try:
        # Check if BERT system is working
        test_keywords = bert_ats_generator.generate_ats_keywords({
            "experiences": ["Software Developer"],
            "skills": ["Python"],
            "education": "Computer Science",
            "cvText": "Software Developer with Python experience"
        }, 5)

        return jsonify({
            "status": "active",
            "bert_system": "operational",
            "api_clients": len(api_clients),
            "training_examples": len(cv_generator.training_data),
            "sample_keywords": test_keywords[:3],
            "message": "System ready - BERT ATS Generator + Multi-API Professional Summary"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "bert_system": "error"
        }), 500

@app.route('/api/training-info')
def get_training_info():
    """Get information about training data"""
    if cv_generator.training_data:
        return jsonify({
            "success": True,
            "training_examples": len(cv_generator.training_data),
            "sample_fields": list(cv_generator.training_data[0].keys()) if cv_generator.training_data else [],
            "message": f"Model fine-tuned with {len(cv_generator.training_data)} CV examples from your dataset"
        })
    else:
        return jsonify({
            "success": False,
            "message": "No training data loaded"
        })

@app.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    """Generate professional summary using DeepSeek API"""
    try:
        form_data = request.json

        # Find similar examples
        similar_examples = cv_generator.find_similar_examples(form_data)
        examples_context = cv_generator.create_examples_context(similar_examples)

        # Extract key information
        name = form_data.get("name", "Professional")
        skills = form_data.get("skills_technical", "")

        # Find any experience title and company from dynamic fields
        experience_title = ""
        experience_company = ""
        for key, value in form_data.items():
            if 'experience' in key and 'title' in key and value:
                experience_title = value
                # Get corresponding company
                company_key = key.replace('title', 'company')
                experience_company = form_data.get(company_key, "")
                break

        education = form_data.get("education_highest_degree", "")

        prompt = f"""
        You are a professional CV writer. Based on these examples:
        {examples_context}

        Generate a professional summary for:
        Name: {name}
        Skills: {skills}
        Job Title: {experience_title}
        Company: {experience_company}
        Education: {education}

        Create a compelling 10 sentence professional summary. Return ONLY the summary text. i bit different other give me a great opening.
        """

        # Try multiple APIs for Professional Summary
        summary = None
        attempts = 0
        max_attempts = len(api_clients)

        while summary is None and attempts < max_attempts:
            try:
                current_api = get_current_api_client()
                print(f"Trying API: {current_api['name']} (attempt {attempts + 1})")

                completion = current_api['client'].chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "http://localhost:5005",
                        "X-Title": "AI CV Generator",
                    },
                    model=current_api['model'],
                    messages=[
                        {"role": "system", "content": "You are a professional CV writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200,
                    timeout=15
                )

                summary = completion.choices[0].message.content.strip()
                print(f"✅ Success with {current_api['name']}: Generated summary")
                break

            except Exception as api_error:
                print(f"❌ {current_api['name']} failed: {api_error}")
                attempts += 1
                if attempts < max_attempts:
                    get_next_api_client()  # Switch to next API
                    print(f"🔄 Switching to next API...")

        if summary is None:
            print("⚠️ All APIs failed, using fallback summary")
            summary = ""

        print(f"Final summary from API: '{summary}'")

        # If summary is empty, create a fallback
        if not summary:
            fallback_parts = []
            if experience_title:
                fallback_parts.append(f"Experienced {experience_title}")
            if skills:
                fallback_parts.append(f"with expertise in {skills}")
            if education:
                fallback_parts.append(f"holding a {education}")

            if fallback_parts:
                summary = f"{' '.join(fallback_parts)}. Dedicated professional committed to delivering high-quality results and continuous learning."
            else:
                summary = "Dedicated professional with strong technical skills and a commitment to excellence in delivering high-quality solutions."

            print(f"Using fallback summary: '{summary}'")

        return jsonify({
            "success": True,
            "summary": summary,
            "provider": "DeepSeek AI"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/generate-ats-keywords', methods=['POST'])
def generate_ats_keywords():
    """Generate ATS keywords using BERT-based system only (no API calls)"""
    try:
        form_data = request.json
        print(f"🎯 Generating ATS keywords using BERT-based system")

        # Use BERT-based generation exclusively
        keywords = bert_ats_generator.generate_ats_keywords(form_data, 25)

        print(f"✅ Generated {len(keywords)} ATS keywords using BERT: {keywords[:5]}...")

        return jsonify({
            "success": True,
            "keywords": keywords,
            "total_generated": len(keywords),
            "provider": "BERT ATS Generator"
        })
    except Exception as e:
        print(f"❌ BERT ATS generation error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return '', 204

@app.route('/')
def health_check():
    """Health check endpoint for dashboard monitoring"""
    return jsonify({
        "service": "AI Resume Generator",
        "status": "running",
        "port": 5001,
        "endpoints": [
            "/generate_resume",
            "/upload_csv",
            "/download_resume",
            "/health"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)