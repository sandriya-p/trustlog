import hashlib
import json
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/processed/v2/test_risk_scores.csv")
OUTPUT_DIR = Path("results/evidence")

CATEGORIES = {
    "Low": "TRUSTLOG-LOW-001",
    "Medium": "TRUSTLOG-MEDIUM-001",
    "High": "TRUSTLOG-HIGH-001",
}


def main():
    df = pd.read_csv(INPUT_FILE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for category, evidence_id in CATEGORIES.items():
        matches = df[df["risk_level"] == category]

        if matches.empty:
            raise ValueError(f"No records found for {category} risk.")

        # Select a representative row near the middle of the category.
        alert = matches.sort_values("risk_score").iloc[len(matches) // 2]

        evidence = {
            "evidence_id": evidence_id,
            "source": "TrustLog role-aware anomaly detection",
            "user": str(alert["user"]),
            "date": str(alert["date_only"]),
            "role": str(alert["Role"]),
            "prediction": int(alert["role_prediction"]),
            "anomaly_score": float(alert["role_anomaly_score"]),
            "risk_score": float(alert["risk_score"]),
            "risk_level": category,
            "behavior": {
                "login_hour": int(alert["login_hour"]),
                "unique_login_pcs": int(alert["unique_login_pcs"]),
                "http_event_count": int(alert["http_event_count"]),
                "unique_urls": int(alert["unique_urls"]),
            },
            "integrity": {"synthetic": True},
        }

        output_file = OUTPUT_DIR / f"{category.lower()}_evidence.json"

        # Never overwrite an existing evidence file.
        if output_file.exists():
            raise FileExistsError(
                f"{output_file} already exists. "
                "Stopping to protect existing evidence."
            )

        json_bytes = json.dumps(
            evidence, indent=2, sort_keys=True
        ).encode("utf-8")

        output_file.write_bytes(json_bytes)
        sha256_hash = hashlib.sha256(json_bytes).hexdigest()

        print(f"\nCategory: {category}")
        print(f"Evidence ID: {evidence_id}")
        print(f"Risk score: {evidence['risk_score']}")
        print(f"File: {output_file}")
        print(f"SHA-256: {sha256_hash}")


if __name__ == "__main__":
    main()