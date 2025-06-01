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

    if "show_filters" not in st.session_state:
        st.session_state.show_filters = False

    # Sidebar toggle for filters
    with st.sidebar:
        if st.button("🔍 Show/Hide Filters"):
            st.session_state.show_filters = not st.session_state.show_filters

    # Sidebar checkbox for showing raw data
    show_raw = st.sidebar.checkbox("Show Raw Data")

    # Sidebar filters only when toggled on
    if st.session_state.show_filters:
        with st.sidebar:
            states = sorted(df['state'].dropna().unique())
            states_with_all = ["All"] + states
            selected_states = st.multiselect("Select States / UTs", options=states_with_all, default=["All"])
    else:
        selected_states = ["All"]

    # Handle "All" selection
    if "All" in selected_states or len(selected_states) == 0:
        df_filtered = df.copy()
    else:
        df_filtered = df[df['state'].isin(selected_states)]

    # Calculate KPIs
    total_states = df_filtered['state'].nunique()
    total_complete_proposals = df_filtered['number_of_complete_esz_proposals_with_the_ministry'].sum()
    total_approved_notified = df_filtered['number_of_esz_proposals_approved_notified'].sum()
    total_protected_areas = df_filtered['number_of_protected_areas_covered_under_the_approved_notified_esz_proposals'].sum()
    total_to_be_notified = df_filtered['number_of_esz_proposals_to_be_notified'].sum()

    # Improved KPI layout with emojis and single row
    kpi_cols = st.columns(5)
    kpi_cols[0].metric("🏞 States / UTs Covered", total_states)
    kpi_cols[1].metric("📄 Complete Proposals", f"{total_complete_proposals:,}")
    kpi_cols[2].metric("✅ Approved / Notified", f"{total_approved_notified:,}")
    kpi_cols[3].metric("🛡 Protected Areas", f"{total_protected_areas:,}")
    kpi_cols[4].metric("🕒 Proposals To Be Notified", f"{total_to_be_notified:,}")

    st.markdown("---")

    if show_raw:
        st.subheader("Raw Eco-sensitive Zones Data")
        st.dataframe(df_filtered.reset_index(drop=True))

    plt.style.use('dark_background')

    approved_palette = sns.color_palette("bright", n_colors=1)
    protected_palette = sns.color_palette("pastel", n_colors=1)

    st.subheader("Approved / Notified ESZ Proposals by State / UT")
    plt.figure(figsize=(10,6))
    sns.barplot(
        data=df_filtered.sort_values('number_of_esz_proposals_approved_notified', ascending=False),
        x='state',
        y='number_of_esz_proposals_approved_notified',
        color=approved_palette[0]
    )
    plt.xticks(rotation=45, ha='right', color='white')
    plt.xlabel("State / UT", color='white')
    plt.ylabel("Approved / Notified Proposals", color='white')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

    st.subheader("Protected Areas Covered Under Approved Proposals")
    plt.figure(figsize=(10,6))
    sns.barplot(
        data=df_filtered.sort_values('number_of_protected_areas_covered_under_the_approved_notified_esz_proposals', ascending=False),
        x='state',
        y='number_of_protected_areas_covered_under_the_approved_notified_esz_proposals',
        color=protected_palette[0]
    )
    plt.xticks(rotation=45, ha='right', color='white')
    plt.xlabel("State / UT", color='white')
    plt.ylabel("Protected Areas Covered", color='white')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
