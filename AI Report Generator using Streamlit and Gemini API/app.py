import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
from io import StringIO

# Set up the page configuration
st.set_page_config(page_title="AI Report Generator", layout="wide")

# App title and description
st.title("AI Report Generator")
st.markdown("""
This app allows you to upload data (CSV or JSON) and ask questions about it in natural language.
The AI will analyze your data and provide insights based on your questions.
""")

# Function to initialize Gemini API
def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    # return genai.GenerativeModel('gemini-pro')
    return genai.GenerativeModel('gemini-2.0-flash')

# File uploader
st.subheader("1. Upload your data")
uploaded_file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

# API Key input
st.subheader("2. Enter your Gemini API Key")
gemini_api_key = st.text_input("Gemini API Key", type="password")
if gemini_api_key:
    st.success("API key received! You can now analyze your data.")

# Main app function
def analyze_data(data_df, question, model):
    try:
        # Convert DataFrame to a readable format for Gemini
        data_str = data_df.to_string()
        
        # Prepare prompt for Gemini
        prompt = f"""
        I have the following data:
        
        {data_str}
        
        Question: {question}
        
        Please analyze this data and provide insights in response to the question.
        Include relevant statistics, trends, or visualizations descriptions if appropriate.
        Format your response in markdown for better readability.
        """
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing data: {str(e)}"

# Data preview section
if uploaded_file is not None:
    try:
        # Read the file based on its type
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            # Try different JSON formats
            try:
                df = pd.read_json(uploaded_file)
            except:
                # If it's not directly convertible to DataFrame, load as JSON then convert
                content = uploaded_file.getvalue().decode('utf-8')
                json_data = json.loads(content)
                # Handle both list of objects and nested JSON
                if isinstance(json_data, list):
                    df = pd.json_normalize(json_data)
                else:
                    df = pd.json_normalize([json_data])[0]
        
        st.subheader("3. Data Preview")
        st.dataframe(df.head(10))
        
        # Ask questions about the data
        st.subheader("4. Ask questions about your data")
        question = st.text_area("Enter your question in natural language:", 
                               height=100,
                               placeholder="Examples:\n- What are the top 3 products sold?\n- Show me the trend in sales over time.\n- Which regions have the highest customer satisfaction?")
        
        analyze_button = st.button("Analyze Data")
        
        if analyze_button and question and gemini_api_key:
            with st.spinner("Analyzing your data..."):
                try:
                    # Initialize the Gemini model
                    model = initialize_gemini(gemini_api_key)
                    
                    # Analyze the data
                    analysis_result = analyze_data(df, question, model)
                    
                    # Display results
                    st.subheader("Analysis Results")
                    st.markdown(analysis_result)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        elif analyze_button and not gemini_api_key:
            st.warning("Please enter a valid Gemini API key.")
        elif analyze_button and not question:
            st.warning("Please enter a question about your data.")
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

# Instructions sidebar
with st.sidebar:
    st.header("How to use this app")
    st.markdown("""
    1. **Upload your data file** (CSV or JSON format)
    2. **Enter your Gemini API key**
       - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
    3. **Review your data** in the preview section
    4. **Ask questions** about your data in natural language
    5. **Click "Analyze Data"** to get AI-powered insights
    
    ### Example questions:
    - "What are the top 3 products sold in Q1?"
    - "Show me the sales trend over the past 12 months"
    - "Which customer segment has the highest lifetime value?"
    - "Identify unusual patterns in this transaction data"
    - "Summarize the key insights from this survey data"
    """)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app uses Google's Gemini AI to analyze your data and provide insights.
    Your data is processed securely and not stored on our servers.
    """)