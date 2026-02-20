import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

st.title('📊 MarketMind Dashboard')

# Load data
try:
    sales_df = pd.read_csv('../../data/sales_data.csv')
    sales_df['date'] = pd.to_datetime(sales_df['date'])
except Exception as e:
    st.error(f"Error loading sales data: {e}")
    sales_df = pd.DataFrame()

try:
    leads_df = pd.read_csv('../../data/bank_marketing.csv', sep=';')
except Exception as e:
    st.error(f"Error loading leads data: {e}")
    leads_df = pd.DataFrame()

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = sales_df['sales'].sum() if not sales_df.empty else 0
    st.metric("Total Sales", f"${total_sales:,.0f}")

with col2:
    total_leads = len(leads_df) if not leads_df.empty else 0
    st.metric("Total Leads", f"{total_leads:,}")

with col3:
    avg_lead_score = 0.5  # Placeholder
    st.metric("Avg Lead Score", f"{avg_lead_score:.2f}")

with col4:
    conversion_rate = 0.12  # Placeholder
    st.metric("Conversion Rate", f"{conversion_rate:.1%}")

# Sales Trend Chart
st.subheader('Sales Trend')
if not sales_df.empty:
    fig = px.line(sales_df, x='date', y='sales', title='Sales Over Time')
    st.plotly_chart(fig)
else:
    st.info("No sales data available for trend analysis")

# Lead Distribution
st.subheader('Lead Analysis')
if not leads_df.empty:
    col1, col2 = st.columns(2)

    with col1:
        # Job distribution
        job_counts = leads_df['job'].value_counts().head(10)
        fig = px.bar(job_counts, title='Top Job Categories')
        st.plotly_chart(fig)

    with col2:
        # Education distribution
        education_counts = leads_df['education'].value_counts()
        fig = px.pie(education_counts, title='Education Distribution', names=education_counts.index, values=education_counts.values)
        st.plotly_chart(fig)

    # Age distribution
    st.subheader('Age Distribution')
    fig = px.histogram(leads_df, x='age', nbins=20, title='Lead Age Distribution')
    st.plotly_chart(fig)
else:
    st.info("No leads data available for analysis")

# Recent Activity
st.subheader('Recent Activity')
st.info("Dashboard shows key metrics and visualizations for sales and lead data.")
st.info("Connect to backend APIs for real-time data and predictions.")
