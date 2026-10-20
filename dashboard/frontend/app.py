import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
API_BASE_URL = "http://127.0.0.1:8000"

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

/* =========================================================
   CYBERNOVA-INSPIRED TRUSTLOG SOC THEME
   ========================================================= */

:root {
    --soc-bg: #0b0d14;
    --soc-panel: #151925;
    --soc-panel-hover: #1b2130;
    --soc-border: #293145;
    --soc-text: #e7edf8;
    --soc-muted: #8490a6;
    --soc-cyan: #48b9f5;
    --soc-green: #39d98a;
    --soc-red: #ff596d;
    --soc-amber: #f6bd4b;
    --soc-purple: #9b8cff;
}

.stApp {
    background: var(--soc-bg) !important;
    color: var(--soc-text);
}

[data-testid="stHeader"] {
    background: rgba(11, 13, 20, 0.94);
    border-bottom: 1px solid var(--soc-border);
}

[data-testid="stSidebar"] {
    background: #111522 !important;
    border-right: 1px solid var(--soc-border);
}

[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

[data-testid="stSidebar"] hr {
    border-color: var(--soc-border);
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 4px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 7px;
    padding: 7px 10px;
    transition: background 0.15s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #20283a;
}

[data-testid="stSidebar"] [role="radiogroup"] label p {
    font-size: 0.84rem;
}

.main .block-container {
    max-width: 1800px;
    padding-top: 1.1rem;
    padding-bottom: 1.5rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

.brand {
    font-size: 29px;
    font-weight: 900;
    letter-spacing: 2.5px;
    margin-bottom: 2px;
}

.brand span {
    color: var(--soc-cyan);
}

.subtitle {
    font-size: 12px;
    color: var(--soc-muted);
    margin-top: 0;
    margin-bottom: 10px;
}

.live-status {
    background: rgba(57, 217, 138, 0.09);
    border: 1px solid rgba(57, 217, 138, 0.25);
    color: var(--soc-green);
    border-radius: 5px;
    padding: 4px 9px;
    font-size: 10px;
    letter-spacing: 0.7px;
    font-weight: 800;
}

.section-title {
    font-size: 18px;
    font-weight: 800;
    color: #f2f6ff;
    margin-top: 4px;
    margin-bottom: 10px;
}

.info-card {
    background: var(--soc-panel);
    border: 1px solid var(--soc-border);
    border-radius: 9px;
    padding: 14px 16px;
    line-height: 1.55;
}

.metric-card {
    background: var(--soc-panel);
    border: 1px solid var(--soc-border);
    border-radius: 10px;
    padding: 14px;
    min-height: 110px;
    box-shadow: none;
    transition: border-color 0.15s ease,
                background 0.15s ease;
}

.metric-card:hover {
    background: var(--soc-panel-hover);
    border-color: #3c4963;
}

.metric-label {
    color: var(--soc-muted);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.7px;
}

.metric-value {
    color: #f4f7ff;
    font-size: 27px;
    font-weight: 850;
    margin-top: 8px;
}

.metric-sub {
    color: var(--soc-muted);
    font-size: 10px;
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid var(--soc-border);
    border-radius: 8px;
    overflow: hidden;
}

[data-testid="stMetric"] {
    background: var(--soc-panel);
    border: 1px solid var(--soc-border);
    border-radius: 9px;
    padding: 13px 15px;
}

[data-testid="stMetricLabel"] {
    color: var(--soc-muted);
    font-size: 11px;
}

[data-testid="stMetricValue"] {
    color: #f4f7ff;
    font-weight: 800;
}

[data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
    gap: 0.8rem;
}

.stButton > button {
    border: 1px solid var(--soc-border);
    border-radius: 6px;
    font-weight: 700;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    border-color: var(--soc-cyan);
    color: var(--soc-cyan);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #171c29;
    border-color: var(--soc-border);
    border-radius: 6px;
}

[data-testid="stAlert"] {
    border-radius: 8px;
}

[data-testid="stCaptionContainer"] {
    color: var(--soc-muted);
}

.footer-card {
    color: var(--soc-muted);
    border-top: 1px solid var(--soc-border);
    padding-top: 14px;
}

@media (max-width: 900px) {
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .brand {
        font-size: 24px;
    }

    .metric-value {
        font-size: 22px;
    }
}

/* TrustLog colorful SOC accents */
:root {
    --risk-low: #38D996;
    --risk-medium: #F5C451;
    --risk-high: #FF914D;
    --risk-critical: #FF5D73;
    --accent-cyan: #48C8F5;
    --accent-violet: #AD8CFF;
    --accent-teal: #38D9C0;
}

/* Colorful section headings */
.section-title {
    border-left: 3px solid var(--accent-cyan);
    padding-left: 10px;
}

/* Distinct, subtle color accents on metric cards */
/* Color-coded TrustLog overview cards */
.metric-records {
    border-top: 3px solid #48C8F5;
    background: linear-gradient(145deg, #172333, #151925 65%);
}

.metric-anomalies {
    border-top: 3px solid #AD8CFF;
    background: linear-gradient(145deg, #211B35, #151925 65%);
}

.metric-critical {
    border-top: 3px solid #FF3030;
    background: linear-gradient(145deg, #351719, #151925 65%);
}

.metric-employees {
    border-top: 3px solid #38D9C0;
    background: linear-gradient(145deg, #152C2D, #151925 65%);
}

/* Colorful interactive controls */
.stButton > button[kind="primary"] {
    background: linear-gradient(110deg, #2563EB, #7C3AED);
    border: 1px solid #5B7CFA;
    color: white;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(110deg, #3478FF, #925BFF);
    color: white;
}

/* Success, warning, and error states */
[data-testid="stAlert"] {
    border-radius: 8px;
}

[data-testid="stAlert"][kind="success"] {
    border-left: 4px solid var(--risk-low);
}

[data-testid="stAlert"][kind="warning"] {
    border-left: 4px solid var(--risk-medium);
}

[data-testid="stAlert"][kind="error"] {
    border-left: 4px solid var(--risk-critical);
}

/* More color in the navigation's selected item */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: rgba(72, 200, 245, 0.12);
    border-left: 3px solid var(--accent-cyan);
}

/* Employee investigation KPI accents */
.employee-role {
    border-top: 3px solid #48C8F5;
    background: linear-gradient(145deg, #172333, #151925 65%);
}

.employee-days {
    border-top: 3px solid #38D9C0;
    background: linear-gradient(145deg, #152C2D, #151925 65%);
}

.employee-anomalies {
    border-top: 3px solid #AD8CFF;
    background: linear-gradient(145deg, #211B35, #151925 65%);
}

.employee-max-risk {
    border-top: 3px solid #FF3030;
    background: linear-gradient(145deg, #351719, #151925 65%);
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
            "Data Explorer"
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
            <div class="metric-card metric-records">
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
            <div class="metric-card metric-anomalies">
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
            <div class="metric-card metric-critical">
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
            <div class="metric-card metric-employees">
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

    left, right = st.columns([1.15, 0.85], gap="medium")

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
            color="Risk Level",
            color_discrete_map={
                "Low": "#38D996",
                "Medium": "#F5C451",
                "High": "#FF914D",
                "Critical": "#FF3030",
            },
            category_orders={
                "Risk Level": ["Low", "Medium", "High", "Critical"]
            },
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
                color="#E7EDF8",
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
        "Explore AI-detected anomalies or all risk-scored employee-days."
    )

    roles = [
        "All Roles"
    ] + overview.get(
        "roles",
        [],
    )

    col1, col2, col3, col4 = st.columns(4)

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

    with col4:
        record_type = st.selectbox(
            "Record Type",
            [
                "AI-detected anomalies",
                "All risk-scored records",
            ],
        )

    endpoint = "/api/anomalies?"

    params = [
        f"anomalies_only={str(record_type == 'AI-detected anomalies').lower()}"
    ]

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

            # Color-coded SOC risk table
            display_df = df[available].copy()

            if "role_anomaly_score" in display_df.columns:
                display_df["role_anomaly_score"] = (
                    pd.to_numeric(
                        display_df["role_anomaly_score"],
                        errors="coerce",
                    ).round(3)
                )

            if "risk_score" in display_df.columns:
                display_df["risk_score"] = (
                    pd.to_numeric(
                        display_df["risk_score"],
                        errors="coerce",
                    ).round(2)
                )

            risk_colors = {
                "Low": "#176B4D",
                "Medium": "#80651C",
                "High": "#91451F",
                "Critical": "#8F202B",
            }

            cell_colors = []

            for column in display_df.columns:
                if column == "risk_level":
                    cell_colors.append(
                        display_df[column]
                        .map(risk_colors)
                        .fillna("#8490A6")
                        .tolist()
                    )
                else:
                    cell_colors.append(
                        ["#151925"] * len(display_df)
                    )

            fig_table = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=[
                                f"<b>{column}</b>"
                                for column in display_df.columns
                            ],
                            fill_color="#20283A",
                            line_color="#354057",
                            font=dict(
                                color="#E7EDF8",
                                size=11,
                            ),
                            align="left",
                            height=34,
                        ),
                        cells=dict(
                            values=[
                                display_df[column].tolist()
                                for column in display_df.columns
                            ],
                            fill_color=cell_colors,
                            line_color="#293145",
                            font=dict(
                                color=[
                                    "#FFFFFF"
                                    if column == "risk_level"
                                    else "#DCE5F5"
                                    for column in display_df.columns
                                ],
                                size=10,
                            ),
                            align="left",
                            height=30,
                        ),
                    )
                ]
            )

            fig_table.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=5, b=0),
                height=min(900, 90 + len(display_df) * 30),
            )

            st.plotly_chart(
                fig_table,
                width="stretch",
                config={"displayModeBar": False},
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

            employee_kpis = [
                (
                    "ROLE",
                    employee["role"],
                    "EMPLOYEE PROFILE",
                    "employee-role",
                ),
                (
                    "EMPLOYEE DAYS",
                    f'{employee["employee_days"]:,}',
                    "OBSERVED RECORDS",
                    "employee-days",
                ),
                (
                    "ANOMALIES",
                    f'{employee["anomaly_count"]:,}',
                    "DETECTED BY MODEL",
                    "employee-anomalies",
                ),
                (
                    "MAX RISK",
                    f'{employee["maximum_risk_score"]:.2f}',
                    "OUT OF 100",
                    "employee-max-risk",
                ),
            ]

            for column, (label, value, subtitle, css_class) in zip(
                [ec1, ec2, ec3, ec4],
                employee_kpis,
            ):
                with column:
                    st.markdown(
                        f"""
                        <div class="metric-card {css_class}">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-sub">{subtitle}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
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


                risk_colors = {
                    "Low": "#38D996",
                    "Medium": "#F5C451",
                    "High": "#FF914D",
                    "Critical": "#FF3038",
                }

                timeline = timeline.copy()
                timeline["date_only"] = pd.to_datetime(
                    timeline["date_only"]
                )
                timeline = timeline.sort_values("date_only")
                timeline["date_only"] = timeline["date_only"].dt.strftime("%Y-%m-%d")

                timeline["risk_level"] = timeline["risk_level"].astype(str)

                timeline["risk_color"] = (
                    timeline["risk_level"]
                    .map(risk_colors)
                    .fillna("#48C8F5")
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=timeline["date_only"],
                        y=timeline["risk_score"],
                        mode="lines+markers",
                        name="Risk Score",
                        line=dict(
                            color="#48C8F5",
                            width=2,
                        ),
                        marker=dict(
                            color=timeline["risk_color"].tolist(),
                            size=7,
                            line=dict(
                                color="#0B1220",
                                width=1,
                            ),
                        ),
                        customdata=timeline[
                            ["risk_level"]
                        ].to_numpy(),
                        hovertemplate=(
                            "<b>Date:</b> %{x|%d %b %Y}<br>"
                            "<b>Risk Score:</b> %{y:.2f}<br>"
                            "<b>Risk Level:</b> %{customdata[0]}"
                            "<extra></extra>"
                        ),
                    )
                )

                for level, color in risk_colors.items():
                    fig.add_trace(
                        go.Scatter(
                            x=[None],
                            y=[None],
                            mode="markers",
                            marker=dict(
                                color=color,
                                size=9,
                            ),
                            name=level,
                            showlegend=True,
                        )
                    )

                fig.update_layout(
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        color="#cbd5e1",
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
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
                        t=55,
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


                def style_investigation_row(row):
                    risk_colors = {
                        "Low": "#38D996",
                        "Medium": "#F5C451",
                        "High": "#FF914D",
                        "Critical": "#FF3038",
                    }

                    risk = str(row.get("risk_level", ""))
                    color = risk_colors.get(risk)

                    styles = [""] * len(row)

                    if color and "risk_level" in row.index:
                        risk_index = row.index.get_loc("risk_level")
                        styles[risk_index] = (
                            f"background-color: {color}; "
                            "color: #ffffff; font-weight: 700;"
                        )

                    return styles

                styled_details = detail_df.style.apply(
                    style_investigation_row,
                    axis=1,
                )

                number_formats = {
                    "risk_score": "{:.2f}",
                    "login_hour": "{:.0f}",
                    "http_event_count": "{:.0f}",
                    "after_hours_http": "{:.0f}",
                    "device_connect_count": "{:.0f}",
                    "login_time_deviation": "{:.2f}",
                    "http_activity_deviation": "{:.2f}",
                    "explanation_count": "{:.0f}",
                }

                styled_details = styled_details.format(
                    number_formats,
                    na_rep="—",
                )

                st.dataframe(
                    styled_details,
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

                indicator_labels = {
                    "login_hour": "Average Login Hour",
                    "http_event_count": "HTTP Events",
                    "after_hours_http": "After-Hours HTTP Events",
                    "device_connect_count": "Device Connections",
                    "login_time_deviation": "Login-Time Deviation",
                    "http_activity_deviation": "HTTP Activity Deviation",
                }

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
                                "Behavioral Indicator": indicator_labels.get(
                                    column, column
                                ),
                                "Average Value": (
                                    round(float(value), 2)
                                    if pd.notna(value)
                                    else None
                                ),
                            }
                        )

                    summary_df = pd.DataFrame(summary_values)

                    st.dataframe(
                        summary_df,
                        width="stretch",
                        hide_index=True,
                        column_config={
                            "Behavioral Indicator": st.column_config.TextColumn(
                                "Behavioral Indicator",
                            ),
                            "Average Value": st.column_config.NumberColumn(
                                "Average Value",
                                format="%.2f",
                            ),
                        },
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
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    st.markdown(
        '<div class="section-title">🔎 Data Explorer</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Explore employee-day detection records from the TrustLog dataset."
    )

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        explorer_user = st.text_input(
            "Employee ID",
            placeholder="e.g. AIB0797",
        )

    with col2:
        explorer_role = st.text_input(
            "Role",
            placeholder="e.g. Engineer",
        )

    with col3:
        explorer_limit = st.select_slider(
            "Rows to display",
            options=[100, 250, 500, 1000, 2000],
            value=100,
        )

    params = {
        "limit": int(explorer_limit),
    }

    if explorer_user.strip():
        params["user"] = explorer_user.strip()

    if explorer_role.strip():
        params["role"] = explorer_role.strip()

    try:

        response = requests.get(
            f"{API_BASE_URL}/api/data-explorer",
            params=params,
            timeout=10,
        )

        data = response.json()

        if data.get("status") == "success":

            records = data.get("records", [])
            total_records = data.get("total", len(records))

            st.caption(
                f"Showing {len(records):,} of {total_records:,} matching employee-day records"
            )

            if records:

                explorer_df = pd.DataFrame(records)

                st.dataframe(
                    explorer_df,
                    width="stretch",
                    hide_index=True,
                )

            else:

                st.info(
                    "No records found for the selected filters."
                )

        else:

            st.error(
                data.get(
                    "message",
                    "Unable to load Data Explorer data.",
                )
            )

    except Exception as e:

        st.error(
            f"Unable to connect to the TrustLog API: {e}"
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
                color="Explanation Count",
                color_continuous_scale="RdYlGn_r",
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
                    range=[
                        0,
                        max(distribution["Records"]) * 1.30,
                    ],
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

            risk_colors = {
                "Low": "#38D996",
                "Medium": "#F5C451",
                "High": "#FF914D",
                "Critical": "#FF3038",
            }

            def style_explanation_row(row):
                styles = [""] * len(row)
                risk = str(row.get("risk_level", ""))
                color = risk_colors.get(risk)

                if color and "risk_level" in row.index:
                    idx = row.index.get_loc("risk_level")
                    styles[idx] = (
                        f"background-color: {color}; "
                        "color: #ffffff; font-weight: 700;"
                    )

                return styles

            styled_strongest = strongest.style.apply(
                style_explanation_row,
                axis=1,
            )

            number_formats = {
                "risk_score": "{:.2f}",
                "explanation_count": "{:.0f}",
                "login_hour": "{:.0f}",
                "http_event_count": "{:.0f}",
                "after_hours_http": "{:.0f}",
                "device_connect_count": "{:.0f}",
                "login_time_deviation": "{:.2f}",
                "http_activity_deviation": "{:.2f}",
            }

            styled_strongest = styled_strongest.format(
                number_formats,
                na_rep="—",
            )

            st.dataframe(
                styled_strongest,
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
        '<div class="section-title">🛡️ MITRE ATT&CK Mapping & Investigation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            <b>Purpose</b><br>
            This page connects selected TrustLog behavioral indicators
            with potentially relevant MITRE ATT&CK techniques. These
            associations support investigation and contextual analysis;
            they do not establish that an attack occurred.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # --------------------------------------------------------
    # Technique mapping data
    # --------------------------------------------------------

    mitre_data = pd.DataFrame(
        {
            "Technique": ["T1078", "T1091", "T1071"],
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

    technique_details = {
        "T1078": {
            "name": "Valid Accounts",
            "tactic": "Defense Evasion, Persistence, Privilege Escalation, Initial Access",
            "meaning": (
                "An adversary may use legitimate account credentials to "
                "access systems. Such activity can resemble normal user "
                "behavior and may be difficult to distinguish without context."
            ),
            "indicator": "After-hours authentication behavior",
            "relevance": (
                "An unusual login time can be a reason to investigate an "
                "account, especially when combined with unfamiliar devices, "
                "unexpected access, or other anomalies. After-hours access "
                "alone does not indicate account compromise."
            ),
            "investigation": [
                "Review the login timestamp and the user's normal working pattern.",
                "Check the account, source device, and available authentication records.",
                "Compare the event with the user's historical behavior and approved work schedule.",
                "Look for corroborating indicators before escalating the event.",
            ],
            "limitation": (
                "TrustLog's after-hours indicator is not proof that valid "
                "credentials were stolen or misused."
            ),
        },
        "T1091": {
            "name": "Replication Through Removable Media",
            "tactic": "Initial Access, Lateral Movement",
            "meaning": (
                "This technique describes adversaries using removable media "
                "to introduce or propagate malicious content between systems."
            ),
            "indicator": "Removable-device connection activity",
            "relevance": (
                "A removable-device connection may provide context for an "
                "investigation. A connection by itself does not establish "
                "that files were copied, malware was introduced, or the "
                "device was used to move between systems."
            ),
            "investigation": [
                "Review available device connection events and timestamps.",
                "Identify the device and the system where the event occurred, if recorded.",
                "Check available file-access, transfer, and endpoint security logs.",
                "Seek evidence of malicious files or propagation before associating the event with this technique.",
            ],
            "limitation": (
                "A device connection alone does not demonstrate replication "
                "through removable media. Confirm the behavior with additional evidence."
            ),
        },
        "T1071": {
            "name": "Application Layer Protocol",
            "tactic": "Command and Control",
            "meaning": (
                "An adversary may use application-layer protocols, such as "
                "web protocols, to communicate with systems under their control."
            ),
            "indicator": "High web/HTTP activity",
            "relevance": (
                "Unusually high web activity may warrant investigation, but "
                "it can also result from legitimate browsing, software updates, "
                "or automated applications. Volume alone does not establish "
                "command-and-control communication."
            ),
            "investigation": [
                "Review request volume, timestamps, destinations, and available HTTP metadata.",
                "Compare the activity with the user's baseline and expected application behavior.",
                "Investigate unusual destinations, repeated patterns, and other suspicious indicators where data is available.",
                "Correlate with endpoint and network records before drawing a conclusion.",
            ],
            "limitation": (
                "High HTTP activity alone does not prove command-and-control "
                "traffic or malicious communication."
            ),
        },
    }

    # --------------------------------------------------------
    # Overview metrics
    # --------------------------------------------------------

    st.markdown("### 📊 Mapping Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Mapped Techniques",
            mitre_data["Technique"].nunique(),
        )

    with col2:
        st.metric(
            "Behavioral Indicators",
            mitre_data["TrustLog Indicator"].nunique(),
        )

    with col3:
        st.metric(
            "Techniques Requiring Context",
            len(mitre_data),
        )

    st.caption(
        "These figures describe the mappings documented on this page, "
        "not confirmed attacks or live detection counts."
    )

    st.divider()

    # --------------------------------------------------------
    # Search and mapping table
    # --------------------------------------------------------

    st.markdown("### 🔎 Explore Technique Mappings")

    search_text = st.text_input(
        "Search by technique, name, or indicator",
        placeholder="Example: T1078, HTTP, removable media",
        key="mitre_search",
    )

    filtered_mitre = mitre_data.copy()

    if search_text.strip():
        query = search_text.strip().lower()

        mask = filtered_mitre.astype(str).apply(
            lambda column: column.str.lower().str.contains(
                query, regex=False, na=False
            )
        ).any(axis=1)

        filtered_mitre = filtered_mitre[mask]

    st.dataframe(
        filtered_mitre,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "Technique IDs link behavioral observations to ATT&CK concepts; "
        "the mapping is contextual rather than a confirmed classification."
    )

    st.divider()

    # --------------------------------------------------------
    # Detailed technique explanations
    # --------------------------------------------------------

    st.markdown("### 📚 Technique-by-Technique Explanation")

    for technique_id, details in technique_details.items():

        with st.expander(
            f"{technique_id} — {details['name']}",
            expanded=False,
        ):
            st.markdown("**What does this technique mean?**")
            st.write(details["meaning"])

            st.markdown("**Associated ATT&CK tactic(s)**")
            st.write(details["tactic"])

            st.markdown("**TrustLog behavioral indicator**")
            st.info(details["indicator"])

            st.markdown("**Why is this indicator relevant?**")
            st.write(details["relevance"])

            st.markdown("**Suggested investigation steps**")

            for step_number, step in enumerate(
                details["investigation"], start=1
            ):
                st.markdown(f"{step_number}. {step}")

            st.markdown("**Interpretation and limitation**")
            st.warning(details["limitation"])

    st.divider()

    # --------------------------------------------------------
    # Analyst workflow
    # --------------------------------------------------------

    st.markdown("### 🕵️ Recommended Analyst Workflow")

    workflow_col1, workflow_col2 = st.columns(2)

    with workflow_col1:
        st.markdown(
            """
            <div class="info-card">
                <b>1. Identify</b><br>
                Review the behavioral indicator and the associated
                ATT&CK technique.
                <br><br>
                <b>2. Investigate</b><br>
                Examine relevant timestamps, user activity, and
                available supporting records.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with workflow_col2:
        st.markdown(
            """
            <div class="info-card">
                <b>3. Correlate</b><br>
                Compare the event with other indicators and available
                endpoint or network evidence.
                <br><br>
                <b>4. Verify evidence</b><br>
                Where a registered evidence record exists, use TrustLog's
                IPFS and blockchain verification workflow to check integrity.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="info-card">
            <b>Important distinction</b><br>
            MITRE ATT&CK provides a common language for describing
            adversary behavior. TrustLog's behavioral indicators can help
            analysts decide what to investigate. Blockchain verification
            can help establish whether registered evidence matches its
            recorded hash; it does not independently prove that the
            evidence is genuine or that a particular attack occurred.
        </div>
        """,
        unsafe_allow_html=True,
    )




# ============================================================
# PAGE 6 — IPFS EVIDENCE
# ============================================================

elif page == "IPFS Evidence":

    st.markdown(
        '<div class="section-title">📦 IPFS Evidence & Integrity</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            <b>Evidence storage and integrity</b><br>
            TrustLog stores evidence off-chain using IPFS and uses
            SHA-256 hashes and blockchain metadata to support integrity
            verification. A matching hash indicates that the checked
            file matches the recorded fingerprint; it does not by itself
            prove that the evidence is authentic.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # Existing configured evidence values — kept unchanged
    evidence_name = "high_risk_evidence.json"
    evidence_cid = "QmfJXJyPpK1AGiMy2jwvdt3dsomtpxSw79SUtizfzYYR46"
    evidence_hash = (
        "1882fae6c2ba99ec459c7d0ae613b986"
        "c641c8f2b4fb9ad1c8a49be0b7f16fc1"
    )
    gateway_url = "http://127.0.0.1:8080"

    # --------------------------------------------------------
    # Evidence overview
    # --------------------------------------------------------

    st.markdown("### 📋 Evidence Overview")

    overview1, overview2, overview3 = st.columns(3)

    with overview1:
        st.markdown(
            """
            <div class="metric-card metric-records">
                <div class="metric-label">Storage</div>
                <div class="metric-value">IPFS</div>
                <div class="metric-subtitle">Off-chain evidence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with overview2:
        st.markdown(
            """
            <div class="metric-card metric-anomalies">
                <div class="metric-label">Fingerprint</div>
                <div class="metric-value">SHA-256</div>
                <div class="metric-subtitle">Content integrity check</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with overview3:
        st.markdown(
            """
            <div class="metric-card metric-employees">
                <div class="metric-label">Evidence Reference</div>
                <div class="metric-value">CID</div>
                <div class="metric-subtitle">IPFS content identifier</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(
        "These cards describe the configured evidence workflow. "
        "They do not indicate live connectivity or successful verification."
    )

    st.divider()

    # --------------------------------------------------------
    # Evidence details
    # --------------------------------------------------------

    st.markdown("### 🔐 Registered Evidence Details")

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.markdown("**Evidence object**")
        st.code(evidence_name, language="text")

        st.markdown("**IPFS Content Identifier (CID)**")
        st.code(evidence_cid, language="text")

    with detail_col2:
        st.markdown("**SHA-256 fingerprint**")
        st.code(evidence_hash, language="text")

        st.markdown("**Local IPFS gateway**")
        st.code(gateway_url, language="text")

    st.link_button(
        "Open evidence in local IPFS gateway",
        f"{gateway_url}/ipfs/{evidence_cid}",
        use_container_width=False,
    )

    st.caption(
        "The gateway link works only when the local IPFS service is "
        "running and the referenced content is available."
    )

    st.divider()

    # --------------------------------------------------------
    # How integrity verification works
    # --------------------------------------------------------

    st.markdown("### 🔄 How TrustLog Verifies Evidence")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown(
            """
            <div class="info-card">
                <b>1. Store</b><br>
                Evidence content is stored off-chain in IPFS and
                referenced using its CID.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step2:
        st.markdown(
            """
            <div class="info-card">
                <b>2. Register</b><br>
                The evidence fingerprint and relevant metadata can
                be recorded in the blockchain registry.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step3:
        st.markdown(
            """
            <div class="info-card">
                <b>3. Verify</b><br>
                Calculate the file's SHA-256 hash again and compare
                it with the registered hash. A mismatch indicates
                that the content differs.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # --------------------------------------------------------
    # Interpretation guide
    # --------------------------------------------------------

    st.markdown("### 🧭 Interpreting Verification Results")

    st.markdown(
        """
        - **Hash match:** The checked file has the same SHA-256
          fingerprint as the recorded value.
        - **Hash mismatch:** The checked file differs from the
          content represented by the recorded fingerprint.
        - **Content unavailable:** The IPFS gateway may be unreachable,
          or the content may not be available from the current node.
        - **Blockchain record:** The record must be queried separately
          to confirm that the expected evidence metadata is registered.
        """
    )


    # --------------------------------------------------------
    # Live IPFS integrity verification
    # --------------------------------------------------------

    st.markdown("### 🧪 Live Integrity Verification")

    if st.button(
        "Verify IPFS Evidence Now",
        type="primary",
        key="verify_ipfs_evidence",
    ):
        with st.spinner("Checking IPFS and calculating SHA-256..."):
            st.session_state["ipfs_verification_result"] = get_api(
                "/api/ipfs/verify"
            )

    verification = st.session_state.get("ipfs_verification_result")

    if verification and verification.get("status") == "verified":

        if verification and verification.get("status") == "verified":
            st.success("VERIFIED — IPFS is reachable and the SHA-256 hash matches.")

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.metric("IPFS API", "Connected")
                st.metric("Retrieved Bytes", verification["bytes_retrieved"])

            with result_col2:
                st.metric("SHA-256 Match", "Yes")
                st.metric("IPFS Version", verification["ipfs_version"])

            with st.expander("View verification details"):
                st.write("**CID**")
                st.code(verification["cid"], language="text")

                st.write("**Expected SHA-256**")
                st.code(verification["expected_sha256"], language="text")

                st.write("**Calculated SHA-256**")
                st.code(verification["actual_sha256"], language="text")

        elif verification and verification.get("status") == "mismatch":
            st.error("HASH MISMATCH — The retrieved content differs from the expected fingerprint.")

            st.write("**Expected SHA-256**")
            st.code(verification.get("expected_sha256", "Unavailable"))

            st.write("**Calculated SHA-256**")
            st.code(verification.get("actual_sha256", "Unavailable"))

        elif verification:
            st.warning(
                "Verification could not complete: "
                + verification.get("message", "Unknown error")
            )

        else:
            st.error(
                "The verification API did not respond. "
                "Check that the FastAPI backend is running."
            )


    # --------------------------------------------------------
    # Blockchain registration comparison
    # --------------------------------------------------------

    st.divider()
    st.markdown("### ⛓️ Blockchain Registration Check")

    st.caption(
        "This check compares the verified IPFS content with the "
        "blockchain record for the corresponding evidence ID."
    )

    blockchain_evidence_id = st.text_input(
        "Evidence ID to verify on-chain",
        value="TRUSTLOG-HIGH-RISK-001",
        key="ipfs_blockchain_evidence_id",
    )

    if st.button(
        "Check Blockchain Registration",
        type="secondary",
        key="check_ipfs_blockchain",
    ):
        if not verification or verification.get("status") != "verified":
            st.warning(
                "Verify the IPFS content successfully before comparing "
                "it with the blockchain record."
            )
        elif not blockchain_evidence_id.strip():
            st.warning("Enter an evidence ID.")
        else:
            with st.spinner("Fetching the blockchain record..."):
                record = get_api(
                    "/api/blockchain/evidence/"
                    + blockchain_evidence_id.strip()
                )

            if record and record.get("status") == "success":
                cid_matches = (
                    record.get("ipfs_cid") == verification.get("cid")
                )
                hash_matches = (
                    record.get("sha256_hash", "").lower()
                    == verification.get("actual_sha256", "").lower()
                )

                if cid_matches and hash_matches:
                    st.success(
                        "BLOCKCHAIN MATCH — The registered CID and "
                        "SHA-256 match the verified IPFS evidence."
                    )
                else:
                    st.error(
                        "BLOCKCHAIN RECORD MISMATCH — The registered "
                        "CID and/or SHA-256 differs from the IPFS evidence."
                    )

                comparison = pd.DataFrame(
                    {
                        "Check": ["IPFS CID", "SHA-256"],
                        "IPFS value": [
                            verification.get("cid", ""),
                            verification.get("actual_sha256", ""),
                        ],
                        "Blockchain value": [
                            record.get("ipfs_cid", ""),
                            record.get("sha256_hash", ""),
                        ],
                        "Match": [
                            "Yes" if cid_matches else "No",
                            "Yes" if hash_matches else "No",
                        ],
                    }
                )

                st.dataframe(
                    comparison,
                    width="stretch",
                    hide_index=True,
                )

            elif record and "Evidence not found" in record.get("message", ""):
                st.warning(
                    "RECORD NOT FOUND — This evidence ID is not registered "
                    "in the current blockchain contract. The IPFS hash "
                    "check may still be successful, but on-chain registration "
                    "has not been established."
                )
            elif record:
                st.error(
                    "Blockchain lookup failed: "
                    + record.get("message", "Unknown error")
                )
            else:
                st.error(
                    "The blockchain API did not respond. Check that "
                    "FastAPI and Ganache are running."
                )



# ============================================================
# PAGE 7 — BLOCKCHAIN
# ============================================================


elif page == "Blockchain":

    st.markdown(
        '<div class="section-title">Blockchain Verification</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            TrustLog retrieves evidence metadata directly from the local
            Ethereum-compatible blockchain. The original evidence file
            remains in IPFS, while the blockchain stores its identifier,
            SHA-256 hash, CID, risk score, timestamp and recorder.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    evidence_id = st.text_input(
        "Evidence ID",
        value="TRUSTLOG-DEMO-001",
        help="Enter the ID of evidence registered on the current Ganache chain.",
    )

    if st.button("Fetch Blockchain Record", type="primary"):
        get_api.clear()

    if evidence_id.strip():
        blockchain_record = get_api(
            f"/api/blockchain/evidence/{evidence_id.strip()}"
        )

        if blockchain_record and blockchain_record.get("status") == "success":
            st.success("Evidence metadata retrieved from the live blockchain.")

            blockchain_data = pd.DataFrame(
                {
                    "Field": [
                        "Evidence ID",
                        "Smart Contract",
                        "SHA-256 Hash",
                        "IPFS CID",
                        "Risk Score",
                        "Timestamp (Unix)",
                        "Recorder Address",
                        "Blockchain",
                    ],
                    "Value": [
                        blockchain_record["evidence_id"],
                        blockchain_record["contract_address"],
                        blockchain_record["sha256_hash"],
                        blockchain_record["ipfs_cid"],
                        str(blockchain_record["risk_score"]),
                        str(blockchain_record["timestamp"]),
                        blockchain_record["recorder"],
                        f"Ganache / Chain ID {blockchain_record['chain_id']}",
                    ],
                }
            )

            st.dataframe(
                blockchain_data,
                width="stretch",
                hide_index=True,
            )

            st.caption(
                "This confirms that the record was retrieved from the contract. "
                "To verify a file's integrity, compare its SHA-256 hash with "
                "the registered hash using the tampering-check script."
            )

        elif blockchain_record:
            st.error(
                "Could not retrieve the evidence record: "
                + blockchain_record.get("message", "Unknown error")
            )
        else:
            st.error(
                "The blockchain API did not respond. Check that FastAPI "
                "and Ganache are running."
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
