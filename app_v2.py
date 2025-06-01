import streamlit as st
import pandas as pd
import os
from glob import glob

st.set_page_config(page_title="India Culture & Tourism Dashboard", layout="wide")

st.title("📊 India Culture & Tourism Dashboard")
st.markdown("Explore insights from cultural heritage, tourism, and environmental datasets.")

# ✅ Function to list all nested Parquet files
@st.cache_data(ttl=600)
def list_parquet_files():
    files = glob("data/silver/**/*.parquet", recursive=True)
    return {
        os.path.basename(f).replace(".parquet", "").replace("_", " ").title(): f
        for f in files
    }

# ✅ Load file list
file_map = list_parquet_files()

# ✅ Sidebar selector
selected_dataset = st.sidebar.selectbox("Choose a dataset to explore:", list(file_map.keys()))

if selected_dataset:
    # ✅ Read and display the selected Parquet file
    file_path = file_map[selected_dataset]
    try:
        df = pd.read_parquet(file_path)
        st.subheader(f"📁 {selected_dataset}")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📌 Dataset Overview")
        st.write("**Shape:**", df.shape)
        st.write("**Columns:**", list(df.columns))

        if st.checkbox("Show Summary Stats"):
            st.write(df.describe(include='all'))

        if st.checkbox("Enable Column Filter"):
            columns_to_show = st.multiselect("Select columns to display", df.columns.tolist(), default=df.columns.tolist())
            st.dataframe(df[columns_to_show], use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
