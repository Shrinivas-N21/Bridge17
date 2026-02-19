import streamlit as st
import pandas as pd
import json
import re

# ----------------------------
# SESSION STATE INIT
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
    st.title("Bridge 17 – AI Partnership Architect")

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

    st.title("📊 Bridge 17 Analytics Dashboard")

    # ---- Metrics ----
    col1, col2, col3 = st.columns(3)

    col1.metric("Total NGOs", len(df_ngos))
    col2.metric("Total Suppliers", len(df_suppliers))
    col3.metric("States Covered", df_ngos["state"].nunique())

    st.markdown("---")

    # ---- Analytics Charts ----
    st.subheader("SDG Distribution Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### NGOs by SDG")
        st.bar_chart(df_ngos["sdg_goal"].value_counts())

    with col2:
        st.markdown("### Suppliers by SDG")
        st.bar_chart(df_suppliers["sdg_goal"].value_counts())

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### NGOs by State")
        st.bar_chart(df_ngos["state"].value_counts())

    with col4:
        st.markdown("### Average NGO Trust Score by State")
        avg_trust = df_ngos.groupby("state")["trust_score"].mean()
        st.bar_chart(avg_trust)

    st.markdown("---")

    # ---- Matchmaking Info Section ----
    st.subheader("🤝 AI Partnership Matchmaking")

    st.info(
        """
        The Matchmaking Engine automatically connects CSR initiatives 
        with the most suitable NGOs and Suppliers based on:
        
        • SDG alignment  
        • Geographic location  
        • Trust & Reliability scores  
        
        You can either upload a CSR report for automatic matching 
        or manually search by State and SDG.
        """
    )

    if st.button("Go to Matchmaking"):
        st.session_state.page = "matchmaking"
        st.rerun()


# ----------------------------
# MATCHMAKING PAGE
# ----------------------------
def matchmaking_page():

    df_suppliers = load_suppliers()
    df_ngos = load_ngos()

    st.title("🤖 AI Matchmaking Engine")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("---")

    mode = st.radio(
        "Choose Matching Mode",
        ["Auto Match via CSR Upload", "Manual Search"]
    )

    # ------------------------
    # AUTO MATCH
    # ------------------------
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

    # ------------------------
    # MANUAL SEARCH
    # ------------------------
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


# ----------------------------
# SIDEBAR GLOBAL
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
