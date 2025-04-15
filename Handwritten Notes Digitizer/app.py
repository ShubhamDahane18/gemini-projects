# from dotenv import load_dotenv
# import streamlit as st
# import os
# import google.generativeai as genai
# from PIL import Image
# import json

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Gemini model
# model = genai.GenerativeModel("gemini-2.0-flash")

# def extract_text_from_image(image):
#     """Extracts handwritten text from an image using Gemini AI."""
#     prompt = "Extract the handwritten text from this image and return it as plain text."
#     response = model.generate_content([image[0], prompt])
#     return response.text.strip()

# def process_uploaded_image(uploaded_file):
#     """Convert uploaded file to bytes for Gemini API."""
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         return [{"mime_type": uploaded_file.type, "data": bytes_data}]
#     else:
#         return None

# # Streamlit UI
# st.set_page_config(page_title="📝 Handwritten Notes Digitizer")
# st.header("📜 Handwritten Notes Digitizer")

# uploaded_file = st.file_uploader("Upload Handwritten Notes (JPG, PNG, WEBP)", type=['jpg', 'jpeg', 'png', 'webp'])

# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Handwritten Note", use_column_width=True)

# submit = st.button("Extract Text")

# if submit:
#     if uploaded_file is None:
#         st.error("Please upload a handwritten note first.")
#     else:
#         image_data = process_uploaded_image(uploaded_file)
#         if image_data:
#             extracted_text = extract_text_from_image(image_data)
            
#             st.subheader("📄 Extracted Text:")
#             text_area = st.text_area("Edit Text (if needed)", extracted_text, height=200)
            
#             # Save options
#             json_data = json.dumps({"extracted_text": text_area}, indent=4)
#             st.download_button("Download as JSON", json_data, "handwritten_text.json", "application/json")
#             st.download_button("Download as TXT", text_area, "handwritten_text.txt", "text/plain")

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import json
import sqlite3
from gtts import gTTS

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

# Database setup
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT, summary TEXT, keywords TEXT)")
conn.commit()

def extract_text_from_image(image):
    """Extract handwritten text from an image using Gemini AI."""
    prompt = "Extract the handwritten text from this image and return it as plain text."
    response = model.generate_content([image[0], prompt])
    return response.text.strip()

def summarize_text(text):
    """Summarize extracted text using Gemini AI."""
    prompt = "Summarize the following text in bullet points:\n\n" + text
    response = model.generate_content([prompt])
    return response.text.strip()

def extract_keywords(text):
    """Extract key topics from the text."""
    prompt = "Extract the main topics or keywords from the following text:\n\n" + text
    response = model.generate_content([prompt])
    return response.text.strip()

def translate_text(text, target_language):
    """Translate text to the selected language."""
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    response = model.generate_content([prompt])
    return response.text.strip()

def process_uploaded_image(uploaded_file):
    """Convert uploaded file to bytes for Gemini API."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        return None

def save_to_database(text, summary, keywords):
    """Save extracted notes to SQLite database."""
    cursor.execute("INSERT INTO notes (text, summary, keywords) VALUES (?, ?, ?)", (text, summary, keywords))
    conn.commit()

# Streamlit UI
st.set_page_config(page_title="📜 Handwritten Notes Digitizer", layout="wide")
st.title("📝 AI-Powered Handwritten Notes Digitizer")

uploaded_file = st.file_uploader("Upload Handwritten Notes (JPG, PNG, WEBP)", type=['jpg', 'jpeg', 'png', 'webp'])

languages = ["English", "Spanish", "French", "Hindi", "Chinese"]
language = st.selectbox("🌍 Translate Extracted Text To:", languages)

submit = st.button("🚀 Extract & Process Notes")

if submit:
    if uploaded_file is None:
        st.error("Please upload a handwritten note first.")
    else:
        image_data = process_uploaded_image(uploaded_file)
        if image_data:
            extracted_text = extract_text_from_image(image_data)
            summary = summarize_text(extracted_text)
            keywords = extract_keywords(extracted_text)
            translated_text = translate_text(extracted_text, language)
            
            save_to_database(extracted_text, summary, keywords)

            st.subheader("📄 Extracted Text:")
            text_area = st.text_area("Edit Text (if needed)", extracted_text, height=200)

            st.subheader("🔎 AI Summary:")
            st.write(summary)

            st.subheader("🏷️ Key Topics / Keywords:")
            st.write(keywords)

            st.subheader("🌍 Translated Text:")
            st.write(translated_text)

            # Convert to Speech
            tts = gTTS(extracted_text)
            tts.save("notes_audio.mp3")
            st.audio("notes_audio.mp3", format="audio/mp3")

            # Download buttons
            json_data = json.dumps({"extracted_text": extracted_text, "summary": summary, "keywords": keywords}, indent=4)
            st.download_button("📥 Download as JSON", json_data, "handwritten_text.json", "application/json")
            st.download_button("📥 Download as TXT", extracted_text, "handwritten_text.txt", "text/plain")

# Search past notes
st.sidebar.header("📂 Search Saved Notes")
search_query = st.sidebar.text_input("🔍 Search by Keyword:")
if st.sidebar.button("Search"):
    cursor.execute("SELECT text, summary, keywords FROM notes WHERE keywords LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()
    if results:
        st.sidebar.subheader("📌 Search Results:")
        for i, (text, summary, keywords) in enumerate(results, 1):
            st.sidebar.write(f"**{i}. Extracted Text:** {text[:100]}...")
            st.sidebar.write(f"🔹 **Summary:** {summary}")
            st.sidebar.write(f"🏷 **Keywords:** {keywords}")
            st.sidebar.markdown("---")
    else:
        st.sidebar.warning("No matching notes found.")
