# import os
# import streamlit as st
# import google.generativeai as genai
# import requests
# import json
# from dotenv import load_dotenv
# from newspaper import Article

# # Load API Key
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Google Gemini Model
# model = genai.GenerativeModel("gemini-2.0-flash")

# def analyze_news(article_text):
#     """Analyzes news credibility using AI"""
#     prompt = f"""
#     You are an expert in detecting fake news. Analyze the given article and classify it as:
#     - **Real**
#     - **Fake**
#     - **Biased** (Left or Right)

#     Provide the response in JSON format:
#     {{
#         "classification": "",
#         "confidence": "",
#         "reasoning": ""
#     }}

#     Article:
#     {article_text}
#     """
#     response = model.generate_content(prompt)
#     return response.text  # JSON Response

# def extract_text_from_url(news_url):
#     """Extracts text from a news article URL"""
#     article = Article(news_url)
#     article.download()
#     article.parse()
#     return article.text

# # Streamlit UI
# st.set_page_config(page_title="📰 Fake News Detector", layout="wide")
# st.header("📰 AI-Powered Fake News Detector")

# news_url = st.text_input("Enter News Article URL:")

# if st.button("Analyze News"):
#     if news_url:
#         try:
#             article_text = extract_text_from_url(news_url)
#             analysis = analyze_news(article_text)
            
#             # Parse JSON Response
#             response_dict = json.loads(analysis)
            
#             st.subheader("🔍 AI Analysis:")
#             st.json(response_dict)

#             # Classification
#             classification = response_dict["classification"]
#             st.success(f"📢 **News is classified as: {classification}**")

#             # Reasoning
#             st.write("📝 **Reasoning:**")
#             st.write(response_dict["reasoning"])

#         except Exception as e:
#             st.error(f"Error processing the news: {str(e)}")
#     else:
#         st.warning("Please enter a valid news article URL!")
# import os
# import streamlit as st
# import google.generativeai as genai
# import json
# from dotenv import load_dotenv
# from newspaper import Article

# # Load API Key
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Google Gemini Model
# model = genai.GenerativeModel("gemini-2.0-flash")

# def analyze_news(article_text):
#     """Analyzes news credibility using AI"""
#     prompt = f"""
#     You are an expert in detecting fake news. Analyze the given article and classify it as:
#     - **Real**
#     - **Fake**
#     - **Biased** (Left or Right)

#     Provide the response in JSON format:
#     {{
#         "classification": "",
#         "confidence": "",
#         "reasoning": ""
#     }}

#     Article:
#     {article_text}
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         raw_response = response.text

#         # Debugging: Print raw response
#         print("Raw API Response:", raw_response)

#         # Ensure response is valid JSON
#         return json.loads(raw_response) if raw_response else None
#     except Exception as e:
#         print(f"AI Model Error: {str(e)}")
#         return None

# def extract_text_from_url(news_url):
#     """Extracts text from a news article URL"""
#     try:
#         article = Article(news_url)
#         article.download()
#         article.parse()

#         if not article.text:
#             print("⚠️ No text extracted from the article.")
#             return None
        
#         return article.text
#     except Exception as e:
#         print(f"URL Extraction Error: {str(e)}")
#         return None

# # Streamlit UI
# st.set_page_config(page_title="📰 Fake News Detector", layout="wide")
# st.header("📰 AI-Powered Fake News Detector")

# news_url = st.text_input("Enter News Article URL:")

# if st.button("Analyze News"):
#     if news_url:
#         article_text = extract_text_from_url(news_url)

#         if not article_text:
#             st.error("⚠️ Unable to extract text from the article. Try another URL.")
#         else:
#             response_dict = analyze_news(article_text)

#             if response_dict:
#                 st.subheader("🔍 AI Analysis:")
#                 st.json(response_dict)

#                 # Classification
#                 classification = response_dict.get("classification", "Unknown")
#                 st.success(f"📢 **News is classified as: {classification}**")

#                 # Reasoning
#                 st.write("📝 **Reasoning:**")
#                 st.write(response_dict.get("reasoning", "No reasoning provided."))
#             else:
#                 st.error("⚠️ AI model failed to analyze the news. Try again later.")
#     else:
#         st.warning("⚠️ Please enter a valid news article URL!")

# import os
# import streamlit as st
# import google.generativeai as genai
# import json
# from dotenv import load_dotenv
# from newspaper import Article

# # Load API Key
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Google Gemini Model
# model = genai.GenerativeModel("gemini-2.0-flash")

# def analyze_news(article_text):
#     """Analyzes news credibility using AI"""
#     prompt = f"""
#     You are an expert in detecting fake news. Analyze the given article and classify it as:
#     - **Real**
#     - **Fake**
#     - **Biased** (Left or Right)

#     Provide the response in **valid JSON format** with no extra text:
#     {{
#         "classification": "",
#         "confidence": "",
#         "reasoning": ""
#     }}

#     Article:
#     {article_text}
#     """

#     try:
#         response = model.generate_content(prompt)
#         raw_response = response.text.strip()

#         # Debug: Print raw response
#         print("🔍 Raw API Response:", raw_response)

#         # Ensure response is clean JSON
#         if raw_response.startswith("```json"):
#             raw_response = raw_response.replace("```json", "").replace("```", "").strip()

#         return json.loads(raw_response) if raw_response else None
#     except json.JSONDecodeError:
#         print("❌ JSON Parsing Error. Response was not valid JSON.")
#         return None
#     except Exception as e:
#         print(f"⚠️ AI Model Error: {str(e)}")
#         return None

# def extract_text_from_url(news_url):
#     """Extracts text from a news article URL"""
#     try:
#         article = Article(news_url)
#         article.download()
#         article.parse()

#         if not article.text:
#             print("⚠️ No text extracted from the article.")
#             return None
        
#         return article.text
#     except Exception as e:
#         print(f"URL Extraction Error: {str(e)}")
#         return None

# # Streamlit UI
# st.set_page_config(page_title="📰 Fake News Detector", layout="wide")
# st.header("📰 AI-Powered Fake News Detector")

# news_url = st.text_input("Enter News Article URL:")

# if st.button("Analyze News"):
#     if news_url:
#         article_text = extract_text_from_url(news_url)

#         if not article_text:
#             st.error("⚠️ Unable to extract text from the article. Try another URL.")
#         else:
#             response_dict = analyze_news(article_text)

#             if response_dict:
#                 st.subheader("🔍 AI Analysis:")
#                 st.json(response_dict)

#                 # Classification
#                 classification = response_dict.get("classification", "Unknown")
#                 st.success(f"📢 **News is classified as: {classification}**")

#                 # Reasoning
#                 st.write("📝 **Reasoning:**")
#                 st.write(response_dict.get("reasoning", "No reasoning provided."))
#             else:
#                 st.error("⚠️ AI model failed to analyze the news. Try again later.")
#     else:
#         st.warning("⚠️ Please enter a valid news article URL!")

import os
import streamlit as st
import google.generativeai as genai
import json
from dotenv import load_dotenv
from newspaper import Article

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Google Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_news(article_text):
    """Analyzes news credibility using AI"""
    prompt = f"""
    You are an expert in detecting fake news. Analyze the given article and classify it as:
    - **Real** (if it's factual & verifiable)
    - **Fake** (if it contains false/misleading claims)
    - **Biased** (if it leans towards a particular viewpoint)

    🔴 **Important:** If the article contains fake claims, the classification **must be "Fake"**.

    Provide the response in **valid JSON format** with no extra text:
    {{
        "classification": "",
        "confidence": "",
        "reasoning": ""
    }}

    Article:
    {article_text}
    """

    try:
        response = model.generate_content(prompt)
        raw_response = response.text.strip()

        # Debugging: Print raw response
        print("🔍 Raw API Response:", raw_response)

        # Ensure response is clean JSON
        if raw_response.startswith("```json"):
            raw_response = raw_response.replace("```json", "").replace("```", "").strip()

        response_dict = json.loads(raw_response) if raw_response else None

        # 🛠️ **Force correct classification based on reasoning**
        if response_dict:
            reasoning_text = response_dict.get("reasoning", "").lower()

            if "false" in reasoning_text or "misinformation" in reasoning_text or "not true" in reasoning_text:
                response_dict["classification"] = "Fake"

        return response_dict
    except json.JSONDecodeError:
        print("❌ JSON Parsing Error. Response was not valid JSON.")
        return None
    except Exception as e:
        print(f"⚠️ AI Model Error: {str(e)}")
        return None

def extract_text_from_url(news_url):
    """Extracts text from a news article URL"""
    try:
        article = Article(news_url)
        article.download()
        article.parse()

        if not article.text:
            print("⚠️ No text extracted from the article.")
            return None
        
        return article.text
    except Exception as e:
        print(f"URL Extraction Error: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(page_title="📰 Fake News Detector", layout="wide")
st.header("📰 AI-Powered Fake News Detector")

news_url = st.text_input("Enter News Article URL:")

if st.button("Analyze News"):
    if news_url:
        article_text = extract_text_from_url(news_url)

        if not article_text:
            st.error("⚠️ Unable to extract text from the article. Try another URL.")
        else:
            response_dict = analyze_news(article_text)

            if response_dict:
                st.subheader("🔍 AI Analysis:")
                st.json(response_dict)

                # Classification (Final check)
                classification = response_dict.get("classification", "Unknown")
                st.success(f"📢 **News is classified as: {classification}**")

                # Reasoning
                st.write("📝 **Reasoning:**")
                st.write(response_dict.get("reasoning", "No reasoning provided."))
            else:
                st.error("⚠️ AI model failed to analyze the news. Try again later.")
    else:
        st.warning("⚠️ Please enter a valid news article URL!")
        
# import os
# import streamlit as st
# import google.generativeai as genai
# import json
# import requests
# from dotenv import load_dotenv
# from newspaper import Article
# from gtts import gTTS
# from io import BytesIO
# import base64
# import pdfkit

# # Load API Key
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Google Gemini Model
# model = genai.GenerativeModel("gemini-2.0-pro")

# FACT_CHECK_API = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
# FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")

# def analyze_news(article_text):
#     """Analyzes news credibility using AI"""
#     prompt = f"""
#     You are an expert in detecting fake news. Analyze the given article and classify it as:
#     - **Real** (if it's factual & verifiable)
#     - **Fake** (if it contains false/misleading claims)
#     - **Biased** (if it leans towards a particular viewpoint)

#     Also provide a **Sentiment Analysis** (Positive, Negative, Neutral).
    
#     Provide a structured JSON response:
#     {{
#         "classification": "",
#         "confidence": "",
#         "sentiment": "",
#         "reasoning": ""
#     }}

#     Article:
#     {article_text}
#     """

#     try:
#         response = model.generate_content(prompt)
#         raw_response = response.text.strip()

#         # Ensure JSON format
#         if raw_response.startswith("```json"):
#             raw_response = raw_response.replace("```json", "").replace("```", "").strip()

#         response_dict = json.loads(raw_response) if raw_response else None

#         # Auto-fix incorrect classifications
#         if response_dict:
#             reasoning_text = response_dict.get("reasoning", "").lower()
#             if "false" in reasoning_text or "misinformation" in reasoning_text:
#                 response_dict["classification"] = "Fake"

#         return response_dict
#     except json.JSONDecodeError:
#         return None
#     except Exception as e:
#         return None

# def extract_text_from_url(news_url):
#     """Extracts text from a news article URL"""
#     try:
#         article = Article(news_url)
#         article.download()
#         article.parse()
#         return article.text if article.text else None
#     except:
#         return None

# def verify_news_source(news_url):
#     """Checks if the news source is reliable"""
#     trusted_domains = ["bbc.com", "cnn.com", "reuters.com", "theguardian.com", "nytimes.com"]
#     domain = news_url.split("/")[2]
#     return "Trusted Source ✅" if any(t in domain for t in trusted_domains) else "Unverified Source ⚠️"

# def fact_check_with_api(query):
#     """Cross-checks news claims with fact-check databases"""
#     try:
#         response = requests.get(FACT_CHECK_API, params={"query": query, "key": FACT_CHECK_API_KEY})
#         data = response.json()
#         if "claims" in data:
#             return data["claims"][0]["text"]
#         return "No fact-check data found."
#     except:
#         return "Fact-checking unavailable."

# def generate_audio_response(text):
#     """Converts AI analysis to speech"""
#     tts = gTTS(text, lang="en")
#     audio_bytes = BytesIO()
#     tts.save(audio_bytes, format="mp3")
#     audio_bytes.seek(0)
#     return base64.b64encode(audio_bytes.read()).decode()

# def generate_pdf_report(news_url, response_dict):
#     """Generates a PDF report of the AI analysis"""
#     html_content = f"""
#     <h1>Fake News Analysis Report</h1>
#     <p><strong>News URL:</strong> {news_url}</p>
#     <p><strong>Classification:</strong> {response_dict["classification"]}</p>
#     <p><strong>Confidence:</strong> {response_dict["confidence"]}</p>
#     <p><strong>Sentiment:</strong> {response_dict["sentiment"]}</p>
#     <p><strong>Reasoning:</strong> {response_dict["reasoning"]}</p>
#     """
#     pdfkit.from_string(html_content, "fake_news_report.pdf")

# # Streamlit UI
# st.set_page_config(page_title="📰 AI Fake News Detector", layout="wide")
# st.header("📰 AI-Powered Fake News Detector")

# option = st.radio("Choose Input Type:", ["Enter News URL", "Paste News Text"])

# if option == "Enter News URL":
#     news_url = st.text_input("Enter News Article URL:")
#     if st.button("Analyze News"):
#         article_text = extract_text_from_url(news_url)
#         if article_text:
#             response_dict = analyze_news(article_text)
#             if response_dict:
#                 st.subheader("🔍 AI Analysis:")
#                 st.json(response_dict)
#                 st.success(f"📢 **News is classified as: {response_dict['classification']}**")
#                 st.write(f"📝 **Sentiment:** {response_dict['sentiment']}")
#                 st.write(f"📝 **Reasoning:** {response_dict['reasoning']}")
                
#                 # Source Verification
#                 st.write(f"🔍 **News Source Check:** {verify_news_source(news_url)}")

#                 # Fact-Check API
#                 fact_check_result = fact_check_with_api(article_text[:100])
#                 st.write(f"📜 **Fact-Check Result:** {fact_check_result}")

#                 # Generate Audio Analysis
#                 audio_data = generate_audio_response(response_dict['reasoning'])
#                 st.audio(BytesIO(base64.b64decode(audio_data)), format="audio/mp3")

#                 # Generate PDF Report
#                 generate_pdf_report(news_url, response_dict)
#                 with open("fake_news_report.pdf", "rb") as pdf_file:
#                     st.download_button("Download PDF Report", pdf_file, "fake_news_report.pdf", "application/pdf")
# else:
#     news_text = st.text_area("Paste the News Text Here:")
#     if st.button("Analyze Text"):
#         if news_text:
#             response_dict = analyze_news(news_text)
#             if response_dict:
#                 st.subheader("🔍 AI Analysis:")
#                 st.json(response_dict)
#                 st.success(f"📢 **News is classified as: {response_dict['classification']}**")
#                 st.write(f"📝 **Sentiment:** {response_dict['sentiment']}")
#                 st.write(f"📝 **Reasoning:** {response_dict['reasoning']}")

#                 # Fact-Check API
#                 fact_check_result = fact_check_with_api(news_text[:100])
#                 st.write(f"📜 **Fact-Check Result:** {fact_check_result}")

#                 # Generate Audio Analysis
#                 audio_data = generate_audio_response(response_dict['reasoning'])
#                 st.audio(BytesIO(base64.b64decode(audio_data)), format="audio/mp3")

