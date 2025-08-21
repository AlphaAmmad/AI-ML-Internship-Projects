import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import pickle

# Load data
df = pd.read_csv('/home/shayan/Desktop/Ammad stuff/all/AI-InternshipProjectNo1/backend/customer_recommendations_better.csv')

# Features and target
features = [
    'region',
    'gender',
    'user_age_group',
    'user_preferences',
    'season',
    'product_keywords',
    'previous_buy'
]
target = 'suggested_product'

# Drop missing data
df = df[features + [target]].dropna()

# Split X and y
X = df[features]
y = df[target]

# Encode labels (for output class)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Preprocessing pipeline (OneHot for all features)
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), features)
])

# XGBoost model inside pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'))
])

# GridSearch parameters
param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [3, 5, 7],
    'classifier__learning_rate': [0.01, 0.1, 0.3]
}

# Grid Search with CV
grid_search = GridSearchCV(pipeline, param_grid, cv=3, verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# Evaluate
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("✅ Best Hyperparameters:", grid_search.best_params_)
print("🎯 Model Accuracy:", round(accuracy * 100, 2), "%")
print("\n📊 Classification Report:\n", classification_report(label_encoder.inverse_transform(y_test), label_encoder.inverse_transform(y_pred)))

# Save model and label encoder
with open('product_recommendation_model.pkl', 'wb') as f:
    pickle.dump((best_model, label_encoder), f)

print("✅ Model and encoder saved as product_recommendation_model.pkl")
