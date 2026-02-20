import streamlit as st
import pandas as pd
import requests
import io

st.title('🎯 Lead Scoring')

st.markdown("""
Upload your leads data (CSV format) to get AI-powered lead scores.
The system will analyze each lead and provide a score from 0-1 indicating conversion likelihood.
""")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)

        st.success(f"Successfully loaded {len(df)} leads")

        # Display first few rows
        st.subheader('Preview of Uploaded Data')
        st.dataframe(df.head())

        # Score leads button
        if st.button('Score Leads', type='primary'):
            with st.spinner('Scoring leads... This may take a moment.'):

                # Prepare data for API
                # Convert DataFrame to dict for JSON serialization
                leads_data = df.to_dict('records')

                try:
                    # Call the backend API
                    response = requests.post(
                        'http://localhost:5000/api/predict',
                        json={'leads': leads_data},
                        timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()

                        if 'predictions' in result:
                            # Add scores to dataframe
                            df['lead_score'] = result['predictions']

                            st.success('Lead scoring completed!')

                            # Display results
                            st.subheader('Scoring Results')

                            # Summary statistics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Average Score", f"{df['lead_score'].mean():.3f}")
                            with col2:
                                high_score_leads = (df['lead_score'] > 0.7).sum()
                                st.metric("High Score Leads (>0.7)", high_score_leads)
                            with col3:
                                low_score_leads = (df['lead_score'] < 0.3).sum()
                                st.metric("Low Score Leads (<0.3)", low_score_leads)

                            # Score distribution
                            st.subheader('Score Distribution')
                            score_bins = pd.cut(df['lead_score'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                                              labels=['0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0'])
                            score_dist = score_bins.value_counts().sort_index()
                            st.bar_chart(score_dist)

                            # Top scored leads
                            st.subheader('Top 10 Highest Scored Leads')
                            top_leads = df.nlargest(10, 'lead_score')[['lead_score']]
                            st.dataframe(top_leads)

                            # Download results
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="Download Scored Leads CSV",
                                data=csv,
                                file_name='scored_leads.csv',
                                mime='text/csv'
                            )

                        else:
                            st.error("Invalid response format from API")

                    else:
                        st.error(f"API request failed with status code {response.status_code}")
                        st.text(response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to scoring API: {str(e)}")
                    st.info("Make sure the backend server is running on http://localhost:5000")

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please ensure your CSV file has proper headers and data format.")

else:
    st.info("Please upload a CSV file to get started.")

    # Sample data format
    st.subheader('Expected CSV Format')
    sample_data = {
        'age': [30, 45, 25],
        'job': ['technician', 'manager', 'student'],
        'marital': ['single', 'married', 'single'],
        'education': ['secondary', 'tertiary', 'primary'],
        'balance': [1000, 5000, 200]
    }
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df)
    st.info("Your CSV should contain lead information with columns like age, job, marital status, education, etc.")
