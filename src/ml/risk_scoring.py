import pandas as pd
import joblib
from pathlib import Path
import numpy as np

TRAIN_FILE = Path("data/processed/v2/train_employee_days.csv")
TEST_FILE = Path("data/processed/v2/test_employee_days.csv")
PRED_FILE = Path("data/processed/v2/test_role_aware_predictions.csv")

MODEL_DIR = Path("results/v2_role_models")
OUTPUT_FILE = Path("data/processed/v2/test_risk_scores.csv")

FEATURES = [
    "login_count",
    "login_hour",
    "after_hours_login",
    "total_session_hours",
    "session_count",
    "unique_login_pcs",
    "device_connect_count",
    "device_disconnect_count",
    "unique_device_pcs",
    "http_event_count",
    "unique_http_pcs",
    "after_hours_device_connect",
    "after_hours_http",
    "login_time_deviation",
    "http_activity_deviation",
    "employee_active_status",
]

train = pd.read_csv(TRAIN_FILE)
test = pd.read_csv(TEST_FILE)
pred = pd.read_csv(PRED_FILE)

pred["risk_score"] = np.nan
pred["risk_level"] = np.nan

roles = train["Role"].dropna().unique()

for role in roles:
    model_file = MODEL_DIR / (
        str(role).replace(" ", "_").replace("/", "_") + ".joblib"
    )

    model = joblib.load(model_file)

    train_role = train[train["Role"] == role]
    test_mask = pred["Role"] == role

    if test_mask.sum() == 0:
        continue

    # Historical 2010 anomaly-score distribution
    train_scores = model.decision_function(
        train_role[model.feature_names_in_]
    )

    # 2011 anomaly scores
    test_scores = pred.loc[
        test_mask, "role_anomaly_score"
    ].values

    # Lower model score = more unusual.
    # Convert to a 0–100 relative risk percentile.
    risk = np.array([
        (train_scores >= score).mean() * 100
        for score in test_scores
    ])

    pred.loc[test_mask, "risk_score"] = np.round(risk, 2)
def get_risk_level(score):
    if pd.isna(score):
        return "Unknown"
    elif score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


pred["risk_level"] = pred["risk_score"].apply(get_risk_level)
pred.to_csv(OUTPUT_FILE, index=False)

print("Risk scoring completed.")
print("Saved:", OUTPUT_FILE)
print("Rows:", len(pred))
print("Missing risk scores:", pred["risk_score"].isna().sum())
print(
    "Risk range:",
    pred["risk_score"].min(),
    "to",
    pred["risk_score"].max()
)