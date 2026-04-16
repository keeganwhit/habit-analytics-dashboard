import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard Configuration
st.set_page_config(page_title="HabTrak Analyst Insights", layout="wide")

# Title & Description
st.title("📈 HabTrak.ai | Behavioral Analytics Dashboard")
st.markdown("Automated insight engine correlating habit consistency with mood outcomes.")

# Load your 18,000 row dataset
@st.cache_data
def load_data():
    df = pd.read_csv("habit_mood_dataset.csv")
    return df

df = load_data()

# Sidebar Filters (Analyst Touch)
st.sidebar.header("Filter Analytics")
habit_filter = st.sidebar.multiselect("Select Habits to Correlate", options=df['habit_name'].unique())

# High-Level Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Logs", f"{len(df):,}")
col2.metric("Unique Users", df['user_id'].nunique())
col3.metric("Avg. Mood Score", round(df['mood_score'].mean(), 2))

# The "Analyst" Visualization: Correlation
st.subheader("Habit Impact Analysis")
fig = px.scatter(df, x="habit_consistency", y="mood_score", 
                 color="habit_name", trendline="ols",
                 title="Correlation: Habit Consistency vs. Mood")
st.plotly_chart(fig, use_container_width=True)