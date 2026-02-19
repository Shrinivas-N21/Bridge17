import streamlit as st
import pandas as pd
import json
import re

# ----------------------------
# SESSION STATE INITIALIZATION
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "sector" not in st.session_state:
    st.session_state.sector = None

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
# TEXT EXTRACTION HELPERS
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
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Please fill all fields.")


# ----------------------------
# MAIN DASHBOARD
# ----------------------------
def main_dashboard():

    df_suppliers = load_suppliers()
    df_ngos = load_ngos()

    # ---- Sidebar ----
    with st.sidebar:
        st.title("Bridge 17")
        st.write(f"👤 {st.session_state.username}")
        st.write(f"🏢 {st.session_state.sector}")
        st.markdown("---")

        if st.button("View Upload History"):
            st.subheader("Uploaded CSR Files")
            for file in st.session_state.history:
                st.write("•", file)

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.sector = None
            st.rerun()

    # ---- Dashboard Metrics ----
    st.title("Bridge 17 Dashboard")

    col1, col2 = st.columns(2)
    col1.metric("Total NGOs", len(df_ngos))
    col2.metric("Total Suppliers", len(df_suppliers))

    st.subheader("SDG Distribution (Suppliers)")
    st.bar_chart(df_suppliers["sdg_goal"].value_counts())

    st.markdown("---")

    # ----------------------------
    # MATCHING SECTION
    # ----------------------------
    st.subheader("Partnership Matching")

    mode = st.radio(
        "Choose Matching Mode",
        ["Auto Match via CSR Upload", "Manual Search"]
    )

    # =====================================================
    # AUTO MATCH MODE
    # =====================================================
    if mode == "Auto Match via CSR Upload":

        uploaded_file = st.file_uploader("Upload CSR Report (TXT only)")

        if uploaded_file is not None:

            content = uploaded_file.read().decode("utf-8")

            # Save history
            st.session_state.history.append(uploaded_file.name)

            detected_sdg = extract_sdg(content)
            detected_state = extract_state(content, df_suppliers["state"].unique())

            st.write(f"Detected SDG: {detected_sdg}")
            st.write(f"Detected State: {detected_state}")

            if st.button("Run Auto Matching"):

                if detected_sdg and detected_state:

                    matched_ngos = df_ngos[
                        (df_ngos["sdg_goal"].str.contains(detected_sdg, na=False)) &
                        (df_ngos["state"] == detected_state)
                    ].sort_values(by="trust_score", ascending=False).head(3)

                    matched_suppliers = df_suppliers[
                        (df_suppliers["sdg_goal"].str.contains(detected_sdg, na=False)) &
                        (df_suppliers["state"] == detected_state)
                    ].sort_values(by="reliability", ascending=False).head(3)

                    st.subheader("Top NGO Matches")
                    st.dataframe(matched_ngos)

                    st.subheader("Top Supplier Matches")
                    st.dataframe(matched_suppliers)

                else:
                    st.error("Could not detect SDG or State from CSR file.")

    # =====================================================
    # MANUAL SEARCH MODE
    # =====================================================
    elif mode == "Manual Search":

        selected_state = st.selectbox("Select State", df_suppliers["state"].unique())
        selected_sdg = st.selectbox("Select SDG", df_suppliers
