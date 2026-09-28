import pandas as pd

ROLE_PATH = r"data\processed\v2\test_role_aware_predictions.csv"
EMPLOYEE_PATH = r"data\processed\v2\test_employee_specific_predictions.csv"
OUTPUT_PATH = r"data\processed\v2\baseline_comparison.csv"

role = pd.read_csv(ROLE_PATH)
employee = pd.read_csv(EMPLOYEE_PATH)

# Compare only employee-days scored by both models
comparison = role[
    ["user", "date_only", "role_prediction", "role_anomaly_score"]
].merge(
    employee[
        ["user", "date_only", "employee_prediction",
         "employee_anomaly_score"]
    ],
    on=["user", "date_only"],
    how="inner"
)

# Save record-level comparison
comparison.to_csv(OUTPUT_PATH, index=False)

total = len(comparison)

role_anomalies = (comparison["role_prediction"] == -1).sum()
employee_anomalies = (
    comparison["employee_prediction"] == -1
).sum()

both_anomaly = (
    (comparison["role_prediction"] == -1)
    & (comparison["employee_prediction"] == -1)
).sum()

both_normal = (
    (comparison["role_prediction"] == 1)
    & (comparison["employee_prediction"] == 1)
).sum()

role_only = (
    (comparison["role_prediction"] == -1)
    & (comparison["employee_prediction"] == 1)
).sum()

employee_only = (
    (comparison["role_prediction"] == 1)
    & (comparison["employee_prediction"] == -1)
).sum()

agreement = (both_anomaly + both_normal) / total * 100

print("\n=== BASELINE COMPARISON ===")

print(f"Common employee-day records: {total}")

print(
    f"\nRole-aware anomalies: "
    f"{role_anomalies} "
    f"({role_anomalies / total * 100:.2f}%)"
)

print(
    f"Employee-specific anomalies: "
    f"{employee_anomalies} "
    f"({employee_anomalies / total * 100:.2f}%)"
)

print("\n=== AGREEMENT ===")

print(f"Both anomalous: {both_anomaly}")
print(f"Both normal: {both_normal}")
print(f"Role-aware only: {role_only}")
print(f"Employee-specific only: {employee_only}")

print(f"\nModel agreement: {agreement:.2f}%")

print(f"\nSaved comparison:")
print(OUTPUT_PATH)

print(
    "\nNote: These are behavioral anomaly results, "
    "not confirmed attack labels."
)