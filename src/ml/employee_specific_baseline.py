import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

TRAIN_PATH = r"data\processed\v2\train_employee_days.csv"
TEST_PATH = r"data\processed\v2\test_employee_days.csv"
OUTPUT_PATH = r"data\processed\v2\test_employee_specific_predictions.csv"

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
    "unique_urls",
    "unique_http_pcs",
    "after_hours_device_connect",
    "after_hours_http",
    "login_time_deviation",
    "http_activity_deviation",
]

print("Loading training data...")
train = pd.read_csv(TRAIN_PATH)

print("Loading test data...")
test = pd.read_csv(TEST_PATH)

print(f"Training rows: {len(train)}")
print(f"Test rows: {len(test)}")
print(f"Employees in training data: {train['user'].nunique()}")
print(f"Employees in test data: {test['user'].nunique()}")

results = []

print("\nTraining employee-specific models...")

for user, train_group in train.groupby("user"):

    test_group = test[test["user"] == user].copy()

    if test_group.empty:
        continue

    # Need enough historical observations to build a personal model
    if len(train_group) < 10:
        test_group["employee_prediction"] = 1
        test_group["employee_anomaly_score"] = 0.0
        results.append(test_group)
        continue

    X_train = train_group[FEATURES].fillna(0)
    X_test = test_group[FEATURES].fillna(0)

    # Standardize using training data only
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )

    model.fit(X_train_scaled)

    test_group["employee_prediction"] = model.predict(X_test_scaled)

    # Higher value = more anomalous
    test_group["employee_anomaly_score"] = -model.score_samples(
        X_test_scaled
    )

    results.append(test_group)

    if len(results) % 100 == 0:
        print(f"Processed {len(results)} employees...")

result_df = pd.concat(results, ignore_index=True)

result_df.to_csv(OUTPUT_PATH, index=False)

print("\nEmployee-specific baseline completed.")
print(f"Output: {OUTPUT_PATH}")
print(f"Rows: {len(result_df)}")

print("\nPrediction counts:")
print(result_df["employee_prediction"].value_counts())

anomaly_rate = (
    result_df["employee_prediction"].eq(-1).mean() * 100
)

print(f"\nAnomaly rate: {anomaly_rate:.2f} %")

print(
    "\nNote: Anomalies represent behavioral deviations, "
    "not confirmed attacks."
)