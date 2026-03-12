"""
PHASE 4: INTERACTIVE DASHBOARD
Electricity Consumption Analysis in India
Module: Streamlit-based interactive dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Electricity Analysis Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .title-main {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data"""
    df = pd.read_csv("/home/claude/python_project/02_Data_Preparation/electricity_consumption_enhanced.csv")
    df['Dates'] = pd.to_datetime(df['Dates'])
    return df

@st.cache_data
def load_stats():
    """Load statistics"""
    with open("/home/claude/python_project/02_Data_Preparation/analysis_statistics.json", 'r') as f:
        return json.load(f)

def create_metric_cards(stats):
    """Create metric cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("2019 Total", f"₹{stats['total_2019']/1e5:.2f}L units", delta=None)
    
    with col2:
        st.metric("2020 Total", f"₹{stats['total_2020']/1e5:.2f}L units", 
                 delta=f"{stats['yoy_growth']:.1f}%")
    
    with col3:
        st.metric("Recovery Rate", f"+{stats['recovery_rate']:.2f}%", delta="Post-Lockdown")
    
    with col4:
        st.metric("States Analyzed", "33", delta="India-wide")

def create_filters(df):
    """Create sidebar filters"""
    st.sidebar.header("🔍 Filters")
    
    selected_states = st.sidebar.multiselect(
        "Select States",
        options=sorted(df['States'].unique()),
        default=sorted(df['States'].unique())[:5]
    )
    
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=sorted(df['Regions'].unique()),
        default=sorted(df['Regions'].unique())
    )
    
    selected_year = st.sidebar.multiselect(
        "Select Years",
        options=sorted(df['Year'].unique()),
        default=sorted(df['Year'].unique())
    )
    
    return selected_states, selected_regions, selected_year

def filter_data(df, states, regions, years):
    """Filter dataframe based on selections"""
    return df[
        (df['States'].isin(states)) &
        (df['Regions'].isin(regions)) &
        (df['Year'].isin(years))
    ]

def main():
    """Main dashboard application"""
    # Header
    st.markdown('<div class="title-main">⚡ Electricity Consumption Analysis Dashboard</div>', 
                unsafe_allow_html=True)
    st.markdown("**India (Jan 2019 - Dec 2020)** | 16,599 Records | 33 States | 5 Regions")
    st.divider()
    
    # Load data
    df = load_data()
    stats = load_stats()
    
    # Create filters
    selected_states, selected_regions, selected_years = create_filters(df)
    
    # Filter data
    filtered_df = filter_data(df, selected_states, selected_regions, selected_years)
    
    # Display metrics
    st.subheader("📊 Key Metrics")
    create_metric_cards(stats)
    st.divider()
    
    # Tab 1: Overview
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", "🗺️ Regional", "📅 Timeline", "🔐 Lockdown", "📋 Details"
    ])
    
    with tab1:
        st.subheader("Consumption Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            # Year-over-Year comparison
            yearly = filtered_df.groupby('Year')['Usage'].sum()
            fig_yearly = go.Figure(data=[
                go.Bar(x=yearly.index, y=yearly.values, marker_color=['#1f77b4', '#ff7f0e'])
            ])
            fig_yearly.update_layout(title="Yearly Consumption", height=400)
            st.plotly_chart(fig_yearly, use_container_width=True)
        
        with col2:
            # Top states
            top_states = filtered_df.groupby('States')['Usage'].sum().sort_values(ascending=False).head(10)
            fig_top = go.Figure(data=[
                go.Bar(x=top_states.values, y=top_states.index, orientation='h', marker_color='#2ca02c')
            ])
            fig_top.update_layout(title="Top 10 States", height=400)
            st.plotly_chart(fig_top, use_container_width=True)
    
    with tab2:
        st.subheader("Regional Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Regional bar chart
            regional = filtered_df.groupby('Regions')['Usage'].sum().sort_values(ascending=False)
            fig_regional = px.bar(
                x=regional.index, y=regional.values,
                labels={'x': 'Region', 'y': 'Consumption (Units)'},
                title="Consumption by Region"
            )
            st.plotly_chart(fig_regional, use_container_width=True)
        
        with col2:
            # Regional pie chart
            regional_full = filtered_df.groupby('Region_Full')['Usage'].sum()
            fig_pie = go.Figure(data=[go.Pie(labels=regional_full.index, values=regional_full.values)])
            fig_pie.update_layout(title="Regional Distribution", height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab3:
        st.subheader("Consumption Trends")
        
        # Monthly trend
        monthly = filtered_df.groupby(pd.Grouper(key='Dates', freq='M'))['Usage'].sum()
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=monthly.index, y=monthly.values, mode='lines+markers',
                                       name='Monthly Consumption', line=dict(color='#1f77b4', width=2)))
        fig_trend.update_layout(title="Monthly Consumption Trend", height=400, hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with tab4:
        st.subheader("Lockdown Impact Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            period_stats = filtered_df.groupby('Period')['Usage'].agg(['sum', 'mean'])
            fig_period = go.Figure(data=[
                go.Bar(x=period_stats.index, y=period_stats['sum'], name='Total Consumption')
            ])
            fig_period.update_layout(title="Total Usage by Period", height=400)
            st.plotly_chart(fig_period, use_container_width=True)
        
        with col2:
            period_avg = filtered_df.groupby('Period')['Usage'].mean()
            fig_avg = go.Figure(data=[
                go.Bar(x=period_avg.index, y=period_avg.values, 
                      marker_color=['#1f77b4', '#d62728', '#2ca02c'])
            ])
            fig_avg.update_layout(title="Average Daily Usage by Period", height=400)
            st.plotly_chart(fig_avg, use_container_width=True)
    
    with tab5:
        st.subheader("Data Details")
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(filtered_df))
        with col2:
            st.metric("States", filtered_df['States'].nunique())
        with col3:
            st.metric("Avg Daily Usage", f"{filtered_df['Usage'].mean():.2f}")
        
        st.divider()
        
        # Data table
        st.write("### Filtered Data Sample")
        display_cols = ['Dates', 'States', 'Regions', 'Usage', 'Year', 'Month_Name', 'Period']
        st.dataframe(
            filtered_df[display_cols].head(20),
            use_container_width=True,
            height=400
        )

if __name__ == "__main__":
    main()
