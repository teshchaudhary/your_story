import streamlit as st
import pandas as pd
import os
import glob
import altair as alt

st.set_page_config(page_title="India Culture & Tourism Insights", layout="wide")
st.title("🇮🇳 India Culture & Tourism Dashboard")

DATA_FOLDER = "data/silver"

@st.cache_data(ttl=600)
def list_dataset_folders(path):
    return sorted([f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))])

@st.cache_data(ttl=600)
def load_parquet_from_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, "*.parquet"))
    if not files:
        return None
    return pd.read_parquet(files[0])

# Dataset selection
dataset_folders = list_dataset_folders(DATA_FOLDER)
selected_dataset = st.selectbox("📁 Select a Dataset", dataset_folders)

if selected_dataset:
    folder_path = os.path.join(DATA_FOLDER, selected_dataset)
    df = load_parquet_from_folder(folder_path)

    if df is not None:
        # Detect types
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        year_col = next((col for col in df.columns if col.lower() == "year"), None)
        category_cols = df.select_dtypes(include=["object"]).columns.tolist()

        st.subheader(f"📊 {selected_dataset}: Interactive Dashboard")

        # Section 1: Year-over-Year Trend
        if year_col and numeric_cols:
            st.markdown("### 📈 Trend Over Time")
            y_col = st.selectbox("Choose a numeric metric", [col for col in numeric_cols if col != year_col], key="metric")
            trend_df = df[[year_col, y_col]].dropna().sort_values(by=year_col)

            chart = alt.Chart(trend_df).mark_line(point=True).encode(
                x=alt.X(f"{year_col}:O", title="Year"),
                y=alt.Y(f"{y_col}:Q", title=y_col),
                tooltip=[year_col, y_col]
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)

            if trend_df.shape[0] >= 2:
                latest, prev = trend_df.iloc[-1][y_col], trend_df.iloc[-2][y_col]
                growth = (latest - prev) / prev * 100 if prev != 0 else 0
                st.metric(f"📈 YoY Change in {y_col}", f"{growth:.2f}%", delta=f"{latest - prev:,.0f}")

        # Section 2: Category-wise Breakdown
        if year_col and category_cols and numeric_cols:
            st.markdown("### 🧭 Top Categories Over Time")
            cat_col = st.selectbox("Choose a category column", category_cols, key="cat_col")
            num_col = st.selectbox("Choose a numeric value", numeric_cols, key="num_col")
            grouped = df[[year_col, cat_col, num_col]].dropna()
            top_categories = grouped.groupby(cat_col)[num_col].sum().nlargest(5).index.tolist()
            filtered = grouped[grouped[cat_col].isin(top_categories)]

            chart = alt.Chart(filtered).mark_line(point=True).encode(
                x=alt.X(f"{year_col}:O", title="Year"),
                y=alt.Y(f"{num_col}:Q", title=num_col),
                color=cat_col,
                tooltip=[year_col, cat_col, num_col]
            ).properties(height=400)

            st.altair_chart(chart, use_container_width=True)

        # Section 3: Quick Stats
        st.markdown("### 🧮 Quick Stats")
        st.markdown(f"**Shape:** `{df.shape[0]:,}` rows × `{df.shape[1]:,}` columns")
        st.markdown("**Columns:**")
        st.write(df.columns.tolist())

        # Section 4: Preview
        with st.expander("🔍 Preview Raw Data (Top 100 Rows)"):
            st.dataframe(df.head(100), use_container_width=True)

        # Section 5: Column-wise Filtering
        with st.expander("📌 Column Filtering & Selection"):
            selected_columns = st.multiselect("Select columns to view", options=df.columns.tolist(), default=df.columns.tolist())
            if selected_columns:
                st.dataframe(df[selected_columns].head(100), use_container_width=True)

        # Section 6: Descriptive Stats
        with st.expander("📉 Descriptive Statistics"):
            st.dataframe(df.describe(include="all").T, use_container_width=True)

    else:
        st.error("❌ No parquet file found in the selected folder.")
