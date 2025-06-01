import streamlit as st
from dashboards import dtv_dashboard, fee_dashboard, fta_dashboard, protected_monuments_dashboard, eco_sensitive_dashboard, hotspots_dashboard

# Custom CSS for Dark Mode
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    [data-testid="stSidebar"] {
        background-color: #1F1F1F;
        color: #E0E0E0;
    }
    .main-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #BB86FC;
        margin-bottom: 0.2rem;
    }
    .subheader {
        font-size: 0.9rem;
        color: #CF6679;
        margin-bottom: 1rem;
    }
    hr {
        border-color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar header and menu
with st.sidebar:
    st.markdown('<div class="main-title">🧭 India Tourism & Culture</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Explore tourism trends, cultural heritage, and ecological insights.</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.selectbox("Choose a Dashboard", [
        "📍 Tourist Hotspots",
        "🏰 Protected Monuments",
        "🌿 Eco-sensitive Zones",
        "✈️ Foreign Tourist Arrivals",
        "💰 Foreign Exchange Earnings (FEE)",
        "🏞️ Domestic Tourist Visits (DTV)",
    ])

# Dashboard routing
dashboard_map = {
    "📍 Tourist Hotspots": hotspots_dashboard,
    "🏰 Protected Monuments": protected_monuments_dashboard,
    "🌿 Eco-sensitive Zones": eco_sensitive_dashboard,
    "✈️ Foreign Tourist Arrivals": fta_dashboard,
    "💰 Foreign Exchange Earnings (FEE)": fee_dashboard,
    "🏞️ Domestic Tourist Visits (DTV)": dtv_dashboard,
}

dashboard_map[page].show()