import streamlit as st
import requests

st.title("📚 AI Research Assistant (No OpenAI)")

query = st.text_input("Enter your research topic")

if st.button("Search Papers"):
    with st.spinner("Fetching papers..."):
        res = requests.get(f"http://127.0.0.1:8000/search_papers/?query={query}").json()
        for paper in res["papers"]:
            st.subheader(paper["title"])
            st.write(paper["summary"])
            st.write(f"[Read More]({paper['url']})")

text_to_summarize = st.text_area("Paste research text to summarize")
language = st.selectbox("Select Language", ["English", "Hindi", "French", "German"])

if st.button("Summarize"):
    with st.spinner("Summarizing..."):
        summary_res = requests.get(f"http://127.0.0.1:8000/summarize/?text={text_to_summarize}&language={language}").json()
        st.write("**Summary:**")
        st.write(summary_res["summary"])

research_text = st.text_area("Paste research text for Q&A")
question = st.text_input("Ask AI a question about this research")

if st.button("Get Answer"):
    with st.spinner("Processing..."):
        answer_res = requests.get(f"http://127.0.0.1:8000/ask/?question={question}&context={research_text}").json()
        st.write("**AI Answer:**")
        st.write(answer_res["answer"])
