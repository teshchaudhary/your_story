import streamlit as st
import pandas as pd
import altair as alt

def load_data():
    df = pd.read_parquet("data/silver/number_of_visitors_to_centrally_protected_tickted_monuments_2019_20_2020_21_22eeb0f5/number_of_visitors_to_centrally_protected_tickted_monuments_2019_20_2020_21_22eeb0f5.parquet")
    df.columns = df.columns.str.strip()  # Clean column names
    return df

def show():
    st.title("🕌 Centrally Protected Monuments Visitor Dashboard")

    df = load_data()

    # Initialize session state variable for filters visibility if not present
    if "show_filters" not in st.session_state:
        st.session_state.show_filters = False

    # Sidebar toggle button to show/hide filters
    if st.sidebar.button("🔍 Show/Hide Filters"):
        st.session_state.show_filters = not st.session_state.show_filters

    # Sidebar checkbox for showing raw data
    show_raw = st.sidebar.checkbox("Show Raw Data")

    # Filters section (conditionally shown)
    if st.session_state.show_filters:
        circles = sorted(df["Circle"].unique())
        selected_circle = st.sidebar.selectbox("Select Circle", ["All"] + circles)
        if selected_circle != "All":
            df = df[df["Circle"] == selected_circle]

        monument_list = sorted(df["Name of the Monument"].unique())
        selected_monument = st.sidebar.selectbox("Select Monument", ["All"] + monument_list)
        if selected_monument != "All":
            df = df[df["Name of the Monument"] == selected_monument]

    # ========== KPI Section ==========
    st.markdown("## 🔢 Key Performance Indicators")

    total_domestic_2019 = df["Domestic-2019-20"].sum()
    total_foreign_2019 = df["Foreign-2019-20"].sum()
    total_domestic_2020 = df["Domestic-2020-21"].sum()
    total_foreign_2020 = df["Foreign-2020-21"].sum()

    domestic_drop_pct = ((total_domestic_2020 - total_domestic_2019) / total_domestic_2019) * 100
    foreign_drop_pct = ((total_foreign_2020 - total_foreign_2019) / total_foreign_2019) * 100

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("🏠 Domestic Visitors (2019–20)", f"{total_domestic_2019:,}")
    kpi2.metric("🌍 Foreign Visitors (2019–20)", f"{total_foreign_2019:,}")
    kpi3.metric("📉 Domestic Growth", f"{domestic_drop_pct:.2f}%", delta=f"{domestic_drop_pct:.2f}%")
    kpi4.metric("📉 Foreign Growth", f"{foreign_drop_pct:.2f}%", delta=f"{foreign_drop_pct:.2f}%")

    st.divider()

    # ========== Visitor Trend Charts ==========
    st.subheader("📈 Visitor Trends (Domestic vs Foreign)")
    for year in ["2019-20", "2020-21"]:
        st.markdown(f"#### Year: {year}")
        chart_data = df[["Name of the Monument", f"Domestic-{year}", f"Foreign-{year}"]].copy()
        chart_data = chart_data.melt(id_vars="Name of the Monument", var_name="Visitor Type", value_name="Count")

        bar_chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Count:Q", title="Visitor Count"),
            y=alt.Y("Name of the Monument:N", sort="-x", title="Monument"),
            color="Visitor Type:N",
            tooltip=["Visitor Type", "Count"]
        ).properties(width=700, height=400)

        st.altair_chart(bar_chart)

    # ========== Top Monuments ==========
    st.subheader("🔥 Top 10 Most Visited Monuments (2019-20)")
    df["Total Visitors 2019-20"] = df["Domestic-2019-20"] + df["Foreign-2019-20"]
    top_10 = df.nlargest(10, "Total Visitors 2019-20")
    st.bar_chart(top_10.set_index("Name of the Monument")["Total Visitors 2019-20"])

    # ========== Growth Table ==========
    st.subheader("📉 % Growth in Visitors (2020-21 vs 2019-20)")
    growth_df = df[[
        "Name of the Monument", 
        "% Growth 2021-21/2019-20-Domestic", 
        "% Growth 2021-21/2019-20-Foreign"
    ]].copy()
    st.dataframe(growth_df.sort_values("% Growth 2021-21/2019-20-Domestic", ascending=True))

    # Show raw data preview if checked
    if show_raw:
        st.subheader("Raw Data Preview")
        st.dataframe(df)
