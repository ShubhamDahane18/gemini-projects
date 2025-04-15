


# import streamlit as st
# import os
# from dotenv import load_dotenv
# load_dotenv()
# import sqlite3
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# def get_gemini_response(question, prompt) :
#     model = genai.GenerativeModel('gemini-2.0-flash')
#     response = model.generate_content([prompt[0], question])
#     return response.text

# def read_sql_query(sql, db) :
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     conn.commit()
#     conn.close()
    
#     for row in rows :
#         print(row)
#     return rows

# prompt=[
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
#     SECTION and MARKS \n\nFor example,\nExample 1 - How many entries of records are present?, 
#     the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
#     \nExample 2 - Tell me all the students studying in Data Science class?, 
#     the SQL command will be something like this SELECT * FROM STUDENT 
#     where CLASS="Data Science"; 
#     also the sql code should not have ``` in beginning or end and sql word in output

#     """
# ]

# st.set_page_config(page_title="I can Retrieve Information from SQL Database", page_icon=":guardsman:", layout="wide")
# st.header("Gemini APp to Retrieve Information from SQL Database")

# questions = st.text_input("Input :" ,key='input')

# submit = st.button("Ask Question")

# if submit :
#     response = get_gemini_response(questions, prompt)
#     print(response)
#     data = read_sql_query(response, "student.db")
#     st.subheader("The response is :")
#     for row in data :
#         print(row)
#         st.header(row)


import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import speech_recognition as sr
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to process AI-generated SQL
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to execute SQL query
def read_sql_query(sql, db="student.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    conn.commit()
    conn.close()
    
    df = pd.DataFrame(rows, columns=col_names)
    return df

# def read_sql_query(sql, db='student.db'):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    print(f"Executing SQL: {sql}")  # Debugging line
    
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"SQL Error: {e}")
        return [("Error:", str(e))]  # Return error message in UI
    
    conn.commit()
    conn.close()
    return rows


# Prompt for AI
prompt = [
    """
    You are an expert in converting English questions to SQL queries for an SQLite database.
    The database name is `STUDENT`, with columns: `NAME`, `CLASS`, `SECTION`, `MARKS`.

    Rules:
    1. Only use valid SQLite syntax.
    2. Do not generate `SHOW` statements.
    3. For listing all table names, use: `SELECT name FROM sqlite_master WHERE type='table';`
    4. Do not include `sql` or triple backticks (` ``` `) in the response.

    Examples:
    - "How many students are in Data Science?" → `SELECT COUNT(*) FROM STUDENT WHERE CLASS='Data Science';`
    - "List all students with marks > 80" → `SELECT * FROM STUDENT WHERE MARKS > 80;`
    """
]


# Streamlit UI
st.set_page_config(page_title="AI SQL Query App", page_icon="🤖", layout="wide")

st.title("🔍 AI-Powered SQL Querying System")

# Sidebar Navigation
option = st.sidebar.radio("Choose an option:", ["Ask AI", "Query Builder", "History", "Settings"])

if option == "Ask AI":
    st.subheader("🤖 Ask a Question")
    question = st.text_input("Enter your query:", key='input')
    
    # Voice Input
    if st.button("🎙️ Speak"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)
            try:
                question = recognizer.recognize_google(audio)
                st.text(f"Recognized: {question}")
            except sr.UnknownValueError:
                st.write("Sorry, could not understand.")
    
    if st.button("🔍 Generate Query"):
        sql_query = get_gemini_response(question, prompt)
        st.code(sql_query, language="sql")
        
        df = read_sql_query(sql_query)
        if not df.empty:
            st.dataframe(df)
            st.subheader("📊 Data Visualization")
            if "MARKS" in df.columns:
                fig = px.bar(df, x="NAME", y="MARKS", title="Student Marks")
                st.plotly_chart(fig)
        else:
            st.warning("No data found!")

elif option == "Query Builder":
    st.subheader("🛠️ Build a Custom Query")
    name = st.text_input("Filter by Name:")
    class_filter = st.text_input("Filter by Class:")
    min_marks = st.number_input("Minimum Marks:", min_value=0, max_value=100, value=0)
    
    query = "SELECT * FROM STUDENT WHERE 1=1"
    if name:
        query += f" AND NAME='{name}'"
    if class_filter:
        query += f" AND CLASS='{class_filter}'"
    query += f" AND MARKS >= {min_marks}"
    
    if st.button("Run Query"):
        df = read_sql_query(query)
        st.dataframe(df)

elif option == "History":
    st.subheader("📜 Query History")
    history_file = "query_history.txt"
    
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = f.readlines()
            for line in history:
                st.write(line.strip())
    else:
        st.info("No history found.")

elif option == "Settings":
    st.subheader("⚙️ Settings")
    st.write("🔐 Authentication (Future Feature)")
    st.write("📩 Export Data (Coming Soon!)")
