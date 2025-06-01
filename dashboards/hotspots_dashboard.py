import streamlit as st
import pandas as pd

def show():
    st.title("📍 Top Indian Tourist Hotspots")

    # Read the data
    data_path = "data/silver/top_indian_places_to_visit_2be00d71/top_indian_places_to_visit_2be00d71.parquet"
    data = pd.read_parquet(data_path)

    # Clean column names
    data.columns = data.columns.str.strip()

    # Rename for Streamlit map
    data = data.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})

    # Initialize session state for filters visibility
    if "show_filters" not in st.session_state:
        st.session_state.show_filters = False

    # Sidebar toggle button and filters
    with st.sidebar:
        if st.button("🔍 Show/Hide Filters"):
            st.session_state.show_filters = not st.session_state.show_filters

        if st.session_state.show_filters:
            st.header("Filters")
            zones = data["Zone"].dropna().unique()
            selected_zones = st.multiselect("Select Zone(s)", sorted(zones), default=sorted(zones))

            types = data["Type"].dropna().unique()
            selected_types = st.multiselect("Select Place Type(s)", sorted(types), default=sorted(types))
        else:
            selected_zones = data["Zone"].dropna().unique()
            selected_types = data["Type"].dropna().unique()

    # Filter the data
    filtered_data = data[
        data["Zone"].isin(selected_zones) & data["Type"].isin(selected_types)
    ]

    # KPIs
    total_places = filtered_data.shape[0]
    avg_rating = filtered_data["Google review rating"].mean() if total_places > 0 else 0
    avg_fee = filtered_data["Entrance Fee in INR"].mean() if total_places > 0 else 0
    avg_visit_time = filtered_data["time needed to visit in hrs"].mean() if total_places > 0 else 0
    total_google_reviews = filtered_data["Number of google review in lakhs"].sum() if total_places > 0 else 0

    # Display KPIs horizontally
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    kpi1.metric(label="🏛️ Total Places", value=total_places)
    kpi2.metric(label="⭐ Avg. Google Rating", value=f"{avg_rating:.2f}")
    kpi3.metric(label="💰 Avg. Entrance Fee (₹)", value=f"{avg_fee:.0f}")
    kpi4.metric(label="⏳ Avg. Visit Time (hrs)", value=f"{avg_visit_time:.1f}")
    kpi5.metric(label="📝 Total Google Reviews (lakhs)", value=f"{total_google_reviews:.2f}")

    # Ensure map has required columns
    if 'latitude' in filtered_data.columns and 'longitude' in filtered_data.columns and total_places > 0:
        st.subheader("🗺️ Map of Top Places to Visit")
        st.map(filtered_data[['latitude', 'longitude']])
    else:
        st.error("❌ Latitude and Longitude columns not found or no places found!")

    st.caption(
        "🗺️ Map displayed uses third-party tiles which may not reflect the official boundaries of India as per the Survey of India. "
        "For accurate boundaries, refer to official maps provided by the Government of India."
    )

    # Show table
    st.subheader("📋 Details of Selected Places")
    st.dataframe(
        filtered_data[[
            "Name", "City", "State", "Zone", "Type",
            "Google review rating", "Number of google review in lakhs", 
            "Entrance Fee in INR", "time needed to visit in hrs", 
            "Significance", "DSLR Allowed", "Best Time to visit"
        ]].sort_values(by="Google review rating", ascending=False)
    )
