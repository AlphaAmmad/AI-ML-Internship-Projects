from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Global variables for model
model = None
encoder = None
df = None

def load_model():
    """Load and train the model exactly like MODEL.PY"""
    global model, encoder, df
    
    # Load dataset (exactly from your MODEL.PY)
    df = pd.read_csv("course_recommendation_data.csv")
    
    # Features and target (exactly from your MODEL.PY)
    features = ['Age', 'Education_Level', 'Goal', 'Preferred_Category', 'Subcategory']
    target = 'Course_Name'
    
    # Encode features (exactly from your MODEL.PY)
    encoder = OneHotEncoder()
    X = encoder.fit_transform(df[features])
    y = df[target]
    
    # Initialize model (exactly from your MODEL.PY)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    print("Model loaded successfully!")

def recommend_courses_classification(user_input, top_n=10):
    """Your exact recommendation function from MODEL.PY"""
    user_df = pd.DataFrame([user_input])
    user_encoded = encoder.transform(user_df)
    proba = model.predict_proba(user_encoded)[0]
    course_labels = model.classes_
    
    top_indices = np.argsort(proba)[::-1][:top_n]
    top_courses = []

    for i in top_indices:
        course_name = course_labels[i]
        confidence = round(proba[i] * 100, 2)

        # Filter out courses with confidence < 10%
        if confidence < 10:
            continue

        # Get course details from dataset
        course_info = df[df['Course_Name'] == course_name].iloc[0]

        course_data = {
            'id': int(course_info['User_ID']),
            'course': course_name,
            'category': course_info['Preferred_Category'],
            'subcategory': course_info['Subcategory'],
            'rating': float(course_info['Rating']),
            'confidence': confidence,
            'age': int(course_info['Age']),
            'education': course_info['Education_Level'],
            'goal': course_info['Goal']
        }
        top_courses.append(course_data)
    
    return top_courses

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    """API endpoint for recommendations"""
    try:
        data = request.json
        
        # Prepare user input exactly like your MODEL.PY
        user_input = {
            'Age': int(data['age']),
            'Education_Level': data['education'],
            'Goal': data['goal'],
            'Preferred_Category': data['category'],
            'Subcategory': data['subcategory']
        }
        
        # Use your exact recommendation function (get more candidates to filter)
        recommendations = recommend_courses_classification(user_input, top_n=30)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'Model is running!', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("Loading your MODEL.PY...")
    load_model()
    print("Starting API server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
