import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest

INPUT_FILE = Path("data/processed/v2/train_employee_days.csv")
TEST_FILE = Path("data/processed/v2/test_employee_days.csv")
MODEL_DIR = Path("results/v2_role_models")
OUTPUT_FILE = Path("data/processed/v2/test_role_aware_predictions.csv")

MODEL_DIR.mkdir(parents=True, exist_ok=True)

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

print("Loading training data...")
train = pd.read_csv(INPUT_FILE)

print("Loading test data...")
test = pd.read_csv(TEST_FILE)

results = []

roles = train["Role"].dropna().unique()

print("\nTraining role-aware models...")

for role in roles:
    train_role = train[train["Role"] == role].copy()
    test_role = test[test["Role"] == role].copy()

    if len(train_role) < 100:
        print(f"Skipping {role}: insufficient training rows")
        continue

    print(
        f"{role}: "
        f"training={len(train_role)}, "
        f"test={len(test_role)}"
    )

    X_train = train_role[FEATURES]

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train)

    safe_name = (
        str(role)
        .replace(" ", "_")
        .replace("/", "_")
    )

    model_file = MODEL_DIR / f"{safe_name}.joblib"
    joblib.dump(model, model_file)

    if len(test_role) == 0:
        continue

    X_test = test_role[model.feature_names_in_]

    test_role["role_prediction"] = model.predict(X_test)
    test_role["role_anomaly_score"] = model.decision_function(X_test)

    results.append(test_role)

if results:
    final_results = pd.concat(results, ignore_index=True)

    final_results.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nRole-aware prediction completed.")
    print("Output:", OUTPUT_FILE)
    print("Rows:", len(final_results))

    print("\nOverall results:")
    print(
        final_results["role_prediction"]
        .value_counts()
        .to_string()
    )

    print("\nAnomaly rate:")
    print(
        round(
            (final_results["role_prediction"] == -1).mean() * 100,
            2
        ),
        "%"
    )

else:
    print("No role models were generated.")