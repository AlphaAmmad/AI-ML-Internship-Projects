from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random
import time

# === SETUP === #
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Load job dataset
try:
    df_jobs = pd.read_csv("job_postings.csv")
    df_jobs.fillna('', inplace=True)
    print(f"✅ Loaded {len(df_jobs)} job postings")
except Exception as e:
    print(f"⚠️ Error loading job dataset: {e}")
    df_jobs = pd.DataFrame()

# Load Sentence-BERT model for semantic matching
try:
    from sentence_transformers import SentenceTransformer, util
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Sentence-BERT model loaded successfully")

    # Precompute SBERT job embeddings if we have jobs
    if not df_jobs.empty:
        def build_job_text(row):
            return f"{row['title']} {row['job_description']} {row['required_skills']} {row['preferred_soft_skills']} {row['technologies_used']} {row['industry']} {row['required_education']} {row['employment_type']} {row['shift_timings']} {row['job_tags']} {row['experience_required']}"

        df_jobs['job_text'] = df_jobs.apply(build_job_text, axis=1)
        sbert_embeddings = sbert_model.encode(df_jobs['job_text'].tolist(), convert_to_tensor=True)
        print("✅ Job embeddings computed successfully")
    else:
        sbert_embeddings = None

except Exception as e:
    print(f"⚠️ Error loading Sentence-BERT: {e}")
    sbert_model = None
    sbert_embeddings = None

# Demo data for fallback
DEMO_JOBS = [
    {"job_id": "j001", "title": "Senior Software Engineer", "company": "TechCorp Solutions", "location": "Karachi, Pakistan", "similarity_score": 0.92},
    {"job_id": "j002", "title": "Full Stack Developer", "company": "InnovateTech", "location": "Lahore, Pakistan", "similarity_score": 0.87},
    {"job_id": "j003", "title": "Python Developer", "company": "DataSoft Pvt Ltd", "location": "Islamabad, Pakistan", "similarity_score": 0.84},
    {"job_id": "j004", "title": "Machine Learning Engineer", "company": "AI Solutions Inc", "location": "Remote", "similarity_score": 0.81},
    {"job_id": "j005", "title": "DevOps Engineer", "company": "CloudTech Systems", "location": "Faisalabad, Pakistan", "similarity_score": 0.78}
]

TECH_SKILLS = ["Python", "JavaScript", "React", "Node.js", "Django", "Flask", "Docker", "Kubernetes", "AWS", "Git", "SQL", "MongoDB", "Machine Learning", "Data Analysis", "REST APIs", "GraphQL"]
SOFT_SKILLS = ["Leadership", "Communication", "Problem Solving", "Teamwork", "Time Management", "Adaptability", "Critical Thinking", "Creativity"]

# === HELPERS === #
def clean_keywords(s):
    return [word.strip().lower() for word in s.split(',') if word.strip() != '']

# === ROUTES === #

@app.route('/recommend_advice', methods=['POST'])
def recommend_advice():
    """AI Career Advice endpoint"""
    try:
        # Simulate processing time
        time.sleep(2)

        data = request.get_json()
        degree = data.get('degree', '')
        majors = data.get('majors', '')
        skills = data.get('skills', '')

        # Generate career advice based on input
        if 'computer' in degree.lower() or 'software' in degree.lower():
            job_title = "Senior Software Engineer"
        elif 'data' in degree.lower() or 'machine learning' in skills.lower():
            job_title = "Data Scientist"
        elif 'business' in degree.lower() or 'mba' in degree.lower():
            job_title = "Product Manager"
        else:
            job_title = "Software Developer"

        # Select relevant skills
        selected_tech = random.sample(TECH_SKILLS, 8)
        selected_soft = random.sample(SOFT_SKILLS, 6)

        career_advice = f"""Based on your {degree} background and skills in {skills}, you're well-positioned for a career as a {job_title}.

The tech industry is rapidly evolving, and professionals with your educational foundation are in high demand. Focus on building expertise in modern technologies and frameworks that align with current market trends.

Your combination of technical knowledge and problem-solving abilities makes you an ideal candidate for roles that require both analytical thinking and practical implementation. Consider specializing in emerging areas like cloud computing, artificial intelligence, or full-stack development to maximize your career opportunities.

Continuous learning and staying updated with industry best practices will be key to your long-term success in this field."""

        return jsonify({
            "recommended_job_title": job_title,
            "technical_skills_to_learn": selected_tech,
            "soft_skills_to_develop": selected_soft,
            "career_advice": career_advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs():
    """AI Job Recommendations endpoint"""
    try:
        # Simulate processing time
        time.sleep(1.5)

        data = request.get_json()

        # Try semantic matching if models are available
        if sbert_model and sbert_embeddings is not None and not df_jobs.empty:
            user_text = (
                f"{data.get('preferred_roles', '')} {data.get('skills', '')} {data.get('soft_skills', '')} "
                f"{data.get('tools_technologies', '')} {data.get('industry_preference', '')} "
                f"{data.get('job_type_preference', '')} {data.get('preferred_shift', '')} {data.get('experience_required', '')}"
            )

            user_embedding = sbert_model.encode(user_text, convert_to_tensor=True)
            cosine_scores = util.cos_sim(user_embedding, sbert_embeddings)[0]
            df_jobs['similarity_score'] = cosine_scores.cpu().numpy()
            filtered_jobs = df_jobs[df_jobs['similarity_score'] > 0.60]
            top_jobs = filtered_jobs.sort_values(by='similarity_score', ascending=False).head(5)

            result = top_jobs[['job_id', 'title', 'company', 'location', 'similarity_score']].to_dict(orient='records')
            return jsonify(result)

        else:
            # Fallback to demo data
            preferred_roles = data.get('preferred_roles', '')
            skills = data.get('skills', '')

            # Filter and customize jobs based on input
            filtered_jobs = []
            for job in DEMO_JOBS:
                # Simple matching logic for demo
                if any(role.lower() in job['title'].lower() for role in preferred_roles.split(',')):
                    job['similarity_score'] = min(0.95, job['similarity_score'] + 0.05)

                if any(skill.lower() in job['title'].lower() for skill in skills.split(',')):
                    job['similarity_score'] = min(0.98, job['similarity_score'] + 0.03)

                filtered_jobs.append(job)

            # Sort by similarity score and return top matches
            filtered_jobs.sort(key=lambda x: x['similarity_score'], reverse=True)
            return jsonify(filtered_jobs[:5])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🩺 Health Check
@app.route('/')
def health():
    return jsonify({
        "service": "Unified Job Recommendation API",
        "status": "running",
        "endpoints": ["/recommend_advice", "/recommend_jobs"],
        "models": {
            "semantic_based": "Sentence-BERT (all-MiniLM-L6-v2)" if sbert_model else "Demo Mode",
            "jobs_loaded": len(df_jobs) if not df_jobs.empty else 0,
            "embeddings_ready": sbert_embeddings is not None
        }
    })

# === START APP === #
if __name__ == '__main__':
    print("🚀 Starting Job Recommendation API...")
    print("📡 API available at: http://localhost:3000")
    print("🔗 Endpoints:")
    print("   - Career Advice: POST /recommend_advice")
    print("   - Job Recommendations: POST /recommend_jobs")
    print("   - Health Check: GET /")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=3000) 