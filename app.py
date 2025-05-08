import streamlit as st
import pandas as pd
import plotly.express as px

# Load the processed data
tourism_stats_data = pd.read_csv('data/tourism_statistics/processed/fta_data_cleaned.csv')
monuments_data = pd.read_csv('data/centrally_protected_monuments/processed/visitors_to_cpm_cleaned.csv')

# App title
st.title('India Culture & Tourism Dashboard')

# Section for Tourism Statistics
st.header('Tourism Statistics')
st.subheader('Tourist Arrivals to India')

# Show a sample of the tourism statistics data
st.write("### Sample of Tourism Statistics")
st.dataframe(tourism_stats_data.head())

# Plot some basic tourism statistics using Plotly
fig = px.line(tourism_stats_data, x='year', y='ftas_in_india_in_million_', title='Foreign Tourist Arrivals to India')
st.plotly_chart(fig)

# Section for Centrally Protected Monuments
st.header('Centrally Protected Monuments Data')
st.subheader('Visitor Data to ASI Monuments')

# Show a sample of the monuments data
st.write("### Sample of Centrally Protected Monuments Data")
st.dataframe(monuments_data.head())

# Plot a graph showing total visitors to monuments over the years
fig2 = px.line(monuments_data, x='_year', y='no__of_visitors___total', title='Visitors to ASI Monuments (Total)')
st.plotly_chart(fig2)

# You can add more visualizations, charts, or even filters to explore the data in greater detail
