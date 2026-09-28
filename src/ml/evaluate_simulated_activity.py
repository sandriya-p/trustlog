import pandas as pd
import joblib
from pathlib import Path


INPUT_FILE = Path(
    r"data\processed\v2\simulated_activity.csv"
)

MODEL_DIR = Path(
    r"results\v2_role_models"
)

OUTPUT_FILE = Path(
    r"data\processed\v2\simulated_detection_results.csv"
)

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


print("Loading simulated activity...")
df = pd.read_csv(INPUT_FILE)

print(f"Simulated records: {len(df)}")

results = []

for role in df["Role"].dropna().unique():

    role_data = df[df["Role"] == role].copy()

    safe_name = (
        str(role)
        .replace(" ", "_")
        .replace("/", "_")
    )

    model_file = MODEL_DIR / f"{safe_name}.joblib"

    if not model_file.exists():
        print(f"Skipping {role}: model not found")
        continue

    model = joblib.load(model_file)

    X = role_data[FEATURES]

    role_data["role_prediction"] = model.predict(X)
    role_data["role_anomaly_score"] = (
        model.decision_function(X)
    )

    results.append(role_data)


if not results:
    print("No simulated records could be evaluated.")
    raise SystemExit


final_results = pd.concat(
    results,
    ignore_index=True
)

final_results.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n=== SIMULATED DETECTION RESULTS ===")

print(f"Evaluated records: {len(final_results)}")

print("\nResults by scenario:")

summary = (
    final_results
    .groupby("scenario")["role_prediction"]
    .agg(
        total="count",
        anomalies=lambda x: (x == -1).sum()
    )
)

summary["anomaly_rate_percent"] = (
    summary["anomalies"]
    / summary["total"]
    * 100
)

print(summary.to_string())


print("\nOverall prediction counts:")
print(
    final_results["role_prediction"]
    .value_counts()
    .to_string()
)

print("\nOutput:")
print(OUTPUT_FILE)

print(
    "\nNote: These are synthetic behavioral scenarios, "
    "not confirmed attacks."
)