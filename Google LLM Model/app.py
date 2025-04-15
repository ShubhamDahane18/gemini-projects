# from dotenv import load_dotenv
# load_dotenv()


# import streamlit as st
# import os

# import google.generativeai as genai

# # Load your API key from environment variable
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model = genai.GenerativeModel("gemini-pro")
# def get_gemini_response(question) :
#     response = model.generate_content(question)
#     return response.text

# st.set_page_config(page_title="Q&A Demo")

# st.header("Gemini LLM Application")

# input = st.text_input("Input:", key="input")
# submit = st.button("Ask the question")

# if submit :
#     response = get_gemini_response(input)
#     st.subheader("The Response is ")
#     st.write(response)


from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os

import google.generativeai as genai

# Load your API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model_name = "gemini-pro"
model_name = "gemini-2.0-flash"

try:
    model = genai.GenerativeModel(model_name)
    def get_gemini_response(question):
        response = model.generate_content(question)
        return response.text
except Exception as e:
    st.error(f"Error initializing the model: {e}")
    st.stop()

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is ")
    st.write(response)