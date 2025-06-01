import streamlit as st
from dashboards import dtv_dashboard, fee_dashboard, fta_dashboard, protected_monuments_dashboard, eco_sensitive_dashboard

page = st.sidebar.selectbox("Choose a Dashboard", [
    "DTV Trends",
    "Foreign Exchange Earnings (FEE)",
    "Foreign Tourist Arrivals",
    "Protected Monuments Dashboard",
    "Eco-sensitive Zones Dashboard"
])

if page == "DTV Trends":
    dtv_dashboard.show()
elif page == "Foreign Exchange Earnings (FEE)":
    fee_dashboard.show()
elif page == "Foreign Tourist Arrivals":
    fta_dashboard.show()
elif page == "Protected Monuments Dashboard":
    protected_monuments_dashboard.show()
elif page == "Eco-sensitive Zones Dashboard":
    eco_sensitive_dashboard.show()
