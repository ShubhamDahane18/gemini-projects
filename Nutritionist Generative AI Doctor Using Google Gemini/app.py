
# import streamlit as st
# import os
# from dotenv import load_dotenv
# load_dotenv()
# from PIL import Image

# import google.generativeai as genai



# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# def get_gemini_response(input_prompt, image) :
#     model = genai.GenerativeModel('gemini-2.0-flash')
#     response = model.generate_content([input_prompt, image[0]])
#     return response.text

# def input_image_setup(uploaded_file) :
#     if uploaded_file is not None :
#         bytes_data = uploaded_file.getvalue()
#         image_parts = [
#             {
#                 'mime_type': uploaded_file.type,
#                 'data': bytes_data
#             }
#         ]
        
#         return image_parts
#     else :
#         raise FileNotFoundError('No file uploaded')
    
# st.set_page_config(page_title='Gemini Health App')
# st.title('Gemini Health App')
# uploaded_file = st.file_uploader('Upload an image...', type=['jpg', 'png', 'jpeg' ])
# image = ""
# if uploaded_file is not None :
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Uploaded Image', use_column_width=True)

# submit = st.button("Tell me about the total calories")

# input_prompt="""
# You are an expert in nutritionist where you need to see the food items from the image
#                and calculate the total calories, also provide the details of every food items with calories intake
#                is below format

#                1. Item 1 - no of calories
#                2. Item 2 - no of calories
#                ----
#                ----


# """

# if submit :
#     image_data = input_image_setup(uploaded_file)
#     response = get_gemini_response(input_prompt, image_data)
#     st.header('The response is')
#     st.write(response)

import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Load environment variables
load_dotenv()

# Configure Google Gemini AI API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to get Gemini response
def get_gemini_response(input_prompt, image, model_name='gemini-2.0-flash'):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to setup image for input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                'mime_type': uploaded_file.type,
                'data': bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')

# Function to parse response into a DataFrame
def parse_food_items(response_text):
    lines = response_text.strip().split('\n')
    items = []
    calories = []
    
    for line in lines:
        if not line.strip():
            continue
        if line[0].isdigit() and ' - ' in line:
            parts = line.split(' - ')
            if len(parts) >= 2:
                item_part = parts[0]
                # Remove numbering from item name
                if '.' in item_part:
                    item_name = item_part.split('.', 1)[1].strip()
                else:
                    item_name = item_part.strip()
                
                # Extract calorie count
                calorie_part = parts[1].strip()
                try:
                    if 'calories' in calorie_part.lower():
                        calorie_str = calorie_part.lower().split('calories')[0].strip()
                    else:
                        calorie_str = calorie_part
                    # Remove non-numeric characters except for decimal points
                    calorie_str = ''.join(c for c in calorie_str if c.isdigit() or c == '.')
                    calories_value = float(calorie_str)
                    items.append(item_name)
                    calories.append(calories_value)
                except ValueError:
                    pass  # Skip lines with unparseable calorie values
    
    return pd.DataFrame({'Food Item': items, 'Calories': calories})

# Function to create visualization
def create_visualization(df):
    plt.figure(figsize=(10, 6))
    chart = sns.barplot(x='Calories', y='Food Item', data=df)
    plt.title('Calorie Content by Food Item')
    plt.xlabel('Calories')
    plt.ylabel('Food Item')
    plt.tight_layout()
    
    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

# Function to get download link for data
def get_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Function to create a nutritional advice based on the food items
def get_nutritional_advice(df):
    total_calories = df['Calories'].sum()
    
    advice = f"""
    ## Nutritional Summary
    
    Total Calories: **{total_calories:.1f} kcal**
    
    ### Meal Analysis:
    """
    
    if total_calories < 300:
        advice += "\n- This appears to be a light snack or small meal."
    elif total_calories < 600:
        advice += "\n- This appears to be a moderate-sized meal."
    else:
        advice += "\n- This appears to be a larger meal with significant caloric content."
    
    if len(df) >= 3:
        highest_calorie_item = df.loc[df['Calories'].idxmax()]['Food Item']
        advice += f"\n- **{highest_calorie_item}** contributes the most calories to this meal."
    
    advice += """
    
    ### General Tips:
    - An average adult needs approximately 2000-2500 calories per day
    - Balance your meals with proteins, carbohydrates, and healthy fats
    - Include fruits and vegetables for essential vitamins and minerals
    """
    
    return advice

# Streamlit app setup
st.set_page_config(page_title='Gemini Health App', layout='wide')

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E7D32;
        margin-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F0F8F0;
        border-radius: 4px 4px 0px 0px;
        gap: 1;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🍽️ Gemini Nutrition Assistant</p>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["📷 Analyze Food", "📊 History", "ℹ️ About"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<p class="sub-header">Upload Food Image</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader('Choose an image of your meal...', type=['jpg', 'png', 'jpeg'])
        
        model_option = st.selectbox(
            'Select AI Model',
            ('gemini-2.0-flash', 'gemini-2.0-pro')
        )
        
        analysis_options = st.multiselect(
            'What would you like to analyze?',
            ['Calorie Count', 'Nutritional Breakdown', 'Health Recommendations'],
            default=['Calorie Count']
        )
        
        col_submit1, col_submit2 = st.columns([1, 1])
        with col_submit1:
            submit = st.button("Analyze Food", type="primary", use_container_width=True)
        with col_submit2:
            clear = st.button("Clear", type="secondary", use_container_width=True)
        
    with col2:
        image_placeholder = st.empty()
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_placeholder.image(image, caption='Uploaded Meal Image', use_column_width=True)
        else:
            image_placeholder.info("Please upload an image of your meal")
    
    # Create an input prompt based on selected options
    input_prompt = """
    You are an expert nutritionist. Analyze the food items in the image and provide the following information:
    """
    
    if 'Calorie Count' in analysis_options:
        input_prompt += """
        - Calculate the total calories and provide a detailed breakdown for each food item in this format:
          1. [Food Item Name] - [calories] calories
          2. [Food Item Name] - [calories] calories
          ...
        """
    
    if 'Nutritional Breakdown' in analysis_options:
        input_prompt += """
        - For each food item, estimate the macronutrient composition (protein, carbs, fat) in grams when possible.
        """
    
    if 'Health Recommendations' in analysis_options:
        input_prompt += """
        - Provide brief health insights about this meal:
          - Is it balanced?
          - What nutrients might be missing?
          - Any suggestions for improvement?
        """
    
    # Results section
    results_container = st.container()
    
    if submit and uploaded_file is not None:
        with st.spinner('Analyzing your meal...'):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data, model_option)
                
                with results_container:
                    st.markdown('<p class="sub-header">Analysis Results</p>', unsafe_allow_html=True)
                    
                    col_text, col_vis = st.columns([1, 1])
                    
                    with col_text:
                        st.markdown("### Detailed Analysis")
                        st.write(response)
                        
                        # Save response to session state for history
                        if 'history' not in st.session_state:
                            st.session_state.history = []
                        
                        # Save current analysis
                        current_analysis = {
                            'timestamp': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                            'image': uploaded_file,
                            'response': response
                        }
                        st.session_state.history.append(current_analysis)
                    
                    with col_vis:
                        try:
                            # Parse data and create visualization
                            df = parse_food_items(response)
                            
                            if not df.empty:
                                st.markdown("### Calorie Distribution")
                                viz_buffer = create_visualization(df)
                                st.image(viz_buffer, caption='Calorie Content by Food Item')
                                
                                st.markdown("### Data Table")
                                st.dataframe(df, use_container_width=True)
                                
                                total_calories = df['Calories'].sum()
                                st.info(f"Total Calories: **{total_calories:.1f}** kcal")
                                
                                st.markdown(get_download_link(df, 'food_calories.csv', 'Download data as CSV'), unsafe_allow_html=True)
                                
                                st.markdown(get_nutritional_advice(df))
                            else:
                                st.warning("Could not parse the response into a structured format. Please see the text analysis.")
                        except Exception as e:
                            st.error(f"Error creating visualization: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    if clear:
        image_placeholder.empty()
        results_container.empty()

with tab2:
    st.markdown('<p class="sub-header">Analysis History</p>', unsafe_allow_html=True)
    
    if 'history' in st.session_state and st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Analysis {i+1} - {entry['timestamp']}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    try:
                        image = Image.open(entry['image'])
                        st.image(image, caption='Meal Image', use_column_width=True)
                    except:
                        st.warning("Image no longer available")
                
                with col2:
                    st.markdown("### Results")
                    st.write(entry['response'])
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No analysis history available yet. Upload an image and analyze it to see history.")

with tab3:
    st.markdown('<p class="sub-header">About Gemini Nutrition Assistant</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### How to Use
    1. **Upload an image** of your meal using the file uploader in the "Analyze Food" tab
    2. **Select analysis options** that you're interested in
    3. **Click "Analyze Food"** to get detailed nutritional information
    4. **View your analysis history** in the "History" tab
    
    ### Features
    - **Calorie Counting**: Get detailed breakdown of calories in your meal
    - **Nutritional Analysis**: Understand the nutritional value of your food
    - **Health Recommendations**: Receive personalized suggestions
    - **Data Visualization**: See your meal's calorie distribution
    - **History Tracking**: Keep track of your previous meals and analyses
    
    ### About the Technology
    This app uses Google's Gemini AI to analyze food images and provide nutritional information. The AI can identify food items and estimate their caloric and nutritional content.
    
    ### Disclaimer
    While this app strives for accuracy, the calorie and nutritional estimates should be considered approximations. For precise nutritional guidance, please consult with a registered dietitian.
    """)