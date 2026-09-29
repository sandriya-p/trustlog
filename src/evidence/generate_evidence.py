import hashlib
import json
from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/processed/v2/test_risk_scores.csv")
OUTPUT_DIR = Path("results/evidence")
OUTPUT_FILE = OUTPUT_DIR / "high_risk_evidence.json"


def main():
    df = pd.read_csv(INPUT_FILE)

    # Select the highest-risk alert
    alert = df.nlargest(1, "risk_score").iloc[0]

    evidence = {
        "evidence_id": "TRUSTLOG-HIGH-RISK-001",
        "source": "TrustLog role-aware anomaly detection",
        "user": str(alert["user"]),
        "date": str(alert["date_only"]),
        "role": str(alert["Role"]),
        "prediction": int(alert["role_prediction"]),
        "anomaly_score": float(alert["role_anomaly_score"]),
        "risk_score": float(alert["risk_score"]),
        "behavior": {
            "login_hour": int(alert["login_hour"]),
            "unique_login_pcs": int(alert["unique_login_pcs"]),
            "http_event_count": int(alert["http_event_count"]),
            "unique_urls": int(alert["unique_urls"]),
        },
        "integrity": {
            "synthetic": True
        }
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write deterministic JSON so the hash can be reproduced.
    json_bytes = json.dumps(
        evidence,
        indent=2,
        sort_keys=True
    ).encode("utf-8")

    OUTPUT_FILE.write_bytes(json_bytes)

    sha256_hash = hashlib.sha256(json_bytes).hexdigest()

    print("Evidence created successfully")
    print("File:", OUTPUT_FILE)
    print("Evidence ID:", evidence["evidence_id"])
    print("User:", evidence["user"])
    print("Date:", evidence["date"])
    print("Risk score:", evidence["risk_score"])
    print("SHA-256:", sha256_hash)


if __name__ == "__main__":
    main()