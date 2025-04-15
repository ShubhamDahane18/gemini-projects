from fastapi import FastAPI
import arxiv
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Keys
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# 🔍 Fetch Research Papers from Arxiv
@app.get("/search_papers/")
async def search_papers(query: str):
    search = arxiv.Search(query=query, max_results=5, sort_by=arxiv.SortCriterion.Relevance)
    papers = [{"title": p.title, "summary": p.summary, "url": p.entry_id} for p in search.results()]
    return {"papers": papers}

# 📜 Generate Summary Using Google Gemini
@app.get("/summarize/")
async def summarize_text(text: str, language: str = "English"):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize this in {language}: {text}"
    response = model.generate_content(prompt)
    return {"summary": response.text}

# ❓ AI Research Q&A
@app.get("/ask/")
async def ask_ai(question: str, context: str):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Based on this research: {context}, answer this: {question}"
    response = model.generate_content(prompt)
    return {"answer": response.text}
