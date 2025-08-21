# Student Performance Predictor

A web application that predicts student academic performance using machine learning.

## Features

- **Machine Learning Model**: Random Forest classifier trained on student data
- **Web Interface**: Clean, responsive HTML/CSS/JavaScript frontend
- **REST API**: Flask backend with multiple endpoints
- **Real-time Predictions**: Instant performance predictions with confidence scores
- **Data Visualization**: Interactive results with probability distributions

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Open Browser**:
   Navigate to `http://localhost:5000`

## API Endpoints

- `GET /` - Main web interface
- `POST /api/predict` - Make predictions
- `GET /api/model-info` - Get model information
- `GET /api/dataset-stats` - Get dataset statistics

## Input Features

- **Age**: Student age (15-25)
- **Gender**: Male/Female
- **School Type**: Public/Private
- **Attendance Percentage**: 0-100%
- **Study Hours Per Day**: 0-12 hours
- **Past Grade**: Previous academic score (0-100)
- **Assignments Completion**: Percentage of completed assignments
- **Participation Score**: Class participation (1-10)
- **Internet Access**: Yes/No

## Model Performance

The Random Forest model achieves approximately 71% accuracy on the test dataset.

## File Structure

```
├── app.py                          # Flask application
├── model.py                        # Original model training script
├── student_performance_dataset.csv # Training data
├── templates/
│   └── index.html                  # Web interface
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Usage

1. Fill in the student information form
2. Click "Predict Performance"
3. View the prediction result with confidence score
4. See probability breakdown for Pass/Fail outcomes
