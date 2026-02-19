import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Bridge 17",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df_ngos = pd.read_csv("ngos.csv")
df_csr = pd.read_csv("csr.csv")
df_suppliers = pd.read_csv("suppliers.csv")

# Clean column names
df_ngos.columns = df_ngos.columns.str.strip().str.lower()
df_csr.columns = df_csr.columns.str.strip().str.lower()
df_suppliers.columns = df_suppliers.columns.str.strip().str.lower()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# --------------------------------------------------
# PROFESSIONAL DARK UI
# --------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white !important;
}
html, body, [class*="css"] {
    color: white !important;
}
h1 { font-size: 50px !important; font-weight: 800 !important; }
h2 { font-size: 36px !important; font-weight: 700 !important; }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] * { color: white !important; }
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white !important;
    border-radius: 10px;
    height: 50px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------
def dashboard_page():

    st.markdown("<h1 style='text-align:center;'>🌍 Bridge 17 Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total NGOs", len(df_ngos))

    with col2:
        st.metric("Total CSR Entries", len(df_csr))

    with col3:
        st.metric("States Covered", df_ngos["state"].nunique())

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- NGO SDG Distribution ---
    st.subheader("📊 NGO SDG Distribution")
    fig1 = px.histogram(df_ngos, x="primary_sdg")
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- CSR Spending Overview ---
    st.subheader("💰 CSR Spending by State")
    fig2 = px.bar(df_csr, x="state", y="csr_amount")
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Negotiation Flexibility ---
    st.subheader("🤝 NGO ZOPA Flexibility Distribution")
    fig3 = px.histogram(df_ngos, x="zopa_flexibility")
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Launch Matchmaking Engine"):
        st.session_state.page = "matchmaking"
        st.rerun()


# --------------------------------------------------
# MATCHMAKING PAGE
# --------------------------------------------------
def matchmaking_page():

    st.markdown("<h1 style='text-align:center;'>🤖 AI Matchmaking Engine</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    selected_state = st.selectbox("Select State", sorted(df_ngos["state"].unique()))
    selected_sdg = st.selectbox("Select SDG", sorted(df_ngos["primary_sdg"].unique()))

    matches = df_ngos[
        (df_ngos["state"] == selected_state) &
        (df_ngos["primary_sdg"] == selected_sdg)
    ]

    if not matches.empty:
        st.success(f"Found {len(matches)} Matching NGOs")
        st.dataframe(matches)

        # Supplier matching
        supplier_matches = df_suppliers[
            (df_suppliers["state"] == selected_state) &
            (df_suppliers["primary_sdg"] == selected_sdg)
        ]

        st.subheader("🔧 Matching Suppliers")
        st.dataframe(supplier_matches)

    else:
        st.warning("No NGOs found for selected filters.")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


# --------------------------------------------------
# ROUTER
# --------------------------------------------------
if st.session_state.page == "dashboard":
    dashboard_page()
else:
    matchmaking_page()
