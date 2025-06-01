import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    file_path = "data/silver/foreign_tourist_arrivals_1981_2020_f9158194/foreign_tourist_arrivals_1981_2020_f9158194.parquet"
    df = pd.read_parquet(file_path)
    df = df.rename(columns={
        "year": "Year",
        "ftas_in_india_in_million_": "FTA (Million)",
        "percentage_change_over_previous_year": "FTA % Change",
        "nris_arrivals_in_india_in_million_": "NRIs (Million)",
        "ercentage_change_over_the_previous_year": "NRIs % Change",
        "international_tourist_arrivals_in_india_in_million_": "International Tourists (Million)",
        "percentage_change_over_the_previous_year": "International Tourists % Change"
    })
    return df

def show():
    st.title("📊 Foreign Tourist Arrivals (FTA) in India (1981-2021)")

    df = load_data()

    if 'show_filters' not in st.session_state:
        st.session_state.show_filters = False

    if st.sidebar.button("🔍 Show/Hide Filters"):
        st.session_state.show_filters = not st.session_state.show_filters

    if st.session_state.show_filters:
        year_min, year_max = int(df['Year'].min()), int(df['Year'].max())
        selected_years = st.sidebar.slider("Select Year Range", year_min, year_max, (year_min, year_max))
        filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    else:
        filtered_df = df

    # Checkbox for showing raw data in sidebar
    show_data = st.sidebar.checkbox("Show raw data")

    latest_year = filtered_df['Year'].max()
    latest_data = filtered_df[filtered_df['Year'] == latest_year].iloc[0]

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric(label="Latest Year", value=latest_year)
    kpi2.metric(label="FTA (Million)", value=f"{latest_data['FTA (Million)']:.2f}")
    kpi3.metric(label="FTA % Change YoY", value=f"{latest_data['FTA % Change']:.2f} %")
    kpi4.metric(label="NRIs (Million)", value=f"{latest_data['NRIs (Million)']:.2f}")
    kpi5.metric(label="International Tourists (Million)", value=f"{latest_data['International Tourists (Million)']:.2f}")

    plt.style.use('dark_background')

    st.subheader("Arrivals Over Years (in Millions)")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_df, x='Year', y='FTA (Million)', marker='o', label='FTA')
    sns.lineplot(data=filtered_df, x='Year', y='NRIs (Million)', marker='o', label='NRIs')
    sns.lineplot(data=filtered_df, x='Year', y='International Tourists (Million)', marker='o', label='International Tourists')
    plt.ylabel("Arrivals (Million)")
    plt.grid(color='gray', linestyle='--', linewidth=0.7)
    plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

    st.subheader("Year-over-Year Percentage Changes")
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.patch.set_facecolor('#121212')

    sns.barplot(data=filtered_df, x='Year', y='FTA % Change', ax=axs[0], color='skyblue')
    axs[0].set_title("FTA % Change")
    axs[0].grid(color='gray', linestyle='--', linewidth=0.7)
    axs[0].set_facecolor('#121212')
    axs[0].axhline(0, color='white', linestyle='--')

    sns.barplot(data=filtered_df, x='Year', y='NRIs % Change', ax=axs[1], color='lightgreen')
    axs[1].set_title("NRIs % Change")
    axs[1].grid(color='gray', linestyle='--', linewidth=0.7)
    axs[1].set_facecolor('#121212')
    axs[1].axhline(0, color='white', linestyle='--')

    sns.barplot(data=filtered_df, x='Year', y='International Tourists % Change', ax=axs[2], color='salmon')
    axs[2].set_title("International Tourists % Change")
    axs[2].grid(color='gray', linestyle='--', linewidth=0.7)
    axs[2].set_facecolor('#121212')
    axs[2].axhline(0, color='white', linestyle='--')

    for ax in axs:
        ax.set_xlabel('')
        ax.tick_params(colors='white')
        ax.title.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, color='white')

    plt.xlabel("Year", color='white')
    st.pyplot(fig)
    plt.clf()

    if show_data:
        st.dataframe(filtered_df)
