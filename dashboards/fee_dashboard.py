import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    filepath = "data/silver/foreign_exchange_earnings_1991_2023_48bdf5cd/foreign_exchange_earnings_1991_2023_48bdf5cd.parquet"
    try:
        df = pd.read_parquet(filepath)
    except Exception as e:
        st.error(f"Failed to load data from {filepath}: {e}")
        return None
    return df

def show():
    st.title("Foreign Exchange Earnings (FEE) Dashboard")
    
    df = load_data()
    if df is None or df.empty:
        st.warning("No data available to display.")
        return
    
    # Sidebar filters
    years = df['year'].sort_values().unique()
    min_year, max_year = int(years.min()), int(years.max())
    year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
    df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Display raw data toggle
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Raw Foreign Exchange Earnings Data")
        st.dataframe(df_filtered.reset_index(drop=True))
    
    # KPIs
    st.subheader("Key Performance Indicators")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    total_fee_crore = df_filtered['fee_in_terms_crore'].sum()
    total_fee_usd = df_filtered['fee_in_us_terms_us_million'].sum()
    
    # Average growth in INR and USD
    avg_growth_inr = df_filtered['fee_in_terms_change_over_previous_year'].mean()
    avg_growth_usd = df_filtered['fee_in_us_terms_change_over_previous_year'].mean()
    
    kpi_col1.metric("Total FEE (Crore INR)", f"{total_fee_crore:,.0f}")
    kpi_col2.metric("Total FEE (Million USD)", f"{total_fee_usd:,.0f}")
    kpi_col3.metric("Avg. Yearly Growth (INR %)", f"{avg_growth_inr:.2f}%")
    kpi_col4.metric("Avg. Yearly Growth (USD %)", f"{avg_growth_usd:.2f}%")
    
    # Plot trends
    st.subheader("FEE Trends Over Time")
    fig_trends = plot_fee_trends(df_filtered)
    st.pyplot(fig_trends)
    
    # Plot yearly % changes
    st.subheader("Yearly % Change in FEE")
    fig_changes = plot_fee_changes(df_filtered)
    st.pyplot(fig_changes)
    
    # Highlight years with dips/spikes
    st.subheader("Years with Significant Change (> ±30%)")
    highlight_years = df_filtered[
        (df_filtered['fee_in_terms_change_over_previous_year'].abs() > 30) |
        (df_filtered['fee_in_us_terms_change_over_previous_year'].abs() > 30)
    ]
    if not highlight_years.empty:
        st.dataframe(highlight_years[['year', 'fee_in_terms_change_over_previous_year', 'fee_in_us_terms_change_over_previous_year']])
    else:
        st.write("No significant changes detected in selected year range.")

def plot_fee_trends(df):
    # plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=(10,5))
    
    ax.plot(df['year'], df['fee_in_terms_crore'], marker='o', label='FEE (Crore INR)')
    ax.plot(df['year'], df['fee_in_us_terms_us_million'], marker='x', label='FEE (Million USD)')
    
    ax.set_xlabel("Year")
    ax.set_ylabel("Foreign Exchange Earnings")
    ax.set_title("Foreign Exchange Earnings (FEE) Trends")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

def plot_fee_changes(df):
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=(10,5))
    
    ax.bar(df['year'] - 0.2, df['fee_in_terms_change_over_previous_year'], width=0.4, label='INR % Change')
    ax.bar(df['year'] + 0.2, df['fee_in_us_terms_change_over_previous_year'], width=0.4, label='USD % Change')
    
    ax.set_xlabel("Year")
    ax.set_ylabel("Yearly % Change")
    ax.set_title("Yearly Percentage Change in FEE")
    ax.legend()
    plt.xticks(rotation=45)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.tight_layout()
    
    return fig
