import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("Tourist Visit Trends in India (2018–2022)")

    # Load data
    df = pd.read_parquet("data/silver/domestic_tour_travels_2018_2022_d6a26721/domestic_tour_travels_2018_2022_d6a26721.parquet")

    

    # Rename columns for clarity
    df = df.rename(columns={
        "dtv__in_lakh_": "DTV (in lakh)",
        "ftv__in_lakh_": "FTV (in lakh)"
    })

    
    # Toggle selection
    options = st.multiselect(
        "Select tourist visit type(s) to visualize:",
        ["DTV (in lakh)", "FTV (in lakh)"],
        default=["DTV (in lakh)", "FTV (in lakh)"]
    )

     # Show metrics
    st.subheader("Key Metrics Summary")
    cols = st.columns(len(options))
    for i, col in enumerate(cols):
        col.metric(
            label=f"{options[i]}",
            value=f"{df[options[i]].max():,.1f} lakh",
            delta=f"{df[options[i]].iloc[-1] - df[options[i]].iloc[0]:+.1f} lakh (from 2018)"
        )

    # Plot line chart
    if options:
        st.subheader("Yearly Tourist Visits Trend")
        fig = px.line(
            df,
            x="year",
            y=options,
            markers=True,
            labels={"value": "Visits (in lakh)", "year": "Year", "variable": "Type"},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Bar Chart Comparison")
        fig_bar = px.bar(
            df,
            x="year",
            y=options,
            barmode="group",
            labels={"value": "Visits (in lakh)", "year": "Year"},
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    
    st.subheader("Raw Data Preview")
    st.dataframe(df)
