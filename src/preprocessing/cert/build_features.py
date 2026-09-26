import pandas as pd
from pathlib import Path


# Project paths
BASE = Path("data/raw/CERT/r1")
OUTPUT = Path("data/processed/v2")

OUTPUT.mkdir(parents=True, exist_ok=True)


# Input files
LOGON_FILE = BASE / "logon.csv"
DEVICE_FILE = BASE / "device.csv"
HTTP_FILE = BASE / "http.csv"
LDAP_DIR = BASE / "LDAP"


# Load logon data
print("Loading logon data...")
logon = pd.read_csv(LOGON_FILE)
logon["date"] = pd.to_datetime(logon["date"])


# Load device data
print("Loading device data...")
device = pd.read_csv(DEVICE_FILE)
device["date"] = pd.to_datetime(device["date"])


# Load HTTP data
print("Loading HTTP data...")
http = pd.read_csv(
    HTTP_FILE,
    header=None,
    names=["id", "date", "user", "pc", "url"]
)
http["date"] = pd.to_datetime(http["date"])


print("\nData loaded successfully.")
print("Logon:", logon.shape)
print("Device:", device.shape)
print("HTTP:", http.shape)


# Basic data checks
print("\n--- Basic Checks ---")

print("Logon users:", logon["user"].nunique())
print("Device users:", device["user"].nunique())
print("HTTP users:", http["user"].nunique())

print("Logon date range:", logon["date"].min(), "to", logon["date"].max())
print("Device date range:", device["date"].min(), "to", device["date"].max())
print("HTTP date range:", http["date"].min(), "to", http["date"].max())


# Load LDAP employee information
print("\nLoading LDAP data...")

ldap_files = sorted(LDAP_DIR.glob("*.csv"))

ldap_frames = []

for file in ldap_files:
    df = pd.read_csv(file)
    df["ldap_month"] = file.stem
    ldap_frames.append(df)

ldap = pd.concat(ldap_frames, ignore_index=True)

print("LDAP records:", ldap.shape)
print("Unique employees:", ldap["user_id"].nunique())
print("Roles:", ldap["Role"].nunique())

# Create employee-day table from logon activity
print("\nCreating employee-day login features...")

logon["date_only"] = logon["date"].dt.date

daily_logon = (
    logon[logon["activity"] == "Logon"]
    .groupby(["user", "date_only"])
    .agg(
        login_count=("id", "count"),
        first_login=("date", "min"),
        unique_login_pcs=("pc", "nunique"),
    )
    .reset_index()
)

print("Employee-day login rows:", daily_logon.shape)
print(daily_logon.head())

# Login timing features
daily_logon["login_hour"] = daily_logon["first_login"].dt.hour

daily_logon["after_hours_login"] = (
    (daily_logon["login_hour"] < 7) |
    (daily_logon["login_hour"] >= 19)
).astype(int)

print("\nLogin features created:")
print(
    daily_logon[
        [
            "user",
            "date_only",
            "login_count",
            "first_login",
            "login_hour",
            "after_hours_login",
            "unique_login_pcs",
        ]
    ].head()
)

# Calculate daily session duration
print("\nCalculating session duration...")

logon_sorted = logon.sort_values(["user", "date"]).copy()

logon_sorted["session_id"] = (
    (logon_sorted["activity"] == "Logon")
    .groupby(logon_sorted["user"])
    .cumsum()
)

logon_events = logon_sorted[logon_sorted["activity"] == "Logon"][
    ["user", "date", "session_id"]
].rename(columns={"date": "login_time"})

logoff_events = logon_sorted[logon_sorted["activity"] == "Logoff"][
    ["user", "date", "session_id"]
].rename(columns={"date": "logout_time"})

sessions = pd.merge(
    logon_events,
    logoff_events,
    on=["user", "session_id"],
    how="inner"
)

sessions["session_duration_hours"] = (
    sessions["logout_time"] - sessions["login_time"]
).dt.total_seconds() / 3600

sessions["date_only"] = sessions["login_time"].dt.date

daily_session = (
    sessions
    .groupby(["user", "date_only"])
    .agg(
        total_session_hours=("session_duration_hours", "sum"),
        session_count=("session_id", "count"),
    )
    .reset_index()
)

daily_logon = daily_logon.merge(
    daily_session,
    on=["user", "date_only"],
    how="left"
)

daily_logon["total_session_hours"] = daily_logon[
    "total_session_hours"
].fillna(0)

daily_logon["session_count"] = daily_logon[
    "session_count"
].fillna(0)

print("Session features added.")
print(
    daily_logon[
        [
            "user",
            "date_only",
            "total_session_hours",
            "session_count",
        ]
    ].head()
)


# Create employee-day device features
print("\nCreating employee-day device features...")

device["date_only"] = device["date"].dt.date

daily_device = (
    device
    .groupby(["user", "date_only"])
    .agg(
        device_connect_count=(
            "activity",
            lambda x: (x == "Connect").sum()
        ),
        device_disconnect_count=(
            "activity",
            lambda x: (x == "Disconnect").sum()
        ),
        unique_device_pcs=("pc", "nunique"),
    )
    .reset_index()
)

# Add device features to the employee-day table
daily_logon = daily_logon.merge(
    daily_device,
    on=["user", "date_only"],
    how="left"
)

# Users without device activity get zero
daily_logon["device_connect_count"] = (
    daily_logon["device_connect_count"].fillna(0)
)

daily_logon["device_disconnect_count"] = (
    daily_logon["device_disconnect_count"].fillna(0)
)

daily_logon["unique_device_pcs"] = (
    daily_logon["unique_device_pcs"].fillna(0)
)

print("Device features added.")
print(
    daily_logon[
        [
            "user",
            "date_only",
            "device_connect_count",
            "device_disconnect_count",
            "unique_device_pcs",
        ]
    ].head()
)

# Create employee-day HTTP features
print("\nCreating employee-day HTTP features...")

http["date_only"] = http["date"].dt.date

daily_http = (
    http
    .groupby(["user", "date_only"])
    .agg(
        http_event_count=("id", "count"),
        unique_urls=("url", "nunique"),
        unique_http_pcs=("pc", "nunique"),
    )
    .reset_index()
)

# Add HTTP features to the employee-day table
daily_logon = daily_logon.merge(
    daily_http,
    on=["user", "date_only"],
    how="left"
)

# Users without HTTP activity get zero
daily_logon["http_event_count"] = (
    daily_logon["http_event_count"].fillna(0)
)

daily_logon["unique_urls"] = (
    daily_logon["unique_urls"].fillna(0)
)

daily_logon["unique_http_pcs"] = (
    daily_logon["unique_http_pcs"].fillna(0)
)

print("HTTP features added.")
print(
    daily_logon[
        [
            "user",
            "date_only",
            "http_event_count",
            "unique_urls",
            "unique_http_pcs",
        ]
    ].head()
)

# Create after-hours device and HTTP features
print("\nCreating after-hours activity features...")

# After-hours device connections
device["hour"] = device["date"].dt.hour

daily_device_after_hours = (
    device[device["activity"] == "Connect"]
    .assign(
        after_hours_device=lambda x: (
            (x["hour"] < 7) | (x["hour"] >= 19)
        ).astype(int)
    )
    .groupby(["user", "date_only"])
    .agg(
        after_hours_device_connect=(
            "after_hours_device",
            "sum"
        )
    )
    .reset_index()
)

# After-hours HTTP activity
http["hour"] = http["date"].dt.hour

daily_http_after_hours = (
    http.assign(
        after_hours_http=lambda x: (
            (x["hour"] < 7) | (x["hour"] >= 19)
        ).astype(int)
    )
    .groupby(["user", "date_only"])
    .agg(
        after_hours_http=(
            "after_hours_http",
            "sum"
        )
    )
    .reset_index()
)

# Merge after-hours device activity
daily_logon = daily_logon.merge(
    daily_device_after_hours,
    on=["user", "date_only"],
    how="left"
)

# Merge after-hours HTTP activity
daily_logon = daily_logon.merge(
    daily_http_after_hours,
    on=["user", "date_only"],
    how="left"
)

# Users without after-hours activity get zero
daily_logon["after_hours_device_connect"] = (
    daily_logon["after_hours_device_connect"]
    .fillna(0)
)

daily_logon["after_hours_http"] = (
    daily_logon["after_hours_http"]
    .fillna(0)
)

print("After-hours features added.")

print(
    daily_logon[
        [
            "user",
            "date_only",
            "after_hours_device_connect",
            "after_hours_http",
        ]
    ].head()
)

# Calculate employee behavioral baseline
print("\nCalculating employee login-time baseline...")

# Convert first login time into minutes after midnight
daily_logon["login_minutes"] = (
    daily_logon["first_login"].dt.hour * 60
    + daily_logon["first_login"].dt.minute
)

# Calculate a time-aware login baseline using only previous days
daily_logon = daily_logon.sort_values(["user", "date_only"]).copy()

daily_logon["previous_login_baseline"] = (
    daily_logon.groupby("user")["login_minutes"]
    .transform(lambda x: x.shift(1).expanding().median())
)

# For the first observation of each employee, use that day's value
daily_logon["previous_login_baseline"] = (
    daily_logon["previous_login_baseline"]
    .fillna(daily_logon["login_minutes"])
)

daily_logon["login_time_deviation"] = (
    daily_logon["login_minutes"]
    - daily_logon["previous_login_baseline"]
).abs()

print("Login-time baseline added.")

print(
    daily_logon[
        [
            "user",
            "date_only",
            "login_minutes",
            "login_time_deviation",
        ]
    ].head()
)

# Calculate employee HTTP activity baseline
print("\nCalculating employee HTTP activity baseline...")

# Calculate a time-aware HTTP activity baseline using only previous days
daily_logon["previous_http_baseline"] = (
    daily_logon.groupby("user")["http_event_count"]
    .transform(lambda x: x.shift(1).expanding().median())
)

# For the first observation of each employee, use that day's value
daily_logon["previous_http_baseline"] = (
    daily_logon["previous_http_baseline"]
    .fillna(daily_logon["http_event_count"])
)

daily_logon["http_activity_deviation"] = (
    daily_logon["http_event_count"]
    - daily_logon["previous_http_baseline"]
).abs()

print("HTTP activity baseline added.")

print(
    daily_logon[
        [
            "user",
            "date_only",
            "http_event_count",
            "http_activity_deviation",
        ]
    ].head()
)

# Add month-specific employee role and active status
print("\nAdding month-specific employee information...")

# Create month key for employee-day records
daily_logon["month"] = pd.to_datetime(
    daily_logon["date_only"]
).dt.to_period("M").astype(str)

# Prepare LDAP data
ldap["user"] = "DTAA/" + ldap["user_id"]
ldap["month"] = ldap["ldap_month"]

employee_context = ldap[
    ["user", "month", "Role"]
].copy()

# Remove any accidental duplicate employee-month records
employee_context = employee_context.drop_duplicates(
    ["user", "month"]
)

# Add role and monthly employee status
daily_logon = daily_logon.merge(
    employee_context,
    on=["user", "month"],
    how="left"
)

# Employee is active if they appear in that month's LDAP snapshot
daily_logon["employee_active_status"] = (
    daily_logon["Role"].notna()
).astype(int)

print("Employee role and active status added.")

print(
    daily_logon[
        [
            "user",
            "date_only",
            "month",
            "Role",
            "employee_active_status",
        ]
    ].head(10)
)

# Save intermediate employee-day features
print("\nSaving intermediate feature dataset...")

output_file = OUTPUT / "employee_day_features_v1.csv"

daily_logon.to_csv(output_file, index=False)

print("Saved:", output_file)
print("Final shape:", daily_logon.shape)
print("\nFinal columns:")
print(daily_logon.columns.tolist())

# Create ML-ready feature dataset
print("\nCreating ML-ready feature dataset...")

ml_features = daily_logon[
    [
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
        "employee_active_status",
    ]
].copy()

print("ML feature shape:", ml_features.shape)
print("ML features:")
print(ml_features.columns.tolist())

# Save ML-ready feature dataset
ml_output_file = OUTPUT / "ml_features.csv"

ml_features.to_csv(
    ml_output_file,
    index=False
)

print("Saved ML dataset:", ml_output_file)
print("ML dataset shape:", ml_features.shape)

# Create time-based train/test split
print("\nCreating time-based train/test split...")

daily_logon["date_only"] = pd.to_datetime(daily_logon["date_only"])

train_data = daily_logon[
    daily_logon["date_only"] < "2011-01-01"
].copy()

test_data = daily_logon[
    daily_logon["date_only"] >= "2011-01-01"
].copy()

train_output = OUTPUT / "train_employee_days.csv"
test_output = OUTPUT / "test_employee_days.csv"

train_data.to_csv(train_output, index=False)
test_data.to_csv(test_output, index=False)

print("Training period:", train_data["date_only"].min(),
      "to", train_data["date_only"].max())

print("Testing period:", test_data["date_only"].min(),
      "to", test_data["date_only"].max())

print("Training shape:", train_data.shape)
print("Testing shape:", test_data.shape)