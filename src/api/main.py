import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from src.blockchain.chain import Blockchain

app = FastAPI(title="TrustLog API")

model = joblib.load("results/random_forest_model.joblib")
test_df = pd.read_csv("data/processed/features_test.csv")
feature_cols = [c for c in test_df.columns if c != "label"]

blockchain = Blockchain()

class LogRecord(BaseModel):
    features: List[float]
    raw_description: str = ""

@app.get("/")
def root():
    return {"message": "TrustLog API is running"}

@app.post("/ingest")
def ingest_log(record: LogRecord):
    """Accept a real 41-feature connection record and score it."""
    X = [record.features]
    pred = int(model.predict(X)[0])
    score = float(model.predict_proba(X)[0][1])
    log_data = {
        "raw_description": record.raw_description,
        "is_anomaly": pred,
        "anomaly_score": round(score, 4),
    }
    block = blockchain.add_block(log_data)
    return {"block_index": block.index, "is_anomaly": pred, "anomaly_score": round(score, 4)}

@app.get("/simulate/{count}")
def simulate_traffic(count: int = 5):
    """Pull random real rows from held-out test set and score+chain them."""
    added = []
    sample = test_df.sample(n=count)
    for _, row in sample.iterrows():
        features = row[feature_cols].tolist()
        true_label = int(row["label"])
        pred = int(model.predict([features])[0])
        score = float(model.predict_proba([features])[0][1])
        log_data = {
            "true_label": true_label,
            "predicted": pred,
            "anomaly_score": round(score, 4),
        }
        block = blockchain.add_block(log_data)
        added.append({"block_index": block.index, "predicted": pred, "true_label": true_label})
    return {"added_blocks": added}

@app.get("/logs")
def get_logs(limit: int = 20):
    recent = blockchain.chain[-limit:]
    return [b.to_dict() for b in recent]

@app.get("/anomalies")
def get_anomalies():
    return [
        b.to_dict() for b in blockchain.chain
        if b.log_data.get("is_anomaly") == 1 or b.log_data.get("predicted") == 1
    ]

@app.get("/chain/verify")
def verify_chain():
    # Re-read from disk every time so live Notepad edits are caught.
    blockchain.load_chain()
    valid, tampered_index = blockchain.is_chain_valid()
    return {"valid": valid, "tampered_block_index": tampered_index}

@app.get("/metrics")
def get_metrics():
    df = pd.read_csv("results/comparison_table.csv")
    return df.to_dict(orient="records")