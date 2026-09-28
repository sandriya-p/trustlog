import pandas as pd
import numpy as np
from pathlib import Path


INPUT_PATH = Path(
    r"data\processed\v2\test_employee_days.csv"
)

OUTPUT_PATH = Path(
    r"data\processed\v2\simulated_activity.csv"
)


def main():
    print("Loading test employee-day data...")

    df = pd.read_csv(INPUT_PATH)

    print(f"Original records: {len(df)}")

    # Select a small, reproducible sample of normal employee-day records.
    sample = df.sample(
        n=min(100, len(df)),
        random_state=42
    ).copy()

    scenarios = []

    # ---------------------------------------------------------
    # Scenario 1: Unusual login time
    # ---------------------------------------------------------
    unusual_login = sample.copy()

    unusual_login["scenario"] = "unusual_login_time"

    unusual_login["login_hour"] = (
        unusual_login["login_hour"] + 8
    ) % 24

    unusual_login["after_hours_login"] = 1

    scenarios.append(unusual_login)

    # ---------------------------------------------------------
    # Scenario 2: Unfamiliar PC / device
    # ---------------------------------------------------------
    unfamiliar_device = sample.copy()

    unfamiliar_device["scenario"] = "unfamiliar_device"

    unfamiliar_device["unique_login_pcs"] = (
        unfamiliar_device["unique_login_pcs"] + 3
    )

    unfamiliar_device["unique_device_pcs"] = (
        unfamiliar_device["unique_device_pcs"] + 3
    )

    unfamiliar_device["device_connect_count"] = (
        unfamiliar_device["device_connect_count"] + 3
    )

    scenarios.append(unfamiliar_device)

    # ---------------------------------------------------------
    # Scenario 3: Unusual web activity
    # ---------------------------------------------------------
    unusual_web = sample.copy()

    unusual_web["scenario"] = "unusual_web_activity"

    unusual_web["http_event_count"] = (
        unusual_web["http_event_count"] * 5 + 10
    )

    unusual_web["unique_urls"] = (
        unusual_web["unique_urls"] + 20
    )

    unusual_web["unique_http_pcs"] = (
        unusual_web["unique_http_pcs"] + 3
    )

    unusual_web["after_hours_http"] = 1

    scenarios.append(unusual_web)

    # ---------------------------------------------------------
    # Scenario 4: Combined unusual behavior
    # ---------------------------------------------------------
    combined = sample.copy()

    combined["scenario"] = "combined_behavior"

    combined["login_hour"] = (
        combined["login_hour"] + 8
    ) % 24

    combined["after_hours_login"] = 1

    combined["unique_login_pcs"] = (
        combined["unique_login_pcs"] + 3
    )

    combined["unique_device_pcs"] = (
        combined["unique_device_pcs"] + 3
    )

    combined["device_connect_count"] = (
        combined["device_connect_count"] + 3
    )

    combined["http_event_count"] = (
        combined["http_event_count"] * 5 + 10
    )

    combined["unique_urls"] = (
        combined["unique_urls"] + 20
    )

    combined["unique_http_pcs"] = (
        combined["unique_http_pcs"] + 3
    )

    combined["after_hours_http"] = 1

    scenarios.append(combined)

    # Combine all synthetic scenarios.
    simulated = pd.concat(
        scenarios,
        ignore_index=True
    )

    # Mark all generated records explicitly as synthetic.
    simulated["synthetic"] = True

    # Save results.
    simulated.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n=== SIMULATION COMPLETE ===")
    print(f"Original records used: {len(sample)}")
    print(f"Simulated records: {len(simulated)}")

    print("\nScenario counts:")
    print(simulated["scenario"].value_counts())

    print(f"\nOutput:")
    print(OUTPUT_PATH)

    print(
        "\nImportant: These are synthetic behavioral "
        "scenarios, not real attacks."
    )


if __name__ == "__main__":
    main()