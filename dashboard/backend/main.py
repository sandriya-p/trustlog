from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="TrustLog v2 API",
    description="AI-driven behavioral anomaly detection and tamper-resistant log management API",
    version="2.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATA_FILE = Path("data/processed/v2/trustlog_v2_detection_dataset.csv")


@app.get("/")
def root():
    return {
        "project": "TrustLog",
        "version": "2.0.0",
        "status": "online",
        "message": "TrustLog backend is running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "TrustLog API",
    }


@app.get("/api/overview")
def overview():
    if not DATA_FILE.exists():
        return {
            "status": "error",
            "message": "TrustLog v2 detection dataset not found",
        }

    df = pd.read_csv(DATA_FILE)

    total_records = len(df)

    anomaly_count = 0

    if "role_anomaly_score" in df.columns:
        anomaly_count = int(
            (df["role_anomaly_score"] < 0).sum()
        )

    risk_levels = {}

    if "risk_level" in df.columns:
        risk_levels = {
            str(k): int(v)
            for k, v in df["risk_level"].value_counts().items()
        }

    roles = []

    if "Role" in df.columns:
        roles = sorted(
            df["Role"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    return {
        "status": "success",
        "total_employee_days": total_records,
        "anomaly_count": anomaly_count,
        "anomaly_percentage": round(
            (anomaly_count / total_records) * 100,
            2,
        ) if total_records else 0,
        "risk_levels": risk_levels,
        "unique_employees": (
            int(df["user"].nunique())
            if "user" in df.columns
            else 0
        ),
        "date_start": (
            str(df["date_only"].min())
            if "date_only" in df.columns
            else None
        ),
        "date_end": (
            str(df["date_only"].max())
            if "date_only" in df.columns
            else None
        ),
        "roles": roles,
    }


@app.get("/api/anomalies")
def anomalies(
    risk_level: str | None = None,
    role: str | None = None,
    limit: int = 100,
):
    if not DATA_FILE.exists():
        return {
            "status": "error",
            "message": "TrustLog v2 detection dataset not found",
        }

    df = pd.read_csv(DATA_FILE)

    if "role_anomaly_score" in df.columns:
        df = df[df["role_anomaly_score"] < 0]

    if risk_level and "risk_level" in df.columns:
        df = df[
            df["risk_level"].astype(str).str.lower()
            == risk_level.lower()
        ]

    if role and "Role" in df.columns:
        df = df[
            df["Role"].astype(str).str.lower()
            == role.lower()
        ]

    if "risk_score" in df.columns:
        df = df.sort_values(
            "risk_score",
            ascending=False,
        )

    limit = max(1, min(limit, 500))

    records = df.head(limit).copy()

    records = records.where(
        pd.notnull(records),
        None,
    )

    return {
        "status": "success",
        "count": len(records),
        "records": records.to_dict(
            orient="records"
        ),
    }


@app.get("/api/employee/{user_id:path}")
def employee_details(user_id: str):
    if not DATA_FILE.exists():
        return {
            "status": "error",
            "message": "TrustLog v2 detection dataset not found",
        }

    df = pd.read_csv(DATA_FILE)

    employee = df[
        df["user"].astype(str).str.lower()
        == user_id.lower()
    ].copy()

    if employee.empty:
        return {
            "status": "error",
            "message": f"Employee {user_id} not found",
        }

    employee = employee.sort_values("date_only")

    if employee["Role"].notna().any():
        role = str(
            employee["Role"]
            .dropna()
            .iloc[0]
        )
    else:
        role = "Unknown"

    anomaly_mask = employee["role_anomaly_score"] < 0

    anomaly_count = int(
        anomaly_mask.sum()
    )

    average_risk = round(
        float(employee["risk_score"].mean()),
        2,
    )

    maximum_risk = round(
        float(employee["risk_score"].max()),
        2,
    )

    timeline_columns = [
        "date_only",
        "login_count",
        "login_hour",
        "after_hours_login",
        "total_session_hours",
        "device_connect_count",
        "http_event_count",
        "after_hours_http",
        "login_time_deviation",
        "http_activity_deviation",
        "role_anomaly_score",
        "risk_score",
        "risk_level",
        "explanation_count",
    ]

    available_columns = [
        column
        for column in timeline_columns
        if column in employee.columns
    ]

    timeline = employee[
        available_columns
    ].copy()

    timeline = timeline.where(
        pd.notnull(timeline),
        None,
    )

    return {
        "status": "success",
        "user": user_id,
        "role": role,
        "employee_days": len(employee),
        "anomaly_count": anomaly_count,
        "anomaly_percentage": round(
            (anomaly_count / len(employee)) * 100,
            2,
        ),
        "average_risk_score": average_risk,
        "maximum_risk_score": maximum_risk,
        "timeline": timeline.to_dict(
            orient="records"
        ),
    }