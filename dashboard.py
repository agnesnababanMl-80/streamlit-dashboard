import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Konfigurasi halaman
import streamlit as st

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Judul halaman
st.title("Bike Sharing Dashboard")
st.markdown("Welcome to the Bike Sharing Dashboard!")


# Function untuk load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    # Preprocessing
    for df in [day_df, hour_df]:
        df["dteday"] = pd.to_datetime(df["dteday"])
        df["season"] = df["season"].map(
            {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
        )
        df["weathersit"] = df["weathersit"].map(
            {1: "Clear", 2: "Mist", 3: "Light Snow/Rain", 4: "Heavy Rain/Snow"}
        )

    return day_df, hour_df


# Load data
import pandas as pd

day_df, hour_df = load_data()

# Sidebar
st.sidebar.header("Dashboard Filters")

# Year filter
year_list = sorted(day_df["dteday"].dt.year.unique())
selected_year = st.sidebar.selectbox("Select Year", year_list)

# Season filter
season_list = day_df["season"].unique()
selected_seasons = st.sidebar.multiselect(
    "Select Season", season_list, default=season_list
)

# Filter dataframes
filtered_day_df = day_df[
    (day_df["dteday"].dt.year == selected_year)
    & (day_df["season"].isin(selected_seasons))
]
filtered_hour_df = hour_df[
    (hour_df["dteday"].dt.year == selected_year)
    & (hour_df["season"].isin(selected_seasons))
]

# Main content
st.title("🚲 Bike Sharing Dashboard")

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rentals = filtered_day_df["cnt"].sum()
    st.metric("Total Rentals", f"{total_rentals:,.0f}")

with col2:
    avg_daily_rentals = filtered_day_df["cnt"].mean()
    st.metric("Avg Daily Rentals", f"{avg_daily_rentals:.0f}")

with col3:
    peak_rentals = filtered_day_df["cnt"].max()
    st.metric("Peak Daily Rentals", f"{peak_rentals:,.0f}")

with col4:
    total_registered = filtered_day_df["registered"].sum()
    pct_registered = (total_registered / total_rentals) * 100
    st.metric("% Registered Users", f"{pct_registered:.1f}%")

# Charts
import plotly.express as px

col1, col2 = st.columns(2)

with col1:
    # Seasonal Pattern
    st.subheader("Seasonal Usage Pattern")
    season_data = filtered_day_df.groupby("season")["cnt"].mean().reset_index()
    fig_season = px.bar(
        season_data, x="season", y="cnt", title="Average Daily Rentals by Season"
    )
    st.plotly_chart(fig_season, use_container_width=True)

with col2:
    # Weather Pattern
    st.subheader("Weather Impact")
    weather_data = filtered_day_df.groupby("weathersit")["cnt"].mean().reset_index()
    fig_weather = px.bar(
        weather_data, x="weathersit", y="cnt", title="Average Daily Rentals by Weather"
    )
    st.plotly_chart(fig_weather, use_container_width=True)

# Hourly pattern
st.subheader("Hourly Usage Pattern")
hourly_data = filtered_hour_df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()
fig_hourly = px.line(
    hourly_data,
    x="hr",
    y="cnt",
    color="workingday",
    title="Average Hourly Rentals (Workingday vs Holiday)",
    labels={"hr": "Hour of Day", "cnt": "Average Rentals", "workingday": "Working Day"},
)
st.plotly_chart(fig_hourly, use_container_width=True)

# Monthly trend
st.subheader("Monthly Trend")
monthly_data = (
    filtered_day_df.set_index("dteday").resample("M")["cnt"].mean().reset_index()
)
fig_monthly = px.line(
    monthly_data, x="dteday", y="cnt", title="Monthly Average Rentals"
)
st.plotly_chart(fig_monthly, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "Data source: [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)"
)
