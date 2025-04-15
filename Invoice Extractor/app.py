# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# import os
# import google.generativeai as genai
# from PIL import Image

# genai.configure(
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# model = genai.GenerativeModel(
#     "gemini-2.0-flash"
# )

# def get_gemini_response(input, image, prompt) :
#     response = model.generate_content([input, image[0], prompt])
#     return response.text

# def input_image_details(uploaded_file) :
#     if uploaded_file is not None :
#         bytes_data = uploaded_file.getvalue()
        
#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else :
#         raise FileNotFoundError("No file uploaded")

# st.set_page_config(page_title="MultiLanguage Invoice Extractor")

# st.header("MultiLanguage Invoice Extractor")
# input = st.text_input("Input Prompt:", key='input')
# uploaded_file = st.file_uploader("Upload an image of the invoice...", type=['jpg', 'jpeg', 'png', 'webp'])
# image=""

# if uploaded_file is not None :
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)
    
# submit = st.button("Tell me about the invoice")

# input_prompt = """
# You are an expert in understanding invoices. We will upload image as invoice and you will answer any questions based on the uploaded invoice image.

# """

# if submit :
#     image_data = input_image_details(uploaded_file)
#     response = get_gemini_response(input, image_data, input_prompt)
#     st.subheader("The Response is:")
#     st.write(response)


# from dotenv import load_dotenv
# import streamlit as st
# import os
# import google.generativeai as genai
# from PIL import Image
# import json
# import pandas as pd

# # Load environment variables
# load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model = genai.GenerativeModel("gemini-2.0-flash")

# def get_gemini_response(input, image, prompt, language):
#     """Fetches response from the Gemini AI model."""
#     full_prompt = f"""
#     You are an expert in understanding invoices. 
#     The user wants the extracted details in {language}. 
#     Provide the details like Invoice Number, Date, Vendor, Total Amount, and Items in a structured manner.
#     """
#     response = model.generate_content([input, image[0], full_prompt])
#     return response.text

# def input_image_details(uploaded_file):
#     """Processes uploaded image for AI model."""
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# # Streamlit UI
# st.set_page_config(page_title="MultiLanguage Invoice Extractor")
# st.header("🧾 MultiLanguage Invoice Extractor")

# input_text = st.text_input("Enter Additional Instructions (Optional):", key='input')

# uploaded_file = st.file_uploader("Upload an invoice image...", type=['jpg', 'jpeg', 'png', 'webp'])

# language = st.selectbox("Select Output Language:", ["English", "Spanish", "French", "German", "Hindi", "Chinese"])

# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Invoice", use_column_width=True)

# submit = st.button("Extract Invoice Details")

# if submit:
#     try:
#         if uploaded_file is None:
#             st.error("Please upload an invoice image first.")
#         else:
#             image_data = input_image_details(uploaded_file)
#             response = get_gemini_response(input_text, image_data, input_text, language)
            
#             # Display response
#             st.subheader("📜 Extracted Invoice Details:")
#             st.write(response)

#             # Save as JSON and CSV
#             try:
#                 response_dict = json.loads(response)  # Convert to dictionary
#                 df = pd.DataFrame([response_dict])
                
#                 json_data = json.dumps(response_dict, indent=4)
#                 csv_data = df.to_csv(index=False)
                
#                 # Download buttons
#                 st.download_button("Download JSON", json_data, "invoice_data.json", "application/json")
#                 st.download_button("Download CSV", csv_data, "invoice_data.csv", "text/csv")
#             except json.JSONDecodeError:
#                 st.warning("Failed to parse structured invoice details. Showing raw output.")
#     except Exception as e:
#         st.error(f"Error: {str(e)}")


from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import json
import pandas as pd

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def get_gemini_response(input, image, language):
    """Fetches response from the Gemini AI model."""
    full_prompt = f"""
    You are an expert in understanding invoices. 
    The user wants the extracted details in {language}. 
    Provide the details in structured JSON format with the following fields:
    {{
        "invoice_number": "",
        "date": "",
        "vendor": "",
        "total_amount": "",
        "items": [
            {{"name": "", "quantity": "", "price": ""}}
        ]
    }}
    """
    response = model.generate_content([input, image[0], full_prompt])
    return response.text

def input_image_details(uploaded_file):
    """Processes uploaded image for AI model."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("🧾 MultiLanguage Invoice Extractor")

input_text = st.text_input("Enter Additional Instructions (Optional):", key='input')

uploaded_file = st.file_uploader("Upload an invoice image...", type=['jpg', 'jpeg', 'png', 'webp'])

language = st.selectbox("Select Output Language:", ["English", "Spanish", "French", "German", "Hindi", "Chinese"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # st.image(image, caption="Uploaded Invoice", use_column_width=True)
    st.image(image, caption="Uploaded Invoice", use_container_width=True)

submit = st.button("Extract Invoice Details")

if submit:
    try:
        if uploaded_file is None:
            st.error("Please upload an invoice image first.")
        else:
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_text, image_data, language)
            
            # Display response
            st.subheader("📜 Extracted Invoice Details:")
            
            try:
                response_dict = json.loads(response)  # Convert to dictionary
                st.json(response_dict)  # Display structured JSON output
                
                df = pd.DataFrame([response_dict])
                json_data = json.dumps(response_dict, indent=4)
                csv_data = df.to_csv(index=False)
                
                # Download buttons
                st.download_button("Download JSON", json_data, "invoice_data.json", "application/json")
                st.download_button("Download CSV", csv_data, "invoice_data.csv", "text/csv")
            except json.JSONDecodeError:
                st.warning("Failed to parse structured invoice details. Showing raw output.")
                st.write(response)
    except Exception as e:
        st.error(f"Error: {str(e)}")