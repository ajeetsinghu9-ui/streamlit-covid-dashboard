import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="COVID-19 Analytics Dashboard",
    page_icon="🦠",
    layout="wide"
)

# ==========================================
# COVID-19 ANALYTICS DASHBOARD
# ==========================================

# ------------------------------------------
# Page Configuration
# ------------------------------------------

# ------------------------------------------
# Dashboard Title
# ------------------------------------------

st.title("🦠 COVID-19 Analytics Dashboard")

st.markdown("### Welcome to the COVID-19 Analytics Dashboard")

st.write(
    "Use the filters from the sidebar to explore COVID-19 data."
)

# ------------------------------------------
# Load Dataset
# ------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("country_wise_latest.csv")
    return df

df = load_data()

# ------------------------------------------
# Sidebar
# ------------------------------------------

st.sidebar.header("🔍 Filter Data")

# WHO Region Filter
regions = sorted(df["WHO Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select WHO Region",
    options=regions,
    default=regions
)

# Filter Data
filtered_df = df[df["WHO Region"].isin(selected_regions)]

# Top Countries Slider
top_n = st.sidebar.slider(
    "Select Top Countries",
    min_value=5,
    max_value=20,
    value=10
)

# ------------------------------------------
# KPI Cards
# ------------------------------------------

st.subheader("📊 Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Confirmed",
        f"{filtered_df['Confirmed'].sum():,}"
    )

with col2:
    st.metric(
        "Total Deaths",
        f"{filtered_df['Deaths'].sum():,}"
    )

with col3:
    st.metric(
        "Total Recovered",
        f"{filtered_df['Recovered'].sum():,}"
    )

with col4:
    st.metric(
        "Total Active",
        f"{filtered_df['Active'].sum():,}"
    )

# ------------------------------------------
# Bar Chart
# ------------------------------------------

st.subheader("📊 Top Countries by Confirmed Cases")

top_countries = filtered_df.sort_values(
    by="Confirmed",
    ascending=False
).head(top_n)

fig = px.bar(
    top_countries,
    x="Country/Region",
    y="Confirmed",
    color="Confirmed",
    title="Top Countries by Confirmed Cases"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# Pie Chart
# ------------------------------------------

st.subheader("🥧 WHO Region Distribution")

region_data = (
    filtered_df.groupby("WHO Region")["Confirmed"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_data,
    names="WHO Region",
    values="Confirmed",
    title="Confirmed Cases by WHO Region",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# Scatter Plot
# ------------------------------------------

st.subheader("📈 Confirmed vs Deaths")

fig = px.scatter(
    filtered_df,
    x="Confirmed",
    y="Deaths",
    color="WHO Region",
    hover_name="Country/Region",
    size="Confirmed",
    title="Confirmed Cases vs Deaths",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------
# Dataset Preview
# ------------------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)