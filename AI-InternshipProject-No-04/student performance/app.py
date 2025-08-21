from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# Global variables to store model and preprocessors
model = None
scaler = None
label_encoders = {}

def train_and_save_model():
    """Train the model and save it along with preprocessors"""
    global model, scaler, label_encoders
    
    # Load dataset
    df = pd.read_csv("student_performance_dataset.csv")
    
    # Separate features & target
    X = df.drop(["Student_ID", "Final_Grade", "Performance"], axis=1)
    y = df["Performance"]
    
    # Encode categorical columns
    categorical_cols = ["Gender", "School_Type", "Internet_Access"]
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    
    # Scale numeric features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model and preprocessors
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('label_encoders.pkl', 'wb') as f:
        pickle.dump(label_encoders, f)
    
    print("Model trained and saved successfully!")

def load_model():
    """Load the trained model and preprocessors"""
    global model, scaler, label_encoders
    
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Model files not found. Training new model...")
        train_and_save_model()

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions"""
    try:
        data = request.json
        
        # Create DataFrame from input data
        student_data = pd.DataFrame({
            "Age": [data['age']],
            "Gender": [data['gender']],
            "School_Type": [data['school_type']],
            "Attendance_Percentage": [data['attendance_percentage']],
            "Study_Hours_Per_Day": [data['study_hours_per_day']],
            "Past_Grade": [data['past_grade']],
            "Assignments_Completion": [data['assignments_completion']],
            "Participation_Score": [data['participation_score']],
            "Internet_Access": [data['internet_access']]
        })
        
        # Encode categorical variables
        categorical_cols = ["Gender", "School_Type", "Internet_Access"]
        for col in categorical_cols:
            student_data[col] = label_encoders[col].transform(student_data[col])
        
        # Scale the data
        student_data_scaled = scaler.transform(student_data)
        
        # Make prediction
        prediction = model.predict(student_data_scaled)[0]
        prediction_proba = model.predict_proba(student_data_scaled)[0]
        
        # Get confidence scores
        confidence = max(prediction_proba) * 100
        
        return jsonify({
            'prediction': prediction,
            'confidence': round(confidence, 2),
            'probabilities': {
                'Fail': round(prediction_proba[0] * 100, 2),
                'Pass': round(prediction_proba[1] * 100, 2)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the model"""
    try:
        # Load dataset to get some stats
        df = pd.read_csv("student_performance_dataset.csv")
        
        return jsonify({
            'total_students': len(df),
            'pass_rate': round((df['Performance'] == 'Pass').mean() * 100, 2),
            'fail_rate': round((df['Performance'] == 'Fail').mean() * 100, 2),
            'features': [
                'Age', 'Gender', 'School_Type', 'Attendance_Percentage',
                'Study_Hours_Per_Day', 'Past_Grade', 'Assignments_Completion',
                'Participation_Score', 'Internet_Access'
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/dataset-stats', methods=['GET'])
def dataset_stats():
    """Get dataset statistics"""
    try:
        df = pd.read_csv("student_performance_dataset.csv")
        
        stats = {
            'age_stats': {
                'min': int(df['Age'].min()),
                'max': int(df['Age'].max()),
                'mean': round(df['Age'].mean(), 1)
            },
            'attendance_stats': {
                'min': int(df['Attendance_Percentage'].min()),
                'max': int(df['Attendance_Percentage'].max()),
                'mean': round(df['Attendance_Percentage'].mean(), 1)
            },
            'study_hours_stats': {
                'min': round(df['Study_Hours_Per_Day'].min(), 1),
                'max': round(df['Study_Hours_Per_Day'].max(), 1),
                'mean': round(df['Study_Hours_Per_Day'].mean(), 1)
            },
            'gender_distribution': df['Gender'].value_counts().to_dict(),
            'school_type_distribution': df['School_Type'].value_counts().to_dict(),
            'internet_access_distribution': df['Internet_Access'].value_counts().to_dict()
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Load or train model on startup
    load_model()
    app.run(debug=True, host='0.0.0.0', port=5001)
