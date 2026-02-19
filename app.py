import streamlit as st
import pandas as pd
import json
import re

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Bridge 17",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------
# PREMIUM UI STYLING
# ----------------------------
st.markdown("""
<style>

/* Main Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Headings Bigger */
h1 {
    font-size: 52px !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 36px !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 28px !important;
}

/* Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(8px);
}

/* Section Cards */
.section-card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 30px;
    backdrop-filter: blur(10px);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 50px;
    font-weight: 600;
    font-size: 16px;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #0072ff, #00c6ff);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# SESSION STATE
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "sector" not in st.session_state:
    st.session_state.sector = None

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------
# LOAD DATA
# ----------------------------
def load_suppliers():
    with open("suppliers.json", "r") as f:
        return pd.DataFrame(json.load(f))

def load_ngos():
    with open("ngos.json", "r") as f:
        return pd.DataFrame(json.load(f))

# ----------------------------
# HELPERS
# ----------------------------
def extract_sdg(text):
    match = re.search(r"SDG\s?\d+", text)
    return match.group(0) if match else None

def extract_state(text, states):
    for state in states:
        if state.lower() in text.lower():
            return state
    return None

# ----------------------------
# LOGIN PAGE
# ----------------------------
def login_page():
    st.markdown("<h1 style='text-align:center;'>🌍 Bridge 17</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:lightgray;'>AI Partnership Architect</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    sector = st.selectbox("Select Sector", ["NGO", "PSU", "Government"])

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.sector = sector
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Please fill all fields.")

# ----------------------------
# DASHBOARD PAGE
# ----------------------------
def dashboard_page():

    df_suppliers = load_suppliers()
    df_ngos = load_ngos()

    st.markdown("<h1 style='text-align:center;'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:lightgray;'>Real-time SDG Partnership Intelligence</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics
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

    st.markdown("<br>", unsafe_allow_html=True)

    # SDG Distribution
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2>SDG Distribution Overview</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### NGOs by SDG")
        st.bar_chart(df_ngos["sdg_goal"].value_counts())

    with col2:
        st.markdown("### Suppliers by SDG")
        st.bar_chart(df_suppliers["sdg_goal"].value_counts())

    st.markdown("</div>", unsafe_allow_html=True)

    # State & Trust
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2>Geographic & Trust Insights</h2>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### NGOs by State")
        st.bar_chart(df_ngos["state"].value_counts())

    with col4:
        st.markdown("### Avg Trust Score by State")
        avg_trust = df_ngos.groupby("state")["trust_score"].mean()
        st.bar_chart(avg_trust)

    st.markdown("</div>", unsafe_allow_html=True)

    # Matchmaking Info
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2>🤝 AI Partnership Matchmaking</h2>", unsafe_allow_html=True)

    st.markdown("""
Bridge 17 intelligently connects CSR initiatives with the most suitable NGOs 
and Suppliers based on:

- 🎯 SDG Alignment  
- 📍 Geographic Location  
- ⭐ Trust & Reliability Scores  
- 📊 Data-driven ranking  

Launch the Matchmaking Engine to begin partner discovery.
""")

    if st.button("🚀 Launch Matchmaking Engine"):
        st.session_state.page = "matchmaking"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# MATCHMAKING PAGE
# ----------------------------
def matchmaking_page():

    df_suppliers = load_suppliers()
    df_ngos = load_ngos()

    st.markdown("<h1 style='text-align:center;'>🤖 AI Matchmaking Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:lightgray;'>Precision Partner Discovery Platform</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    mode = st.radio(
        "Choose Matching Mode",
        ["Auto Match via CSR Upload", "Manual Search"]
    )

    if mode == "Auto Match via CSR Upload":

        uploaded_file = st.file_uploader("Upload CSR Report (TXT only)")

        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8")
            st.session_state.history.append(uploaded_file.name)

            detected_sdg = extract_sdg(content)
            detected_state = extract_state(content, df_suppliers["state"].unique())

            st.write(f"Detected SDG: {detected_sdg}")
            st.write(f"Detected State: {detected_state}")

            if st.button("Run Auto Matching"):

                matched_ngos = df_ngos[
                    (df_ngos["sdg_goal"].str.contains(detected_sdg, na=False)) &
                    (df_ngos["state"] == detected_state)
                ].sort_values(by="trust_score", ascending=False)

                matched_suppliers = df_suppliers[
                    (df_suppliers["sdg_goal"].str.contains(detected_sdg, na=False)) &
                    (df_suppliers["state"] == detected_state)
                ].sort_values(by="reliability", ascending=False)

                st.subheader("Top NGO Matches")
                st.dataframe(matched_ngos.head(5))

                st.subheader("Top Supplier Matches")
                st.dataframe(matched_suppliers.head(5))

    elif mode == "Manual Search":

        selected_state = st.selectbox("Select State", df_ngos["state"].unique())
        selected_sdg = st.selectbox("Select SDG", df_ngos["sdg_goal"].unique())

        if st.button("Search"):

            matched_ngos = df_ngos[
                (df_ngos["sdg_goal"] == selected_sdg) &
                (df_ngos["state"] == selected_state)
            ].sort_values(by="trust_score", ascending=False)

            matched_suppliers = df_suppliers[
                (df_suppliers["sdg_goal"] == selected_sdg) &
                (df_suppliers["state"] == selected_state)
            ].sort_values(by="reliability", ascending=False)

            st.subheader("Matching NGOs")
            st.dataframe(matched_ngos)

            st.subheader("Matching Suppliers")
            st.dataframe(matched_suppliers)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
# ----------------------------
def sidebar():
    with st.sidebar:
        st.title("Bridge 17")
        st.write(f"👤 {st.session_state.username}")
        st.write(f"🏢 {st.session_state.sector}")
        st.markdown("---")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "dashboard"
            st.rerun()

# ----------------------------
# ROUTING
# ----------------------------
if not st.session_state.logged_in:
    login_page()
else:
    sidebar()
    if st.session_state.page == "dashboard":
        dashboard_page()
    elif st.session_state.page == "matchmaking":
        matchmaking_page()
