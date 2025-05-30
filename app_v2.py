import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="India Culture & Tourism Dashboard", layout="wide")

DATA_DIR = "data/silver"

# Map dataset folder name -> user-friendly titles
DATASET_TITLES = {
    "eco_sensitive_zones_2015_bfd2221e": "Eco Sensitive Zones (2015)",
    "domestic_tour_travels_2018_2022_d6a26721": "Domestic Tour Travels (2018-2022)",
    "monuments_funding_2016_2021_e9e638f4": "Monuments Funding (2016-2021)",
    "seasonal_temperature_1901_2019_7a6a9b18": "Seasonal Temperature (1901-2019)",
    "month_wise_break_up_of_non_residents_indians_arrivals_2018_2020_c1f4090c": "NRI Arrivals (2018-2020)",
    "foreign_tourist_arrivals_1981_2020_f9158194": "Foreign Tourist Arrivals (1981-2020)",
    "foreign_exchange_earnings_1991_2023_48bdf5cd": "Foreign Exchange Earnings (1991-2023)",
    "inbound_tourism_foreign_tourist_arrivals_of_non_resident_indians_and_internation_1d6144a3": "Inbound Tourism & NRIs",
    "year_wise_details_of_funds_allocated_by_the_archaeological_survey_of_india_for_c_2cde790f": "ASI Fund Allocations (Year-wise)",
    "number_of_visitors_to_centrally_protected_tickted_monuments_2019_20_2020_21_22eeb0f5": "Visitors to Centrally Protected Monuments (2019-22)",
    "state_ut_wise_number_of_beneficiaries_and_funds_released_for_preservation_and_de_8f0bb93a": "State/UT Beneficiaries & Funds Released",
    "monuments_under_encroachment_988b521c": "Monuments Under Encroachment",
    "pilgrimage_rejuvenation_and_spiritual_heritage_augmentation_drive_prashad_scheme_42a90b4c": "PRASHAD Scheme",
    "state_fairs_festivals_2014_2021_337926d0": "State Fairs & Festivals (2014-2021)",
}

# Cache load parquet for speed
@st.cache_data(show_spinner=True)
def load_dataset(dataset_folder_name):
    path = os.path.join(DATA_DIR, dataset_folder_name, f"{dataset_folder_name}.parquet")
    df = pd.read_parquet(path)
    return df

# Render dashboard charts per dataset
def plot_dashboard(dataset_name, df, filters=None):
    st.markdown(f"### Dashboard for {DATASET_TITLES.get(dataset_name, dataset_name)}")

    # Apply filters if any
    if filters:
        for col, val in filters.items():
            if val != "All" and col in df.columns:
                df = df[df[col] == val]

    # Example dashboards based on dataset_name with basic charts
    if dataset_name == "domestic_tour_travels_2018_2022_d6a26721":
        # Example columns: 'Year' and 'Number of Trips' - check first
        if 'Year' in df.columns and 'Number of Trips' in df.columns:
            trips_per_year = df.groupby('Year')['Number of Trips'].sum()
            st.line_chart(trips_per_year)
        else:
            st.info("Expected columns 'Year' and 'Number of Trips' not found for charts.")

    elif dataset_name == "monuments_funding_2016_2021_e9e638f4":
        if 'Year' in df.columns and 'Funds Allocated' in df.columns:
            funds_per_year = df.groupby('Year')['Funds Allocated'].sum()
            st.bar_chart(funds_per_year)
        else:
            st.info("Expected columns 'Year' and 'Funds Allocated' not found for charts.")

    elif dataset_name == "eco_sensitive_zones_2015_bfd2221e":
        if 'Zone Type' in df.columns:
            zone_counts = df['Zone Type'].value_counts()
            st.bar_chart(zone_counts)
        else:
            st.info("Expected column 'Zone Type' not found for charts.")

    else:
        st.write("No pre-built charts for this dataset. Showing data preview only.")

    st.markdown("---")

# Show filters popup modal
def show_filter_popup(df):
    # Prepare filters dictionary
    filters = {}
    st.markdown("### Filters")

    # Pick categorical columns for filtering
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    for col in cat_cols:
        unique_vals = df[col].dropna().unique()
        unique_vals_sorted = sorted(unique_vals)
        options = ["All"] + unique_vals_sorted
        selected = st.selectbox(f"Filter by {col}", options, key=f"filter_{col}")
        filters[col] = selected

    return filters

# Show dataset detail page
def show_dataset_detail(dataset_name):
    df = load_dataset(dataset_name)

    st.title(DATASET_TITLES.get(dataset_name, dataset_name))
    st.markdown(f"**Total rows:** {df.shape[0]} | **Total columns:** {df.shape[1]}")

    # Filter button icon
    with st.expander("Show Filters"):
        filters = show_filter_popup(df)
    apply_filters = st.button("Apply Filters")

    if apply_filters:
        applied_filters = {k: v for k, v in filters.items() if v != "All"}
        filtered_df = df.copy()
        for col, val in applied_filters.items():
            filtered_df = filtered_df[filtered_df[col] == val]
        plot_dashboard(dataset_name, filtered_df)
        st.markdown("### Filtered Data Preview")
        st.dataframe(filtered_df)
    else:
        plot_dashboard(dataset_name, df)
        st.markdown("### Data Preview")
        st.dataframe(df)

# Main app
def main():
    st.sidebar.title("Datasets")
    # Sidebar with equal sized buttons for datasets
    dataset_names = list(DATASET_TITLES.keys())
    selected_dataset = st.sidebar.radio("Select Dataset", dataset_names, format_func=lambda x: DATASET_TITLES.get(x, x))

    show_dataset_detail(selected_dataset)


if __name__ == "__main__":
    main()
