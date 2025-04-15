

# import streamlit as st
# import os
# from langchain_groq import ChatGroq
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain.chains import create_retrieval_chain

# from dotenv import load_dotenv
# load_dotenv()

# groq_api_key = os.getenv('GROQ_API_KEY')
# os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")


# st.title("Gemma Model Document Q&A")

# llm = ChatGroq(api_key=groq_api_key, model_name='Gemma-7b-it')

# prompt = ChatPromptTemplate.from_template(
#     """
#     Answer the question based on the context only.
#     Please provide the most accurate response based on the question
#     <context>
#     {context}
#     <context>
#     Question:{input}
    
#     """
# )

# def vector_embedding() :
#     if 'vector' not in st.session_state :
#         st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         st.session_state.loader = PyPDFDirectoryLoader('./us_census')
#         st.session_state.docs = st.session_state.loader.load()
#         st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
#         st.session_state.vectors= FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# prompt1 = st.text_input("Enter your question from the documents?")

# if st.button("Creating Vector Store") :
#     vector_embedding()
#     st.success("Vector Store Created Successfully")

# import time


# if prompt1 :
#     document_chain = create_stuff_documents_chain(llm, prompt)
#     retriever = st.session_state.vector.as_retriever()
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
#     start = time.process_time()
#     response =retrieval_chain.invoke({'input' : prompt1})
#     st.write(response['answer'])
    
#     with st.expander('Document Similarity Search') :
#         for i, doc in enumerate(response['context']) :
#             st.write(doc.page_content)
#             st.write("--------------------------------")


import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain

from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

st.title("Gemma Model Document Q&A")

llm = ChatGroq(api_key=groq_api_key, model_name='gemma2-9b-it')

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on the context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Question:{input}
    """
)

uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

def vector_embedding():
    if 'vector' not in st.session_state and uploaded_files:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        docs = []
        for uploaded_file in uploaded_files:
            with open(f"./temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.read())

            loader = PyPDFLoader(f"./temp_{uploaded_file.name}")
            docs.extend(loader.load())

        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(docs)
        st.session_state.vector = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

if st.button("Create Vector Store"):
    vector_embedding()
    st.success("Vector Store Created Successfully")

prompt1 = st.text_input("Enter your question from the documents:")

if prompt1 and "vector" in st.session_state:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    response = retrieval_chain.invoke({'input': prompt1})
    st.write(response['answer'])
    
    with st.expander('Document Similarity Search'):
        for doc in response['context']:
            st.write(doc.page_content)
            st.write("--------------------------------")


