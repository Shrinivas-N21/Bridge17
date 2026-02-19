import streamlit as st
import pandas as pd
import json

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
# LOAD SUPPLIERS DATA
# ----------------------------
def load_suppliers():
    with open("suppliers.json", "r") as f:
        return pd.DataFrame(json.load(f))


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
            st.error("Please enter all fields")


# ----------------------------
# MAIN DASHBOARD
# ----------------------------
def main_dashboard():
    st.title("Bridge 17 Dashboard")

    df = load_suppliers()

    # ---- Sidebar ----
    with st.sidebar:
        st.title("Navigation")

        st.write(f"👤 {st.session_state.username}")
        st.write(f"🏢 {st.session_state.sector}")
        st.markdown("---")

        if st.button("View History"):
            st.subheader("Upload History")
            for item in st.session_state.history:
                st.write(item)

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.sector = None
            st.rerun()

    # ---- Dashboard Stats ----
    st.subheader("Supplier Overview")

    col1, col2 = st.columns(2)

    col1.metric("Total Suppliers", len(df))
    col2.metric("States Covered", df["state"].nunique())

    st.bar_chart(df["sdg_goal"].value_counts())

    st.markdown("---")

    # ---- CSR Upload ----
    st.subheader("Upload CSR Report")

    uploaded_file = st.file_uploader("Upload CSR Report (PDF or TXT)")

    if uploaded_file is not None:
        st.success("File uploaded successfully!")

        # Save history
        st.session_state.history.append(uploaded_file.name)

        st.markdown("### View Matching")

        if st.button("Find Matching Suppliers"):
            # Simple matching example
            sector = st.session_state.sector

            if sector == "NGO":
                matches = df[df["sdg_goal"].str.contains("SDG 6")]
            elif sector == "PSU":
                matches = df[df["sdg_goal"].str.contains("SDG 3")]
            else:
                matches = df[df["sdg_goal"].str.contains("SDG 4")]

            st.subheader("Matching Suppliers")
            st.dataframe(matches)


# ----------------------------
# ROUTING LOGIC
# ----------------------------
if not st.session_state.logged_in:
    login_page()
else:
    main_dashboard()
