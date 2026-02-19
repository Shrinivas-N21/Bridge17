import streamlit as st
import pandas as pd
import plotly.express as px
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Bridge 17", layout="wide")

# -----------------------------
# SESSION INIT
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "matched_pair" not in st.session_state:
    st.session_state.matched_pair = None

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df_ngos = pd.read_csv("ngos.csv")
    df_csr = pd.read_csv("csr.csv")
    df_suppliers = pd.read_csv("suppliers.csv")
    return df_ngos, df_csr, df_suppliers

df_ngos, df_csr, df_suppliers = load_data()

# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.title("🔷 Bridge 17 – AI Partnership Architect")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Select Role", ["CSR", "NGO", "Supplier"])

    if st.button("Login"):
        # Demo login (customize later)
        if username and password:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Enter credentials")

# -----------------------------
# MATCHMAKING ENGINE
# -----------------------------
def matchmaking_page():
    st.header("🤝 AI Matchmaking Engine")

    selected_sdg = st.selectbox("Select SDG Focus", sorted(df_ngos["sdg"].unique()))

    ngos_filtered = df_ngos[df_ngos["sdg"] == selected_sdg]
    csr_filtered = df_csr[df_csr["sdg"] == selected_sdg]

    if st.button("Find Match"):
        if not ngos_filtered.empty and not csr_filtered.empty:
            ngo = ngos_filtered.sample(1).iloc[0]
            csr = csr_filtered.sample(1).iloc[0]

            st.session_state.matched_pair = (ngo, csr)

            st.success("Match Found!")
            st.write("### NGO Partner")
            st.write(ngo)

            st.write("### CSR Partner")
            st.write(csr)
        else:
            st.warning("No matching partners found for this SDG")

# -----------------------------
# BARGAINING TRIGGER
# -----------------------------
def bargaining_section():
    if st.session_state.matched_pair:
        st.header("🧠 AI Bargaining Simulation")

        if st.button("Start AI Negotiation"):
            ngo, csr = st.session_state.matched_pair

            # Placeholder logic (Replace with Cerebral API call)
            ngo_offer = random.randint(10000, 50000)
            csr_offer = random.randint(20000, 60000)

            st.write(f"NGO Proposal Budget: ₹{ngo_offer}")
            st.write(f"CSR Counter Offer: ₹{csr_offer}")

            if csr_offer >= ngo_offer:
                st.success("Agreement Reached ✅")
            else:
                st.error("Negotiation Failed ❌")

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
def dashboard_page():
    st.title("🌍 Bridge 17 Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(df_ngos, x="sdg", title="NGO SDG Focus")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.histogram(df_csr, x="sdg", title="CSR SDG Focus")
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(df_suppliers, x="sdg", title="Supplier SDG Focus")
    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# ROLE BASED ROUTING
# -----------------------------
def main_app():
    st.sidebar.title("Bridge 17")
    st.sidebar.write(f"Logged in as: {st.session_state.role}")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Matchmaking", "Bargaining"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.matched_pair = None
        st.rerun()

    if menu == "Dashboard":
        dashboard_page()
    elif menu == "Matchmaking":
        matchmaking_page()
    elif menu == "Bargaining":
        bargaining_section()

# -----------------------------
# APP ENTRY POINT
# -----------------------------
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
