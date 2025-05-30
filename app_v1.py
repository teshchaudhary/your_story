import streamlit as st
import pandas as pd
import os
import glob
import altair as alt

st.set_page_config(page_title="India Culture & Tourism Insights (Local Silver Parquet)", layout="wide")
st.title("India Culture & Tourism Insights Dashboard (Local Silver Parquet Files)")

DATA_FOLDER = "data/silver"

@st.cache_data(ttl=600)
def list_dataset_folders(path):
    # List all folders inside silver folder
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return sorted(folders)

@st.cache_data(ttl=600)
def load_parquet_from_folder(folder_path):
    # Find the single parquet file inside the folder
    files = glob.glob(os.path.join(folder_path, "*.parquet"))
    if not files:
        return None
    return pd.read_parquet(files[0])

# List dataset folders
dataset_folders = list_dataset_folders(DATA_FOLDER)
selected_dataset = st.selectbox("Select dataset to load", dataset_folders)

if selected_dataset:
    folder_path = os.path.join(DATA_FOLDER, selected_dataset)
    df = load_parquet_from_folder(folder_path)
    
    if df is not None:
        st.subheader(f"Preview of `{selected_dataset}`")
        st.dataframe(df.head(100))
        
        st.markdown(f"**Rows:** {df.shape[0]}  |  **Columns:** {df.shape[1]}")

        columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns to display", options=columns, default=columns)

        if selected_columns:
            st.dataframe(df[selected_columns].head(100))
        
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        year_col = None
        for col in ["YEAR", "year"]:
            if col in df.columns:
                year_col = col
                break
        
        if year_col and numeric_cols:
            numeric_cols_for_plot = [col for col in numeric_cols if col != year_col]
            y_col = st.selectbox("Select numeric column to plot over years", numeric_cols_for_plot)
            if y_col:
                chart_df = df[[year_col, y_col]].dropna()
                chart = alt.Chart(chart_df).mark_line(point=True).encode(
                    x=alt.X(f"{year_col}:O", title=year_col),
                    y=alt.Y(f"{y_col}:Q", title=y_col),
                    tooltip=[year_col, y_col]
                ).properties(width=700, height=400)
                st.altair_chart(chart, use_container_width=True)
    else:
        st.error("No parquet file found inside the selected folder.")
