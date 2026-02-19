import streamlit as st
import pandas as pd
import plotly.express as px
import json

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Bridge 17",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------
# PREMIUM HIGH-CONTRAST UI
# ----------------------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white !important;
}

/* Force all text white */
html, body, [class*="css"] {
    color: white !important;
}

/* Headings */
h1 {
    font-size: 52px !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 38px !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 28px !important;
    font-weight: 600 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Cards */
.metric-card {
    background: rgba(255,255,255,0.12);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.section-card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 30px;
    backdrop-filter: blur(12px);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white !important;
    border-radius: 10px;
    height: 50px;
    font-weight: 700;
    font-size: 16px;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    transform: scale(1.03);
}

/* Metric styling */
[data-testid="stMetricValue"] {
    font-size: 32px !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 18px !important;
    color: #d1d5db !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD DATA
# ----------------------------
df_ngos = pd.read_csv("ngos.csv")
df_suppliers = pd.read_csv("suppliers.csv")

# ----------------------------
# SESSION STATE
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# ----------------------------
# DASHBOARD PAGE
# ----------------------------
def dashboard_page():

    st.markdown("<h1 style='text-align:center;'>🌍 Bridge 17 Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:lightgray;'>AI-powered SDG Partnership Intelligence Platform</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Metrics ----
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total NGOs", len(df_ngos))
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Suppliers", len(df_suppliers))
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("States Covered", df_ngos["state"].nunique())
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>")

    # ---- Charts ----
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("📊 SDG Distribution Overview")

    fig1 = px.histogram(df_ngos, x="sdg", title="NGO SDG Focus")
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       font=dict(color="white"))
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df_ngos, x="state", title="NGOs by State")
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(df_ngos, x="trust_score", title="Trust Score Distribution")
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Matchmaking Section ----
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("## 🤝 AI Partnership Matchmaking")

    st.markdown("""
Bridge 17’s AI Matchmaking Engine connects CSR initiatives 
with the most suitable NGOs and Suppliers using:

- 🎯 SDG Alignment  
- 📍 Geographic Matching  
- ⭐ Trust Score Ranking  
- 📊 Data-driven scoring
""")

    if st.button("🚀 Launch Matchmaking Engine"):
        st.session_state.page = "matchmaking"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# MATCHMAKING PAGE
# ----------------------------
def matchmaking_page():

    st.markdown("<h1 style='text-align:center;'>🤖 AI Matchmaking Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:lightgray;'>Precision Partner Discovery for Sustainable Development</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    mode = st.radio("Select Mode:",
                    ["Upload CSR File (Auto Match)",
                     "Manual Search"])

    if mode == "Upload CSR File (Auto Match)":

        uploaded_file = st.file_uploader("Upload CSR JSON file", type=["json"])

        if uploaded_file:
            csr_data = json.load(uploaded_file)

            sdg = csr_data.get("sdg")
            state = csr_data.get("state")

            matches = df_ngos[
                (df_ngos["sdg"] == sdg) &
                (df_ngos["state"] == state)
            ].sort_values(by="trust_score", ascending=False)

            st.success("Top Matches Found:")
            st.dataframe(matches)

    else:

        selected_sdg = st.selectbox("Select SDG", df_ngos["sdg"].unique())
        selected_state = st.selectbox("Select State", df_ngos["state"].unique())

        matches = df_ngos[
            (df_ngos["sdg"] == selected_sdg) &
            (df_ngos["state"] == selected_state)
        ].sort_values(by="trust_score", ascending=False)

        st.success("Top Matches:")
        st.dataframe(matches)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# ROUTER
# ----------------------------
if st.session_state.page == "dashboard":
    dashboard_page()
else:
    matchmaking_page()
