import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard Configuration
st.set_page_config(page_title="HabTrak Analyst Insights", layout="wide")

st.title("📈 HabTrak.ai | Behavioral Analytics Dashboard")
st.markdown("Automated insight engine correlating habit consistency with mood outcomes.")

@st.cache_data
def load_data():
    df = pd.read_csv("habit_mood_dataset.csv")
    
    # 1. Identify all habit columns (those starting with 'Habit_')
    habit_cols = [col for col in df.columns if col.startswith('Habit_')]
    
    # 2. Reshape data from 'Wide' to 'Long' (The Analyst Move)
    df_long = df.melt(
        id_vars=['User_ID', 'Date', 'Mood_Score', 'HRV_ms'], 
        value_vars=habit_cols, 
        var_name='Habit', 
        value_name='Completed'
    )
    
    # 3. Clean up habit names (e.g., 'Habit_Gym' -> 'Gym')
    df_long['Habit'] = df_long['Habit'].str.replace('Habit_', '').str.replace('_', ' ')
    
    # 4. Calculate 7-day rolling consistency per user/habit
    # This creates the 'habit_consistency' metric we need for the chart
    df_long = df_long.sort_values(['User_ID', 'Habit', 'Date'])
    df_long['Consistency'] = df_long.groupby(['User_ID', 'Habit'])['Completed'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    
    return df_long

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Analytics")
selected_habits = st.sidebar.multiselect(
    "Select Habits to Analyze", 
    options=df['Habit'].unique(),
    default=df['Habit'].unique()[:3] # Default to first 3
)

# Filter the data
filtered_df = df[df['Habit'].isin(selected_habits)]

# High-Level Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Data Points", f"{len(df):,}")
col2.metric("Avg. Mood Score", f"{df['Mood_Score'].mean():.2f}")
col3.metric("Avg. HRV (Recovery)", f"{df['HRV_ms'].mean():.1f}ms")

# Visualization: Correlation
st.subheader("Behavioral Correlation: Consistency vs. Mood")
st.markdown("This chart uses a **7-day rolling average** to show how habit consistency impacts reported mood.")

fig = px.scatter(
    filtered_df, 
    x="Consistency", 
    y="Mood_Score", 
    color="Habit", 
    trendline="ols",
    labels={"Consistency": "7-Day Habit Consistency (0 to 1)", "Mood_Score": "Mood Score (1-10)"},
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# Analyst Insight Box
st.info("**Analyst Note:** The slopes of the trendlines represent the 'Impact Factor' of each habit. A steeper line indicates that consistency in that specific habit has a stronger correlation with higher mood scores.")