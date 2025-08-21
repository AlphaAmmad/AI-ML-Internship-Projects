# AI Internship Projects Collection

This repository contains four comprehensive AI internship projects, each demonstrating different aspects of machine learning, data science, and web development. The projects range from business analytics to computer vision applications.

## 📁 Project Structure

```
project/
├── AI-InternshipProject-No-01/    # Business Analytics Suite
├── AI-InternshipProject-No-02/    # Career & Job Platform
├── AI-InternshipProject-No-03/    # Business Intelligence Tools
├── AI-InternshipProject-No-04/    # Educational & Vision Systems
└── README.md
```

## 🚀 Projects Overview

### Project 01: Business Analytics Suite
**Location:** `AI-InternshipProject-No-01/`

A comprehensive business analytics platform with customer churn prediction, sales forecasting, and product recommendation systems.

**Features:**
- Customer Churn Prediction
- Sales Forecasting
- Product Recommendation Engine
- Interactive Web Dashboard

**Tech Stack:**
- Backend: Python, Flask, Flask-CORS
- ML Libraries: scikit-learn, XGBoost, pandas, numpy
- Frontend: HTML, CSS, JavaScript

### Project 02: Career & Job Platform
**Location:** `AI-InternshipProject-No-02/`

An AI-powered career platform featuring resume generation and job recommendation systems.

**Features:**
- AI Resume Generator (OpenAI integration)
- Job Recommendation System
- Skills-based matching
- Interactive career advice

**Tech Stack:**
- Backend: Python, Flask
- AI: OpenAI API, sentence-transformers, PyTorch
- ML: scikit-learn, NLTK
- Frontend: HTML, CSS, JavaScript

### Project 03: Business Intelligence Tools
**Location:** `AI-InternshipProject-No-03/`

Advanced business intelligence suite with meeting summarization, cross-sell prediction, and financial forecasting.

**Features:**
- AI Meeting Summarizer (Audio processing)
- Cross-sell/Upsell Prediction
- Monthly Financial Forecasting
- Data visualization dashboards

**Tech Stack:**
- Backend: Python, Flask
- Data Science: pandas, numpy, scikit-learn
- Visualization: matplotlib, seaborn, plotly
- Audio Processing: Speech recognition libraries

### Project 04: Educational & Vision Systems
**Location:** `AI-InternshipProject-No-04/`

Educational technology and computer vision applications including attendance systems and performance analytics.

**Features:**
- Face Recognition Attendance System
- Course Recommendation Engine
- Eye Closure Detection (Driver safety)
- Student Performance Prediction

**Tech Stack:**
- Backend: Python, Flask, Flask-CORS
- Computer Vision: OpenCV, dlib
- ML: scikit-learn, pandas, numpy
- Frontend: HTML, CSS, JavaScript

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### General Setup Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd project
```

2. **Set up virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies for each project:**

Navigate to each project directory and install requirements:

```bash
# Project 01
cd AI-InternshipProject-No-01/backend
pip install -r req.txt

# Project 02 - Job Recommendation
cd ../../AI-InternshipProject-No-02/job\ recommendation
pip install -r req.txt

# Project 02 - Resume Generator
cd ../AI\ resume\ Generator
pip install openai flask jinja2 nltk scikit-learn numpy

# Project 03 - Monthly Forecast
cd ../../AI-InternshipProject-No-03/monthlyforcast
pip install -r requirements.txt

# Project 04 - Student Performance
cd ../../AI-InternshipProject-No-04/student\ performance
pip install -r requirements.txt
```

### Project-Specific Setup

#### Project 01: Business Analytics Suite
```bash
cd AI-InternshipProject-No-01/backend
python app.py
```
Access at: `http://localhost:5000`

#### Project 02: Career Platform
For Resume Generator:
```bash
cd AI-InternshipProject-No-02/AI\ resume\ Generator
# Add your OpenAI API key to apikey.txt
python app.py
```

For Job Recommendation:
```bash
cd AI-InternshipProject-No-02/job\ recommendation
python app.py
```

#### Project 03: Business Intelligence
```bash
cd AI-InternshipProject-No-03/monthlyforcast
python app.py
```

#### Project 04: Educational Systems
```bash
cd AI-InternshipProject-No-04/student\ performance
python app.py
```

## 📋 Configuration

### API Keys Required
- **Project 02 (Resume Generator):** OpenAI API key in `AI-InternshipProject-No-02/AI resume Generator/apikey.txt`

### Data Files
Each project includes sample datasets. Ensure the following files are present:
- Project 01: `churndata.csv`, `retail_sales_data.csv`
- Project 02: `cv_dataset.csv`, `job_postings.csv`
- Project 03: `company_expenses_non_linear.csv`
- Project 04: `student_performance_dataset.csv`

## 🔧 Usage

Each project runs independently on different ports. Start the Flask applications and access the web interfaces through your browser. Most projects include:

- Interactive web dashboards
- File upload capabilities
- Real-time predictions
- Data visualization
- Model training interfaces

## 📊 Features by Project

| Feature | Project 01 | Project 02 | Project 03 | Project 04 |
|---------|------------|------------|------------|------------|
| Machine Learning | ✅ | ✅ | ✅ | ✅ |
| Web Interface | ✅ | ✅ | ✅ | ✅ |
| Data Upload | ✅ | ✅ | ✅ | ✅ |
| Visualization | ✅ | ❌ | ✅ | ❌ |
| Computer Vision | ❌ | ❌ | ❌ | ✅ |
| NLP/AI | ❌ | ✅ | ✅ | ❌ |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational purposes as part of an AI internship program.


