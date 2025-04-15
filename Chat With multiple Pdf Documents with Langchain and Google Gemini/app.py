
# import streamlit as st
# import os
# from PyPDF2 import PdfReader
# from dotenv import load_dotenv
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import google.generativeai as genai
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from langchain.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# genai.configure(
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# # model = genai.GenerativeModel("gemini-2.0-flash")


# def get_pdf_text(pdf_docs) :
#     text = ""
#     for pdf in pdf_docs :       
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages :
#             text += page.extract_text()
#     return text

# def get_text_chunks(text) :
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
#     chunks = text_splitter.split_text(text)
#     return chunks

# def get_vector_store(text_chunks) :
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     vector_store = FAISS.from_texts(text_chunks, embeddings)
#     vector_store.save_local("faiss_index")
    
    
# def get_conversational_chain() :
#     prompt_template = """ 
#     Answer the question as detailed as possible from the provided context,make sure to provide all the details, If the answer is not found in Provided context, just say "answer is not available in the context", don't provide the wrong answer\n\n
#     Context:\n{context}?\n
#     Question: \n{question}\n
    
#     Answer:
#     """
    
#     model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    
#     prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
#     chain = load_qa_chain(model, chain_type='stuff', prompt=prompt)
    
#     return chain



# def user_input(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
#     # new_db = FAISS.load_local("faiss_index", embeddings)
#     new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

#     docs = new_db.similarity_search(user_question)
    
#     chain = get_conversational_chain()
    
#     response = chain(
#         {"input_documents": docs, "question": user_question}, 
#         return_only_outputs=True
#     )
    
#     print(response)
#     st.write("Reply:", response['output_text'])
    
# def main() :
#     st.set_page_config("Chat Multiple PDF")
#     st.header("Chat with Multiple PDF Documents using Gemini")
    
#     user_question = st.text_input("Ask a question about the PDF documents")
    
#     if user_question :
#         user_input(user_question)
    
#     with st.sidebar :
#         st.title("Menu")
#         pdf_docs = st.file_uploader("Upload PDF documents", type="pdf", accept_multiple_files=True)
#         if st.button("Submit and Process") :
#             with st.spinner("Processing...") :
#                 raw_text = get_pdf_text(pdf_docs)
#                 text_chunks = get_text_chunks(raw_text)
#                 get_vector_store(text_chunks)
#                 st.success("PDF documents processed successfully!")
                
#                 st.balloons()
#                 st.success("You can now ask questions about the PDF documents.")
#                 st.balloons()

# if __name__ == "__main__" :
#     main()
    
   
import streamlit as st
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    metadata = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        metadata.append(f"{pdf.name} - {len(pdf_reader.pages)} pages")
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text, metadata

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. If the answer is not found, say "answer is not available in the context".
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    return load_qa_chain(model, chain_type='stuff', prompt=prompt)

def user_input(user_question, chat_history):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    chat_history.append((user_question, response['output_text']))
    return chat_history

def main():
    st.set_page_config(page_title="Chat with Multiple PDFs", layout="wide")
    st.header("📄 Chat with Multiple PDFs using Gemini AI")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_question = st.text_input("Ask a question about the PDFs")
    
    if user_question:
        st.session_state.chat_history = user_input(user_question, st.session_state.chat_history)
    
    st.subheader("Chat History")
    for question, answer in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(f"**You:** {question}")
        with st.chat_message("assistant"):
            st.write(f"**Bot:** {answer}")
    
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()
    
    with st.sidebar:
        st.title("📂 Upload PDFs")
        pdf_docs = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        
        if st.button("Process PDFs"):
            with st.spinner("Processing..."):
                raw_text, metadata = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("✅ PDFs processed successfully!")
                st.write("### Processed Documents")
                for data in metadata:
                    st.write(f"📘 {data}")
                
                st.download_button("Download Extracted Text", raw_text, "extracted_text.txt")
                st.balloons()

if __name__ == "__main__":
    main()

