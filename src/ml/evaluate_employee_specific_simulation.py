import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pathlib import Path


TRAIN_PATH = Path(
    r"data\processed\v2\train_employee_days.csv"
)

SIMULATED_PATH = Path(
    r"data\processed\v2\simulated_activity.csv"
)

OUTPUT_PATH = Path(
    r"data\processed\v2\employee_specific_simulated_results.csv"
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
    "unique_urls",
    "unique_http_pcs",
    "after_hours_device_connect",
    "after_hours_http",
    "login_time_deviation",
    "http_activity_deviation",
]


print("Loading training data...")
train = pd.read_csv(TRAIN_PATH)

print("Loading simulated activity...")
simulated = pd.read_csv(SIMULATED_PATH)

print(f"Training rows: {len(train)}")
print(f"Simulated rows: {len(simulated)}")
print(f"Training employees: {train['user'].nunique()}")
print(f"Simulated employees: {simulated['user'].nunique()}")


results = []

print("\nApplying employee-specific models...")


for user, simulated_group in simulated.groupby("user"):

    train_group = train[train["user"] == user]

    simulated_group = simulated_group.copy()

    if train_group.empty:
        simulated_group["employee_prediction"] = 1
        simulated_group["employee_anomaly_score"] = 0.0
        results.append(simulated_group)
        continue

    if len(train_group) < 10:
        simulated_group["employee_prediction"] = 1
        simulated_group["employee_anomaly_score"] = 0.0
        results.append(simulated_group)
        continue

    X_train = train_group[FEATURES].fillna(0)
    X_simulated = simulated_group[FEATURES].fillna(0)

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_simulated_scaled = scaler.transform(X_simulated)

    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )

    model.fit(X_train_scaled)

    simulated_group["employee_prediction"] = (
        model.predict(X_simulated_scaled)
    )

    simulated_group["employee_anomaly_score"] = (
        -model.score_samples(X_simulated_scaled)
    )

    results.append(simulated_group)


result_df = pd.concat(
    results,
    ignore_index=True
)


result_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\n=== EMPLOYEE-SPECIFIC SIMULATED RESULTS ===")

print(f"Evaluated records: {len(result_df)}")

print("\nResults by scenario:")

summary = (
    result_df
    .groupby("scenario")["employee_prediction"]
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
    result_df["employee_prediction"]
    .value_counts()
    .to_string()
)


print("\nOutput:")
print(OUTPUT_PATH)

print(
    "\nNote: These are synthetic behavioral scenarios, "
    "not confirmed attacks."
)