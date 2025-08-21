from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def dashboard():
    """Serve the main dashboard"""
    return send_from_directory('.', 'index.html')

@app.route('/advice.html')
def advice():
    """Serve the AI advice page"""
    return send_from_directory('.', 'advice.html')

@app.route('/jobs.html')
def jobs():
    """Serve the AI jobs page"""
    return send_from_directory('.', 'jobs.html')

@app.route('/styles.css')
def styles():
    """Serve the CSS file"""
    return send_from_directory('.', 'styles.css', mimetype='text/css')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        "service": "Job Recommendation Frontend",
        "status": "running",
        "port": 3000,
        "pages": [
            {"name": "Dashboard", "url": "/"},
            {"name": "AI Career Advice", "url": "/advice.html"},
            {"name": "AI Job Recommendations", "url": "/jobs.html"}
        ]
    }

if __name__ == '__main__':
    print("🚀 Starting Job Recommendation Frontend Server...")
    print("📱 Dashboard available at: http://localhost:3000")
    print("💡 AI Career Advice: http://localhost:3000/advice.html")
    print("💼 AI Job Recommendations: http://localhost:3000/jobs.html")
    print("🔗 Make sure backend API is running on port 5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=3000)
