import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TrustLog SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(30, 64, 175, 0.12),
            transparent 30%
        ),
        #070b14;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #1e293b;
}

[data-testid="stSidebar"] * {
    color: #cbd5e1;
}

.brand {
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #f8fafc;
    margin-bottom: 0;
}

.brand span {
    color: #38bdf8;
}

.subtitle {
    color: #64748b;
    font-size: 14px;
    margin-top: -4px;
    margin-bottom: 18px;
}

.live-status {
    display: inline-block;
    background: rgba(34, 197, 94, 0.10);
    border: 1px solid rgba(34, 197, 94, 0.30);
    color: #4ade80;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 700;
}

.metric-card {
    background:
        linear-gradient(
            145deg,
            rgba(17, 24, 39, 0.96),
            rgba(15, 23, 42, 0.96)
        );
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 18px;
    min-height: 125px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
}

.metric-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.metric-value {
    color: #f8fafc;
    font-size: 30px;
    font-weight: 850;
    margin-top: 8px;
}

.metric-sub {
    color: #64748b;
    font-size: 11px;
    margin-top: 3px;
}

.section-title {
    color: #f8fafc;
    font-size: 19px;
    font-weight: 750;
    margin-top: 8px;
    margin-bottom: 12px;
}

.info-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 18px;
    line-height: 1.6;
}

.footer-card {
    text-align: center;
    color: #64748b;
    font-size: 11px;
    line-height: 1.8;
    padding: 12px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# API FUNCTIONS
# ============================================================

@st.cache_data(ttl=30)
def get_api(endpoint):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return None


def clear_cache():
    get_api.clear()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:850;
            color:#f8fafc;
            margin-bottom:4px;
        ">
            🛡️ TRUSTLOG
        </div>

        <div style="
            font-size:11px;
            color:#64748b;
            margin-bottom:20px;
        ">
            SECURITY OPERATIONS CENTER
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Risk Monitoring",
            "Employee Investigation",
            "Explainable AI",
            "MITRE ATT&CK",
            "IPFS Evidence",
            "Blockchain",
        ],
        label_visibility="collapsed",
    )
    
    if st.session_state.get("last_page") != page:
    	st.session_state["last_page"] = page

    	components.html(
            """
            <script>
                window.parent.scrollTo(0, 0);
                window.parent.document.documentElement.scrollTop = 0;
                window.parent.document.body.scrollTop = 0;
           </script>
           """,
           height=0,
        )

    st.divider()

    if st.button(
        "🔄 Refresh Data",
        width="stretch",
    ):
        clear_cache()
        st.rerun()

    st.divider()

    st.markdown(
        """
        <div style="
            font-size:11px;
            color:#64748b;
            line-height:1.7;
        ">
            <b>TrustLog</b><br>
            AI-driven behavioral anomaly detection<br>
            CERT insider-threat dataset<br>
            Role-aware Isolation Forest<br>
            Local IPFS + Ethereum-compatible blockchain
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD OVERVIEW
# ============================================================

overview = get_api("/api/overview")

if overview is None:
    st.error(
        "Unable to connect to the TrustLog API. "
        "Make sure FastAPI is running on port 8000."
    )
    st.stop()

if overview.get("status") != "success":
    st.error(
        overview.get(
            "message",
            "TrustLog API returned an error.",
        )
    )
    st.stop()


# ============================================================
# GLOBAL HEADER
# ============================================================

st.markdown(
    '<div class="brand">TRUST<span>LOG</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "AI-Driven Behavioral Security Operations Center"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<span class="live-status">● SYSTEM OPERATIONAL</span>',
    unsafe_allow_html=True,
)

st.write("")


# ============================================================
# COMMON DATA
# ============================================================

total_days = overview["total_employee_days"]
anomaly_count = overview["anomaly_count"]
anomaly_percentage = overview["anomaly_percentage"]
employee_count = overview["unique_employees"]

risk_levels = overview.get(
    "risk_levels",
    {},
)

critical_count = risk_levels.get(
    "Critical",
    0,
)

high_count = risk_levels.get(
    "High",
    0,
)

medium_count = risk_levels.get(
    "Medium",
    0,
)

low_count = risk_levels.get(
    "Low",
    0,
)


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="section-title">Security Overview</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    EMPLOYEE-DAY RECORDS
                </div>
                <div class="metric-value">
                    {total_days:,}
                </div>
                <div class="metric-sub">
                    analyzed by TrustLog
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    AI ANOMALIES
                </div>
                <div class="metric-value">
                    {anomaly_count:,}
                </div>
                <div class="metric-sub">
                    {anomaly_percentage}% of analyzed days
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    CRITICAL RISK
                </div>
                <div class="metric-value">
                    {critical_count:,}
                </div>
                <div class="metric-sub">
                    highest presentation category
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    UNIQUE EMPLOYEES
                </div>
                <div class="metric-value">
                    {employee_count:,}
                </div>
                <div class="metric-sub">
                    represented in test period
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------
    # Risk Distribution
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">Risk Distribution</div>',
            unsafe_allow_html=True,
        )

        risk_df = pd.DataFrame(
            {
                "Risk Level": [
                    "Low",
                    "Medium",
                    "High",
                    "Critical",
                ],
                "Count": [
                    low_count,
                    medium_count,
                    high_count,
                    critical_count,
                ],
            }
        )

        fig = px.bar(
            risk_df,
            x="Risk Level",
            y="Count",
            text="Count",
        )

        fig.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
        )

        fig.update_layout(
            height=360,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#cbd5e1",
            ),
            xaxis=dict(
                title=None,
                gridcolor="#1e293b",
            ),
            yaxis=dict(
                title=None,
                gridcolor="#1e293b",
            ),
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    # --------------------------------------------------------
    # Detection Summary
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">Detection Summary</div>',
            unsafe_allow_html=True,
        )

        summary_df = pd.DataFrame(
            {
                "Metric": [
                    "Anomaly rate",
                    "Low risk",
                    "Medium risk",
                    "High risk",
                    "Critical risk",
                ],
                "Value": [
                    f"{anomaly_percentage}%",
                    f"{low_count:,}",
                    f"{medium_count:,}",
                    f"{high_count:,}",
                    f"{critical_count:,}",
                ],
            }
        )

        st.dataframe(
            summary_df,
            width="stretch",
            hide_index=True,
        )

        st.markdown(
            "### Analysis window"
        )

        st.markdown(
            f"""
**{overview.get("date_start")} → {overview.get("date_end")}**

---

**DETECTION MODEL**

Role-aware Isolation Forest

---

**IMPORTANT**

Risk levels represent model-derived behavioral risk categories and do not by themselves confirm malicious activity.
"""
        )

    st.write("")

    # --------------------------------------------------------
    # Priority Investigations
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🔴 Priority Investigations</div>',
        unsafe_allow_html=True,
    )

    anomalies = get_api(
        "/api/anomalies?risk_level=Critical&limit=10"
    )

    if anomalies and anomalies.get("status") == "success":

        records = anomalies.get(
            "records",
            [],
        )

        if records:

            rows = []

            for record in records:

                rows.append(
                    {
                        "Employee": record.get(
                            "user",
                            "Unknown",
                        ),
                        "Role": record.get(
                            "Role",
                            "Unknown",
                        ),
                        "Date": record.get(
                            "date_only",
                            "",
                        ),
                        "Risk Score": record.get(
                            "risk_score",
                            0,
                        ),
                        "Anomaly Score": round(
                            record.get(
                                "role_anomaly_score",
                                0,
                            ),
                            4,
                        ),
                        "Reasons": record.get(
                            "explanation_count",
                            0,
                        ),
                    }
                )

            priority_df = pd.DataFrame(rows)

            st.dataframe(
                priority_df,
                width="stretch",
                hide_index=True,
            )


# ============================================================
# PAGE 2 — RISK MONITORING
# ============================================================

elif page == "Risk Monitoring":

    st.markdown(
        '<div class="section-title">Risk Monitoring</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Filter model-detected anomalous employee-days."
    )

    roles = [
        "All Roles"
    ] + overview.get(
        "roles",
        [],
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_risk = st.selectbox(
            "Risk Level",
            [
                "All",
                "Critical",
                "High",
                "Medium",
                "Low",
            ],
        )

    with col2:

        selected_role = st.selectbox(
            "Role",
            roles,
        )

    with col3:

        result_limit = st.slider(
            "Records",
            min_value=10,
            max_value=100,
            value=25,
            step=5,
        )

    endpoint = "/api/anomalies?"

    params = []

    if selected_risk != "All":
        params.append(
            f"risk_level={selected_risk}"
        )

    if selected_role != "All Roles":
        params.append(
            f"role={selected_role}"
        )

    params.append(
        f"limit={result_limit}"
    )

    endpoint += "&".join(params)

    result = get_api(endpoint)

    if result and result.get("status") == "success":

        records = result.get(
            "records",
            [],
        )

        if records:

            df = pd.DataFrame(records)

            display_columns = [
                "user",
    		"Role",
   		"date_only",
   	 	"risk_score",
    		"risk_level",
    		"role_anomaly_score",
   	 	"explanation_count",
    		"login_hour",
    		"http_event_count",
    		"after_hours_http",
    		"device_connect_count",            
	   ]

            available = [
                column
                for column in display_columns
                if column in df.columns
            ]

            st.dataframe(
                df[available],
                width="stretch",
                hide_index=True,
            )

        else:

            st.info(
                "No records matched the selected filters."
            )



# ============================================================
# PAGE 3 — EMPLOYEE INVESTIGATION
# ============================================================

elif page == "Employee Investigation":

    st.markdown(
        '<div class="section-title">Employee Investigation</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Investigate behavioral history for an individual employee."
    )

    user_id = st.text_input(
        "Employee ID",
        placeholder="Example: DTAA/SJH0588",
    )

    if user_id:

        employee = get_api(
            f"/api/employee/{user_id}"
        )

        if employee and employee.get("status") == "success":

            ec1, ec2, ec3, ec4 = st.columns(4)

            with ec1:
                st.metric(
                    "Role",
                    employee["role"],
                )

            with ec2:
                st.metric(
                    "Employee Days",
                    employee["employee_days"],
                )

            with ec3:
                st.metric(
                    "Anomalies",
                    employee["anomaly_count"],
                )

            with ec4:
                st.metric(
                    "Max Risk",
                    employee["maximum_risk_score"],
                )

            st.write("")

            timeline = pd.DataFrame(
                employee["timeline"]
            )

            if not timeline.empty:

                # ------------------------------------------------
                # Risk Timeline
                # ------------------------------------------------

                st.markdown(
                    "### Employee Risk Timeline"
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=timeline["date_only"],
                        y=timeline["risk_score"],
                        mode="lines+markers",
                        name="Risk Score",
                    )
                )

                fig.update_layout(
                    height=380,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        color="#cbd5e1",
                    ),
                    xaxis=dict(
                        title=None,
                        gridcolor="#1e293b",
                    ),
                    yaxis=dict(
                        title="Risk Score",
                        range=[0, 105],
                        gridcolor="#1e293b",
                    ),
                    margin=dict(
                        l=10,
                        r=10,
                        t=20,
                        b=10,
                    ),
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                )

                st.write("")

                # ------------------------------------------------
                # Investigation Details
                # ------------------------------------------------

                st.markdown(
                    "### Investigation Details"
                )

                st.caption(
                    "Behavioral indicators associated with the employee's "
                    "model-derived risk scores."
                )

                detail_columns = [
                    "date_only",
                    "risk_score",
                    "risk_level",
                    "login_hour",
                    "http_event_count",
                    "after_hours_http",
                    "device_connect_count",
                    "login_time_deviation",
                    "http_activity_deviation",
                    "explanation_count",
                ]

                available_detail_columns = [
                    column
                    for column in detail_columns
                    if column in timeline.columns
                ]

                detail_df = timeline[
                    available_detail_columns
                ].copy()

                detail_df = detail_df.sort_values(
                    "date_only",
                    ascending=False,
                )

                st.dataframe(
                    detail_df,
                    width="stretch",
                    hide_index=True,
                )

                st.write("")

                # ------------------------------------------------
                # Behavioral Summary
                # ------------------------------------------------

                st.markdown(
                    "### Behavioral Summary"
                )

                summary_columns = [
                    "login_hour",
                    "http_event_count",
                    "after_hours_http",
                    "device_connect_count",
                    "login_time_deviation",
                    "http_activity_deviation",
                ]

                available_summary_columns = [
                    column
                    for column in summary_columns
                    if column in timeline.columns
                ]

                if available_summary_columns:

                    summary_values = []

                    for column in available_summary_columns:

                        value = timeline[column].mean()

                        summary_values.append(
                            {
                                "Indicator": column,
                                "Average": round(
                                    float(value),
                                    2,
                                ),
                            }
                        )

                    summary_df = pd.DataFrame(
                        summary_values
                    )

                    st.dataframe(
                        summary_df,
                        width="stretch",
                        hide_index=True,
                    )

        else:

            st.warning(
                employee.get(
                    "message",
                    "Employee not found.",
                )
                if employee
                else "Employee investigation request failed."
            )

# ============================================================
# PAGE 4 - EXPLAINABLE AI
# ============================================================

elif page == "Explainable AI":

    st.markdown(
        '<div class="section-title">🧠 Explainable AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            <b>TrustLog does not treat an anomaly score as proof of an attack.</b>
            The explanation layer identifies behavioral indicators that contributed
            to an employee-day being flagged for investigation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # --------------------------------------------------------
    # Explanation indicators
    # --------------------------------------------------------

    explanation_data = pd.DataFrame(
        {
            "Indicator": [
                "After-hours login",
                "Login-time deviation > 60 min",
                "HTTP activity deviation > 50",
                "After-hours HTTP activity > 10",
                "Device connection activity",
                "High HTTP activity > 100",
            ],
            "Meaning": [
                "Login occurred outside the initial operational window.",
                "Login timing differs substantially from the employee's previous baseline.",
                "HTTP volume differs substantially from the employee's previous baseline.",
                "Web activity occurred repeatedly outside the initial operational window.",
                "A device connection was observed.",
                "High daily HTTP event volume was observed.",
            ],
        }
    )

    st.markdown("### Behavioral Indicators")

    st.dataframe(
        explanation_data,
        width="stretch",
        hide_index=True,
    )

    st.write("")

    # --------------------------------------------------------
    # Load anomaly data
    # --------------------------------------------------------

    anomalies = get_api(
        "/api/anomalies?limit=500"
    )

    if anomalies and anomalies.get("status") == "success":

        df = pd.DataFrame(
            anomalies.get("records", [])
        )

        if not df.empty and "explanation_count" in df.columns:

            # ------------------------------------------------
            # Summary metrics
            # ------------------------------------------------

            total_explained = len(df)

            avg_reasons = round(
                float(df["explanation_count"].mean()),
                2,
            )

            max_reasons = int(
                df["explanation_count"].max()
            )

            multi_reason = int(
                (df["explanation_count"] >= 3).sum()
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Explained Anomalies",
                    f"{total_explained:,}",
                )

            with col2:
                st.metric(
                    "Average Indicators",
                    avg_reasons,
                )

            with col3:
                st.metric(
                    "Maximum Indicators",
                    max_reasons,
                )

            with col4:
                st.metric(
                    "3+ Indicators",
                    f"{multi_reason:,}",
                )

            st.write("")

            # ------------------------------------------------
            # Explanation distribution
            # ------------------------------------------------

            st.markdown("### Explanation Distribution")

            distribution = (
                df["explanation_count"]
                .value_counts()
                .sort_index()
                .reset_index()
            )

            distribution.columns = [
                "Explanation Count",
                "Records",
            ]

            fig = px.bar(
                distribution,
                x="Explanation Count",
                y="Records",
                text="Records",
            )

            fig.update_traces(
                hovertemplate=(
                    "Indicators: %{x}"
                    "<br>Records: %{y}"
                    "<extra></extra>"
                )
            )

            fig.update_layout(
                height=360,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#cbd5e1",
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20,
                ),
                xaxis=dict(
                    title="Number of Behavioral Indicators",
                    gridcolor="#1e293b",
                ),
                yaxis=dict(
                    title="Anomalous Employee-Days",
                    gridcolor="#1e293b",
                ),
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

            st.write("")

            # ------------------------------------------------
            # Most strongly explained cases
            # ------------------------------------------------

            st.markdown(
                "### Strongest Explainable Cases"
            )

            display_columns = [
                "user",
                "Role",
                "date_only",
                "risk_score",
                "risk_level",
                "explanation_count",
                "login_hour",
                "http_event_count",
                "after_hours_http",
                "device_connect_count",
                "login_time_deviation",
                "http_activity_deviation",
            ]

            available_columns = [
                column
                for column in display_columns
                if column in df.columns
            ]

            strongest = (
                df.sort_values(
                    [
                        "explanation_count",
                        "risk_score",
                    ],
                    ascending=False,
                )
                .head(15)
                [available_columns]
                .copy()
            )

            st.dataframe(
                strongest,
                width="stretch",
                hide_index=True,
            )

            st.write("")

            # ------------------------------------------------
            # Interpretation
            # ------------------------------------------------

            st.markdown("### How TrustLog Explains an Anomaly")

            st.markdown(
                """
**1. Behavioral baseline**

TrustLog compares employee activity with previously observed behavior.

**2. Behavioral indicators**

Features such as unusual login timing, HTTP activity, after-hours activity and device connections are evaluated.

**3. Anomaly detection**

The role-aware Isolation Forest identifies employee-days that differ from the learned behavioral patterns.

**4. Explanation layer**

TrustLog presents the observable indicators associated with the flagged employee-day so that an analyst can investigate the underlying activity.

**Important:** These indicators support investigation. They do not independently establish that malicious activity occurred.
                """
            )

        else:

            st.info(
                "No explainable anomaly records are currently available."
            )

    else:

        st.error(
            "Unable to load anomaly data from the TrustLog API."
        )

# ============================================================
# PAGE 5 — MITRE ATT&CK
# ============================================================

elif page == "MITRE ATT&CK":

    st.markdown(
        '<div class="section-title">🛡️ MITRE ATT&CK Mapping</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            TrustLog maps selected behavioral indicators to
            potentially relevant MITRE ATT&CK techniques.
            These mappings are behavioral associations only
            and should not be interpreted as confirmed attacks.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    mitre_data = pd.DataFrame(
        {
            "Technique": [
                "T1078",
                "T1091",
                "T1071",
            ],
            "Name": [
                "Valid Accounts",
                "Replication Through Removable Media",
                "Application Layer Protocol",
            ],
            "TrustLog Indicator": [
                "After-hours authentication behavior",
                "Removable-device connection activity",
                "High web/HTTP activity",
            ],
            "Interpretation": [
                "Potentially relevant behavioral association",
                "Potentially relevant behavioral association",
                "Potentially relevant behavioral association",
            ],
        }
    )

    st.dataframe(
        mitre_data,
        width="stretch",
        hide_index=True,
    )


# ============================================================
# PAGE 6 — IPFS EVIDENCE
# ============================================================

elif page == "IPFS Evidence":

    st.markdown(
        '<div class="section-title">📦 IPFS Evidence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            TrustLog stores detailed evidence off-chain using
            IPFS. The blockchain stores integrity metadata
            including the SHA-256 hash and IPFS CID.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    ipfs_col1, ipfs_col2 = st.columns(2)

    with ipfs_col1:

        st.markdown("### Evidence Object")

        st.code(
            "high_risk_evidence.json",
            language="text",
        )

        st.markdown("### IPFS CID")

        st.code(
            "QmfFguXXn3sefUzkfJKcFBDEeLURo5NgbA2cjS3DpuzaVM",
            language="text",
        )

    with ipfs_col2:

        st.markdown("### SHA-256")

        st.code(
            "c98d94b7550413f592835ab2c376c1646a0b56b8360a7723ef3247e94c196b0e",
            language="text",
        )

        st.markdown("### Local Gateway")

        st.code(
            "http://127.0.0.1:8080",
            language="text",
        )

    st.info(
        "The current IPFS node is local to the development machine."
    )


# ============================================================
# PAGE 7 — BLOCKCHAIN
# ============================================================

elif page == "Blockchain":

    st.markdown(
        '<div class="section-title">⛓️ Blockchain Verification</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            TrustLog uses a local Ethereum-compatible test
            blockchain to register evidence integrity metadata.
            Detailed evidence remains in IPFS while the
            blockchain records the evidence identifier,
            SHA-256 hash, CID, risk score and timestamp.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    blockchain_data = pd.DataFrame(
        {
            "Field": [
                "Evidence ID",
                "Smart Contract",
                "SHA-256 Hash",
                "IPFS CID",
                "Risk Score",
                "Blockchain",
            ],
            "Value": [
                "TRUSTLOG-HIGH-RISK-001",
                "0x6F80189A19ce950F7B0aeDe8ca16BfcB7dA39782",
                "c98d94b7550413f592835ab2c376c1646a0b56b8360a7723ef3247e94c196b0e",
                "QmfFguXXn3sefUzkfJKcFBDEeLURo5NgbA2cjS3DpuzaVM",
                "100",
                "Ganache / Chain ID 1337",
            ],
        }
    )

    st.dataframe(
        blockchain_data,
        width="stretch",
        hide_index=True,
    )

    st.success(
        "Evidence metadata successfully registered and verified on the local blockchain."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    "### TRUSTLOG"
)

st.caption(
    "AI-Driven Behavioral Anomaly Detection & "
    "Tamper-Resistant Log Management"
)

st.markdown(
    "**Developed by**  \n"
    "**Sandriya P · Khushbu · Anushka · Adit**"
)

st.caption(
    "© 2026 Sandriya P, Khushbu Chauhan, "
    "Anushka Roy Chowdhury & Adit J Gond. "
    "All Rights Reserved."
)