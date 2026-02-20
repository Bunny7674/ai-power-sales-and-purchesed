import streamlit as st
import requests
import json

st.title('✍️ AI Content Generator')

st.markdown("""
Generate compelling marketing content using AI. Choose your content type and provide details for personalized copy.
""")

# Content type selection
content_type = st.selectbox(
    'Content Type',
    ['Email Campaign', 'Social Media Post', 'Product Description', 'Blog Post', 'Ad Copy', 'Landing Page Headline']
)

# Content parameters
col1, col2 = st.columns(2)

with col1:
    target_audience = st.text_input('Target Audience', placeholder='e.g., young professionals, small business owners')

with col2:
    tone = st.selectbox('Tone', ['Professional', 'Casual', 'Friendly', 'Urgent', 'Persuasive', 'Educational'])

# Main content input
prompt = st.text_area(
    'Content Details',
    height=100,
    placeholder='Describe what you want to promote, key benefits, unique selling points, or specific requirements...'
)

# Advanced options
with st.expander('Advanced Options'):
    max_length = st.slider('Maximum Length (words)', 50, 500, 200)
    include_cta = st.checkbox('Include Call-to-Action', value=True)
    provider = st.selectbox('AI Provider', ['Grok', 'Doodle'], index=0)

# Generate button
if st.button('Generate Content', type='primary'):
    if not prompt.strip():
        st.error('Please provide content details')
    else:
        with st.spinner('Generating content...'):

            # Prepare the API request
            full_prompt = f"""
            Create {content_type.lower()} content with the following specifications:
            - Target audience: {target_audience}
            - Tone: {tone}
            - Maximum length: {max_length} words
            - Include CTA: {'Yes' if include_cta else 'No'}

            Content details: {prompt}

            Please generate high-quality, engaging content that would convert well.
            """

            try:
                # Call the backend API
                response = requests.post(
                    'http://localhost:5000/generate-content',
                    json={
                        'prompt': full_prompt,
                        'provider': provider
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    if 'content' in result and result['content']:
                        st.success('Content generated successfully!')

                        # Display generated content
                        st.subheader('Generated Content')
                        content = result['content']

                        # Try to format as markdown if it looks like it
                        if any(char in content for char in ['#', '*', '-', '1.']):
                            st.markdown(content)
                        else:
                            st.write(content)

                        # Copy button (using text area for easy copying)
                        st.text_area('Copy Content', content, height=200)

                        # Additional actions
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button('Regenerate'):
                                st.rerun()
                        with col2:
                            st.download_button(
                                'Download as Text',
                                content,
                                file_name='generated_content.txt',
                                mime='text/plain'
                            )
                        with col3:
                            # Simple email share (placeholder)
                            st.button('Share via Email')

                    elif 'error' in result:
                        st.error(f"Generation failed: {result['error']}")
                    else:
                        st.error("Unexpected response format from API")

                else:
                    st.error(f"API request failed with status code {response.status_code}")
                    try:
                        error_details = response.json()
                        st.text(f"Error details: {error_details}")
                    except:
                        st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to content generation API: {str(e)}")
                st.info("Make sure the backend server is running on http://localhost:5000")

# Examples section
st.subheader('Content Examples')
with st.expander('See Examples'):
    examples = {
        'Email Campaign': 'Promote a new software tool for small businesses, emphasizing ease of use and cost savings.',
        'Social Media Post': 'Announce a limited-time discount on premium subscription plans.',
        'Product Description': 'Describe a smart home security camera with AI features and mobile app integration.',
        'Blog Post': 'Write about the benefits of remote work for productivity and work-life balance.',
        'Ad Copy': 'Create a Facebook ad for a fitness app targeting busy professionals.',
        'Landing Page Headline': 'Craft compelling headlines for a SaaS product landing page.'
    }

    for content_type_example, description in examples.items():
        st.markdown(f"**{content_type_example}:** {description}")

st.info("💡 Tip: Be specific about your target audience and key benefits for better results!")
