from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import logging
import os
import sys
sys.path.append('.')
from forcast_model import train_and_predict

# Setup
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Folders
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========================== MODEL LOADING ==========================

# Load churn model and scaler
try:
    with open('churn_model.pkl', 'rb') as f:
        churn_model, churn_scaler = pickle.load(f)
    logging.info("✅ Churn model and scaler loaded")
except Exception as e:
    logging.error(f"❌ Failed to load churn model: {e}")
    churn_model, churn_scaler = None, None

# Load product recommendation model and label encoder
try:
    with open('product_recommendation_model.pkl', 'rb') as f:
        product_model, label_encoder = pickle.load(f)
    logging.info("✅ Product recommendation model and encoder loaded")
except Exception as e:
    logging.error(f"❌ Failed to load product model: {e}")
    product_model, label_encoder = None, None

# ========================== ROUTES ==========================

@app.route('/')
def home():
    return "🚀 Combined API is running! Endpoints: /predict-churn, /metrics, /predict-file, /predict-product"

# ---------- 1. Churn Prediction ----------
@app.route('/predict-churn', methods=['POST'])
def predict_churn():
    if churn_model is None or churn_scaler is None:
        return jsonify({'error': 'Churn model not available'}), 500

    data = request.json
    required_fields = [
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

    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    try:
        input_df = pd.DataFrame([data])
        if input_df['account_status'].dtype == 'object':
            input_df['account_status'] = input_df['account_status'].astype('category').cat.codes

        scaled_input = churn_scaler.transform(input_df)
        prediction = churn_model.predict(scaled_input)[0]
        proba = churn_model.predict_proba(scaled_input)[0][1]

        result = "Churn" if prediction == 1 else "No Churn"
        percentage = proba * 100

        if percentage <= 25:
            zone = "🟢 Green"
        elif percentage <= 50:
            zone = "🔵 Blue"
        elif percentage <= 75:
            zone = "🟠 Orange"
        else:
            zone = "🔴 Red"

        return jsonify({
            "prediction": result,
            "probability": f"{percentage:.2f}%",
            "churn_zone": zone
        })

    except Exception as e:
        logging.error(f"❌ Prediction error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    try:
        df = pd.read_csv('churndata.csv')
        churn_flag = pd.to_numeric(df['churn_flag'], errors='coerce').dropna()

        total = len(churn_flag)
        churned = churn_flag.sum()
        churn_percent = (churned / total) * 100

        if churn_percent <= 25:
            zone = "🟢 Green"
        elif churn_percent <= 50:
            zone = "🔵 Blue"
        elif churn_percent <= 75:
            zone = "🟠 Orange"
        else:
            zone = "🔴 Red"

        status = "Churn" if churn_percent > 50 else "No Churn"

        return jsonify({
            "📉 Churn Percentage": f"{churn_percent:.2f}%",
            "🔮 Churn Status": status,
            "🟢 Churn Zone": zone
        })

    except Exception as e:
        logging.error(f"❌ Metrics error: {e}")
        return jsonify({"error": "Metrics calculation failed"}), 500

# ---------- 2. File Upload Prediction ----------
@app.route('/predict-file', methods=['POST'])
def predict_file():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        df = pd.read_csv(path)

        # Call the actual forecast model
        results = train_and_predict(df)

        return jsonify(results)

    except Exception as e:
        logging.error(f"❌ File prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# ---------- 3. Product Recommendation ----------
@app.route('/predict-product', methods=['POST'])
def predict_product():
    if product_model is None or label_encoder is None:
        return jsonify({'error': 'Product model not available'}), 500

    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        pred_encoded = product_model.predict(df)
        pred_label = label_encoder.inverse_transform(pred_encoded)

        return jsonify({'predicted_product': pred_label[0]})

    except Exception as e:
        logging.error(f"❌ Product prediction error: {e}")
        return jsonify({'error': str(e)}), 400

# ========================== START SERVER ==========================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
