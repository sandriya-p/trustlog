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

DATA_FILE = Path("data/processed/v2/test_risk_scores.csv")

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

@app.get("/api/blockchain/evidence/{evidence_id}")
def get_blockchain_evidence(evidence_id: str):
    import json
    from web3 import Web3

    contract_address = "0xD8c1fAb61C9f23E0D9bA960F6F9C9Ba2fFFe4A52"
    rpc_url = "http://127.0.0.1:8545"
    abi_path = Path("artifacts/contracts/TrustLogRegistry.sol/TrustLogRegistry.json")

    if not abi_path.exists():
        return {"status": "error", "message": "Contract ABI file not found"}

    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        return {"status": "error", "message": "Ganache is not reachable"}

    try:
        with abi_path.open("r", encoding="utf-8") as f:
            abi = json.load(f)["abi"]

        contract = w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=abi,
        )

        record = contract.functions.getEvidence(evidence_id).call()

        return {
            "status": "success",
            "evidence_id": record[0],
            "sha256_hash": record[1],
            "ipfs_cid": record[2],
            "risk_score": record[3],
            "timestamp": record[4],
            "recorder": record[5],
            "contract_address": contract_address,
            "chain_id": w3.eth.chain_id,
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


@app.get("/api/ipfs/verify")
def verify_ipfs_evidence(
    cid: str = "QmfJXJyPpK1AGiMy2jwvdt3dsomtpxSw79SUtizfzYYR46",
    expected_sha256: str = (
        "1882fae6c2ba99ec459c7d0ae613b986"
        "c641c8f2b4fb9ad1c8a49be0b7f16fc1"
    ),
):
    import hashlib
    import requests

    ipfs_api = "http://127.0.0.1:5001"

    try:
        # Check that the IPFS API is reachable.
        version_response = requests.post(
            f"{ipfs_api}/api/v0/version",
            timeout=5,
        )
        version_response.raise_for_status()
        ipfs_version = version_response.json().get("Version", "unknown")

        # Retrieve the evidence content through the local IPFS API.
        file_response = requests.post(
            f"{ipfs_api}/api/v0/cat",
            params={"arg": cid},
            timeout=15,
        )
        file_response.raise_for_status()

        # Calculate SHA-256 over the exact retrieved bytes.
        actual_sha256 = hashlib.sha256(file_response.content).hexdigest()
        expected = expected_sha256.strip().lower()

        if len(expected) != 64 or any(
            char not in "0123456789abcdef" for char in expected
        ):
            return {
                "status": "error",
                "message": "Expected SHA-256 must contain 64 hexadecimal characters.",
                "ipfs_reachable": True,
                "ipfs_version": ipfs_version,
            }

        matched = actual_sha256 == expected

        return {
            "status": "verified" if matched else "mismatch",
            "ipfs_reachable": True,
            "ipfs_version": ipfs_version,
            "cid": cid,
            "expected_sha256": expected,
            "actual_sha256": actual_sha256,
            "hash_match": matched,
            "bytes_retrieved": len(file_response.content),
            "message": (
                "SHA-256 matches the expected fingerprint."
                if matched
                else "SHA-256 does not match the expected fingerprint."
            ),
        }

    except requests.RequestException as exc:
        return {
            "status": "unavailable",
            "ipfs_reachable": False,
            "message": f"IPFS verification could not complete: {exc}",
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
    anomalies_only: bool = True,
):
    if not DATA_FILE.exists():
        return {
            "status": "error",
            "message": "TrustLog v2 detection dataset not found",
        }

    df = pd.read_csv(DATA_FILE)

    if anomalies_only and "role_anomaly_score" in df.columns:
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
@app.get("/api/data-explorer")
def data_explorer(
    user: str | None = None,
    role: str | None = None,
    limit: int = 100,
):
    if not DATA_FILE.exists():
        return {
            "status": "error",
            "message": "TrustLog detection dataset not found",
        }

    df = pd.read_csv(DATA_FILE)

    if user and "user" in df.columns:
        df = df[
            df["user"].astype(str).str.lower()
            == user.lower()
        ]

    if role and "Role" in df.columns:
        df = df[
            df["Role"].astype(str).str.lower()
            == role.lower()
        ]

    if "date_only" in df.columns:
        df = df.sort_values(
            "date_only",
            ascending=False,
        )

    total = len(df)

    limit = max(1, min(limit, 2000))

    records = df.head(limit).copy()

    records = records.where(
        pd.notnull(records),
        None,
    )

    return {
        "status": "success",
        "count": len(records),
        "total": total,
        "records": records.to_dict(
            orient="records"
        ),
    }
