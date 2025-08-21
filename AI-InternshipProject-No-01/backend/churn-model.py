import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle

# Load data
df = pd.read_csv('/home/shayan/Desktop/Ammad stuff/all/AI-InternshipProjectNo1/backend/churndata.csv')

# Selected Features
features = [
    'customer_tenure',
    'number_of_services_or_products',
    'average_monthly_usage',
    'days_since_last_interaction',
    'complaints_resolved_ratio',
    'total_spent',
    'average_transaction_value',
    'discount_or_offer_received',
    'account_status'
]
target = 'churn_flag'

# Clean and prepare data
df = df[features + [target]].dropna()

# Encode categorical if needed
if df['account_status'].dtype == 'object':
    df['account_status'] = LabelEncoder().fit_transform(df['account_status'])

# Split
X = df[features]
y = df[target]

# Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_scaled, y)

# Save both model and scaler
with open('churn_model.pkl', 'wb') as f:
    pickle.dump((model, scaler), f)

print("✅ Model and scaler saved as churn_model.pkl")