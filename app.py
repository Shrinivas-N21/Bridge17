import streamlit as st
import pandas as pd
import plotly.express as px
import random

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="Bridge 17", layout="wide")

# ------------------------------------------------
# SESSION STATE INIT
# ------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "matched_pair" not in st.session_state:
    st.session_state.matched_pair = None

if "agreement" not in st.session_state:
    st.session_state.agreement = None

# ------------------------------------------------
# LOAD + CLEAN DATA
# ------------------------------------------------
@st.cache_data
def load_data():
    df_ngos = pd.read_csv("ngos.csv")
    df_csr = pd.read_csv("csr.csv")
    df_suppliers = pd.read_csv("suppliers.csv")

    # Normalize column names
    for df in [df_ngos, df_csr, df_suppliers]:
        df.columns = df.columns.str.strip().str.lower()

    # Ensure SDG column exists
    required_column = "sdg"

    for df in [df_ngos, df_csr, df_suppliers]:
        if required_column in df.columns:
            df["sdg"] = df["sdg"].astype(str)
            df["sdg"] = df["sdg"].str.split(",")
            df = df.explode("sdg")
            df["sdg"] = df["sdg"].str.strip()

    return df_ngos, df_csr, df_suppliers


df_ngos, df_csr, df_suppliers = load_data()

# ------------------------------------------------
# LOGIN PAGE
# ------------------------------------------------
def login_page():
    st.title("🔷 Bridge 17 – AI Partnership Architect")
    st.subheader("Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["CSR", "NGO", "Supplier"])

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Please enter credentials")

# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------
def dashboard_page():
    st.title("🌍 SDG Ecosystem Dashboard")

    if "sdg" not in df_ngos.columns:
        st.error("SDG column missing in dataset")
        st.write("Columns found:", df_ngos.columns)
        return

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(df_ngos, x="sdg", title="NGO SDG Focus")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.histogram(df_csr, x="sdg", title="CSR SDG Focus")
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(df_suppliers, x="sdg", title="Supplier SDG Focus")
    st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------------
# MATCHMAKING ENGINE
# ------------------------------------------------
def matchmaking_page():
    st.header("🤝 AI Matchmaking Engine")

    if "sdg" not in df_ngos.columns:
        st.error("SDG column missing")
        return

    sdg_options = sorted(df_ngos["sdg"].unique())

    selected_sdg = st.selectbox("Select SDG Focus", sdg_options)

    ngos_filtered = df_ngos[df_ngos["sdg"] == selected_sdg]
    csr_filtered = df_csr[df_csr["sdg"] == selected_sdg]

    if st.button("Find Match"):
        if not ngos_filtered.empty and not csr_filtered.empty:
            ngo = ngos_filtered.sample(1).iloc[0]
            csr = csr_filtered.sample(1).iloc[0]

            st.session_state.matched_pair = (ngo, csr)
            st.session_state.agreement = None

            st.success("Match Found!")

            st.subheader("NGO Partner")
            st.json(ngo.to_dict())

            st.subheader("CSR Partner")
            st.json(csr.to_dict())
        else:
            st.warning("No match found for this SDG")

# ------------------------------------------------
# AI BARGAINING (PLACEHOLDER FOR CEREBRAL API)
# ------------------------------------------------
def bargaining_page():
    st.header("🧠 AI Bargaining Simulation")

    if not st.session_state.matched_pair:
        st.info("No matched pair found. Please run matchmaking first.")
        return

    ngo, csr = st.session_state.matched_pair

    if st.button("Start AI Negotiation"):
        ngo_offer = random.randint(20000, 60000)
        csr_offer = random.randint(30000, 80000)

        st.write(f"NGO Budget Proposal: ₹{ngo_offer}")
        st.write(f"CSR Counter Offer: ₹{csr_offer}")

        if csr_offer >= ngo_offer:
            st.success("Agreement Reached ✅")
            st.session_state.agreement = {
                "ngo_budget": ngo_offer,
                "csr_commitment": csr_offer,
                "status": "Approved"
            }
        else:
            st.error("Negotiation Failed ❌")
            st.session_state.agreement = {
                "ngo_budget": ngo_offer,
                "csr_commitment": csr_offer,
                "status": "Rejected"
            }

# ------------------------------------------------
# AGREEMENT VIEW
# ------------------------------------------------
def agreement_page():
    st.header("📜 Partnership Agreement")

    if not st.session_state.agreement:
        st.info("No agreement available yet.")
        return

    st.json(st.session_state.agreement)

# ------------------------------------------------
# MAIN APP
# ------------------------------------------------
def main_app():
    st.sidebar.title("Bridge 17")
    st.sidebar.write(f"Logged in as: {st.session_state.role}")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Matchmaking", "Bargaining", "Agreement"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.matched_pair = None
        st.session_state.agreement = None
        st.rerun()

    if menu == "Dashboard":
        dashboard_page()
    elif menu == "Matchmaking":
        matchmaking_page()
    elif menu == "Bargaining":
        bargaining_page()
    elif menu == "Agreement":
        agreement_page()

# ------------------------------------------------
# ENTRY POINT
# ------------------------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
