import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df = pd.read_parquet("data/silver/eco_sensitive_zones_2015_bfd2221e/eco_sensitive_zones_2015_bfd2221e.parquet")
    df.columns = df.columns.str.strip()
    return df

def show():
    st.title("Eco-sensitive Zones (ESZ) Dashboard")

    df = load_data()
    if df is None or df.empty:
        st.warning("No data available to display.")
        return

    # Sidebar filters with "All" option
    states = sorted(df['state'].dropna().unique())
    states_with_all = ["All"] + states

    selected_states = st.sidebar.multiselect("Select States / UTs", options=states_with_all, default=["All"])

    # Handle "All" selection
    if "All" in selected_states or len(selected_states) == 0:
        df_filtered = df.copy()  # No filtering if "All" selected or nothing selected
    else:
        df_filtered = df[df['state'].isin(selected_states)]

    # Sidebar toggle to show raw data
    show_raw = st.sidebar.checkbox("Show Raw Data")

    # KPIs in main area
    total_states = df_filtered['state'].nunique()
    total_complete_proposals = df_filtered['number_of_complete_esz_proposals_with_the_ministry'].sum()
    total_approved_notified = df_filtered['number_of_esz_proposals_approved_notified'].sum()
    total_protected_areas = df_filtered['number_of_protected_areas_covered_under_the_approved_notified_esz_proposals'].sum()
    total_to_be_notified = df_filtered['number_of_esz_proposals_to_be_notified'].sum()

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    kpi_col4, kpi_col5 = st.columns(2)

    kpi_col1.metric("States / UTs Covered", total_states)
    kpi_col2.metric("Complete Proposals with Ministry", f"{total_complete_proposals:,}")
    kpi_col3.metric("Approved / Notified Proposals", f"{total_approved_notified:,}")
    kpi_col4.metric("Protected Areas Covered", f"{total_protected_areas:,}")
    kpi_col5.metric("Proposals To Be Notified", f"{total_to_be_notified:,}")

    st.markdown("---")

    if show_raw:
        st.subheader("Raw Eco-sensitive Zones Data")
        st.dataframe(df_filtered.reset_index(drop=True))

    # Plot: Approved / Notified Proposals by State
    st.subheader("Approved / Notified ESZ Proposals by State / UT")
    plt.figure(figsize=(10,6))
    sns.barplot(
        data=df_filtered.sort_values('number_of_esz_proposals_approved_notified', ascending=False),
        x='state',
        y='number_of_esz_proposals_approved_notified',
        palette='viridis'
    )
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("State / UT")
    plt.ylabel("Approved / Notified Proposals")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

    # Plot: Protected Areas Covered by State
    st.subheader("Protected Areas Covered Under Approved Proposals")
    plt.figure(figsize=(10,6))
    sns.barplot(
        data=df_filtered.sort_values('number_of_protected_areas_covered_under_the_approved_notified_esz_proposals', ascending=False),
        x='state',
        y='number_of_protected_areas_covered_under_the_approved_notified_esz_proposals',
        palette='magma'
    )
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("State / UT")
    plt.ylabel("Protected Areas Covered")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
