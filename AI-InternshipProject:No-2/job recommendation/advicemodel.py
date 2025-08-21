import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
import joblib
import nltk
nltk.download('punkt')

# Device setup
device = torch.device("cpu")

# Load BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert = BertModel.from_pretrained("bert-base-uncased").to(device)

# Skill cleaner
def clean_keywords(s):
    return [word.strip().lower() for word in s.split(',') if word.strip() != '']

# Embedding function
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True).to(device)
    with torch.no_grad():
        outputs = bert(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

# Load full dataset
df = pd.read_csv("job_postings.csv")
df.fillna('', inplace=True)

# Encode labels globally
label_encoder = LabelEncoder()
df['encoded_title'] = label_encoder.fit_transform(df['title'])

# Save label encoder
joblib.dump(label_encoder, "label_encoder.pkl")

# Prepare classes once
all_classes = np.unique(df['encoded_title'])

# Model & binarizer
model = SGDClassifier(loss="log_loss", max_iter=1000)
mlb = MultiLabelBinarizer()

# Save chunk size
CHUNK_SIZE = 1000

# Step-by-step training
for start in range(0, len(df), CHUNK_SIZE):
    end = start + CHUNK_SIZE
    chunk = df.iloc[start:end].copy()

    # Combine and clean skills
    chunk['combined_keywords'] = chunk['required_skills'] + ',' + chunk['technologies_used'] + ',' + chunk['job_tags']
    chunk['keyword_list'] = chunk['combined_keywords'].apply(clean_keywords)

    # Fit or transform skills
    if start == 0:
        skill_matrix = mlb.fit_transform(chunk['keyword_list'])
        joblib.dump(mlb, "mlb.pkl")  # Save only once
    else:
        skill_matrix = mlb.transform(chunk['keyword_list'])

    # BERT embeddings
    print(f"🔄 Processing chunk {start}–{end}...")
    chunk['bert_desc'] = chunk['job_description'].apply(get_bert_embedding)
    X_bert = np.stack(chunk['bert_desc'].values)
    X = np.hstack([X_bert, skill_matrix])
    y = chunk['encoded_title'].values

    # Train with partial_fit
    if start == 0:
        model.partial_fit(X, y, classes=all_classes)
    else:
        model.partial_fit(X, y)

    print(f"✅ Trained chunk: {start}–{min(end, len(df))}")

# Save final model
joblib.dump(model, "job_model.pkl")
print("✅ Model saved as job_model.pkl")
