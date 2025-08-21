# student_performance_prediction.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load dataset
df = pd.read_csv("student_performance_dataset.csv")

# 2. Separate features & target
X = df.drop(["Student_ID", "Final_Grade", "Performance"], axis=1)
y = df["Performance"]

# 3. Encode categorical columns
categorical_cols = ["Gender", "School_Type", "Internet_Access"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# 4. Scale numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# 6. Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Predictions
y_pred = model.predict(X_test)

# 8. Evaluation
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 9. Example Prediction
example_student = pd.DataFrame({
    "Age": [18],
    "Gender": ["Male"],
    "School_Type": ["Private"],
    "Attendance_Percentage": [88],
    "Study_Hours_Per_Day": [3.5],
    "Past_Grade": [72],
    "Assignments_Completion": [90],
    "Participation_Score": [8],
    "Internet_Access": ["Yes"]
})

# Encode example student
for col in categorical_cols:
    example_student[col] = label_encoders[col].transform(example_student[col])

# Scale example student
example_student_scaled = scaler.transform(example_student)

# Predict
pred = model.predict(example_student_scaled)
print("\nExample Student Prediction:", pred[0])
