import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np

st.title('📈 Sales Forecasting')

st.markdown("""
Predict future sales trends using historical data and AI-powered forecasting models.
Upload your sales data or use sample data to generate forecasts.
""")

# Data input options
data_option = st.radio(
    'Choose data source:',
    ['Upload CSV', 'Use Sample Data', 'Connect to Database']
)

df = pd.DataFrame()

if data_option == 'Upload CSV':
    uploaded_file = st.file_uploader("Upload sales data (CSV)", type=['csv'])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} records")

            # Display data preview
            st.subheader('Data Preview')
            st.dataframe(df.head())

            # Column selection
            date_col = st.selectbox('Select date column', df.columns)
            value_col = st.selectbox('Select value column to forecast', df.columns)

            if date_col and value_col:
                # Convert date column
                try:
                    df[date_col] = pd.to_datetime(df[date_col])
                    df = df.sort_values(date_col)
                except:
                    st.error("Could not parse date column. Please ensure it contains valid dates.")

        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

elif data_option == 'Use Sample Data':
    # Generate sample sales data
    dates = pd.date_range(start='2023-01-01', end='2024-12-01', freq='M')
    np.random.seed(42)
    sales = 10000 + np.cumsum(np.random.normal(500, 200, len(dates)))

    df = pd.DataFrame({
        'date': dates,
        'sales': sales.astype(int)
    })

    st.success("Using sample sales data")
    st.dataframe(df.head())

    date_col = 'date'
    value_col = 'sales'

# Forecasting parameters
if not df.empty:
    st.subheader('Forecasting Parameters')

    col1, col2 = st.columns(2)

    with col1:
        periods = st.slider('Forecast periods (months)', 1, 24, 12)
        confidence_level = st.slider('Confidence level (%)', 80, 99, 95)

    with col2:
        model_type = st.selectbox('Forecasting model',
                                ['Simple Exponential Smoothing',
                                 'Holt-Winters',
                                 'ARIMA',
                                 'Prophet'])

    # Generate forecast button
    if st.button('Generate Forecast', type='primary'):
        with st.spinner('Generating forecast...'):

            try:
                # Prepare data for API
                historical_data = df[value_col].tolist()

                # Call forecasting API
                response = requests.post(
                    'http://localhost:5000/forecast',
                    json={
                        'data': historical_data,
                        'periods': periods,
                        'model': model_type
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    if 'forecast' in result:
                        forecast_values = result['forecast']

                        st.success('Forecast generated successfully!')

                        # Create forecast dataframe
                        last_date = df[date_col].max()
                        forecast_dates = pd.date_range(start=last_date, periods=periods+1, freq='M')[1:]

                        forecast_df = pd.DataFrame({
                            'date': forecast_dates,
                            'forecasted_sales': forecast_values
                        })

                        # Display results
                        st.subheader('Forecast Results')

                        # Summary metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            avg_forecast = np.mean(forecast_values)
                            st.metric("Average Forecast", f"${avg_forecast:,.0f}")
                        with col2:
                            growth_rate = ((forecast_values[-1] - forecast_values[0]) / forecast_values[0]) * 100
                            st.metric("Growth Rate", f"{growth_rate:.1f}%")
                        with col3:
                            max_forecast = max(forecast_values)
                            st.metric("Peak Forecast", f"${max_forecast:,.0f}")

                        # Forecast visualization
                        st.subheader('Forecast Visualization')

                        # Combine historical and forecast data
                        hist_df = df[[date_col, value_col]].copy()
                        hist_df.columns = ['date', 'value']
                        hist_df['type'] = 'Historical'

                        forecast_df_plot = forecast_df.copy()
                        forecast_df_plot.columns = ['date', 'value']
                        forecast_df_plot['type'] = 'Forecast'

                        combined_df = pd.concat([hist_df, forecast_df_plot])

                        fig = go.Figure()

                        # Historical data
                        hist_data = combined_df[combined_df['type'] == 'Historical']
                        fig.add_trace(go.Scatter(
                            x=hist_data['date'],
                            y=hist_data['value'],
                            mode='lines+markers',
                            name='Historical',
                            line=dict(color='blue')
                        ))

                        # Forecast data
                        forecast_data = combined_df[combined_df['type'] == 'Forecast']
                        fig.add_trace(go.Scatter(
                            x=forecast_data['date'],
                            y=forecast_data['value'],
                            mode='lines+markers',
                            name='Forecast',
                            line=dict(color='red', dash='dash')
                        ))

                        fig.update_layout(
                            title='Sales Forecast',
                            xaxis_title='Date',
                            yaxis_title='Sales ($)',
                            hovermode='x unified'
                        )

                        st.plotly_chart(fig)

                        # Forecast table
                        st.subheader('Forecast Details')
                        st.dataframe(forecast_df)

                        # Download forecast
                        csv = forecast_df.to_csv(index=False)
                        st.download_button(
                            label="Download Forecast CSV",
                            data=csv,
                            file_name='sales_forecast.csv',
                            mime='text/csv'
                        )

                    else:
                        st.error("Invalid response format from forecasting API")

                else:
                    st.error(f"API request failed with status code {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to forecasting API: {str(e)}")
                st.info("Make sure the backend server is running on http://localhost:5000")

else:
    st.info("Please select a data source to get started with forecasting.")

# Help section
with st.expander('How to use forecasting'):
    st.markdown("""
    **Data Requirements:**
    - CSV file with date and value columns
    - Dates should be in a recognizable format (YYYY-MM-DD)
    - Values should be numeric (sales amounts, quantities, etc.)

    **Forecasting Models:**
    - **Simple Exponential Smoothing**: Good for data with no trend or seasonality
    - **Holt-Winters**: Suitable for data with trend and seasonality
    - **ARIMA**: Advanced statistical model for time series analysis
    - **Prophet**: Facebook's forecasting tool, good for business data

    **Tips:**
    - More historical data generally leads to better forecasts
    - Choose appropriate confidence levels based on your risk tolerance
    - Review forecast accuracy periodically and adjust models as needed
    """)
