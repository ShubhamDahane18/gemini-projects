

# import streamlit as st
# import os
# from dotenv import load_dotenv
# load_dotenv()

# import google.generativeai as genai
# import PyPDF2 as pdf



# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# def get_gemini_response(input) :
#     model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
#     response = model.generate_content(input)
#     return response.text 

# def input_pdf_text(uploaded_file) :
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page in range(len(reader.pages)) :
#         page = reader.pages[page]
#         text += str(page.extract_text())
#     return text


# #Prompt Template

# input_prompt="""
# Hey Act Like a skilled or very experience ATS(Application Tracking System)
# with a deep understanding of tech field,software engineering,data science ,data analyst
# and big data engineer. Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide 
# best assistance for improving thr resumes. Assign the percentage Matching based 
# on Jd and
# the missing keywords with high accuracy
# resume:{text}
# description:{jd}

# I want the response in one single string having the structure
# {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# """

# st.title("Smart ATS")
# st.text("Improve Your Resume ATS")

# jd = st.text_area('Paste Job Description')
# uploaded_file = st.file_uploader('Upload Your Resume', type='pdf', help='Upload your resume in PDF format')

# submit = st.button('Submit')

# if submit :
#     if uploaded_file is not None :
#         text = input_pdf_text(uploaded_file)
#         response = get_gemini_response(input_prompt)
#         st.subheader(response)
        
        
import streamlit as st
import os
import json
import tempfile
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2 as pdf
import docx
import pandas as pd
from io import StringIO

# Load environment variables
load_dotenv()

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set page configuration
st.set_page_config(
    page_title="ResumeMatch ATS System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_gemini_response(resume_text, job_description):
    """
    Get analysis from Gemini model comparing resume to job description.
    
    Args:
        resume_text (str): Text extracted from resume
        job_description (str): Job description text
    
    Returns:
        str: JSON string containing analysis
    """
    model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    
    prompt = f"""
    You are an advanced ATS (Applicant Tracking System) analyzer. I want you to analyze how well the provided resume matches the job description.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Perform a comprehensive analysis and provide the following:
    1. An overall percentage match score between the resume and job description
    2. Identify the key skills/requirements from the job description
    3. List which of these key skills/requirements are found in the resume
    4. List which key skills/requirements are missing in the resume
    5. Provide specific recommendations for improving the resume for this job
    6. Highlight the strengths of the resume for this position
    
    Format your response as a structured JSON object with the following keys:
    - "match_percentage": (number between 0-100)
    - "key_requirements": (array of strings)
    - "matching_skills": (array of strings)
    - "missing_skills": (array of strings)
    - "improvement_recommendations": (array of strings)
    - "resume_strengths": (array of strings)
    - "detailed_analysis": (string with overall analysis)
    
    ONLY respond with the JSON object and nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file"""
    with open(file_path, 'rb') as file:
        reader = pdf.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file"""
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_file(uploaded_file):
    """Extract text from various file formats"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name
    
    # Extract text based on file type
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension in ['docx', 'doc']:
        text = extract_text_from_docx(file_path)
    elif file_extension in ['txt', 'text']:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        os.unlink(file_path)
        return "Unsupported file format"
    
    # Delete the temporary file
    os.unlink(file_path)
    return text

def display_analysis(analysis_json):
    """Display the analysis in a structured format"""
    try:
        # Parse the JSON response
        analysis = json.loads(analysis_json)
        
        # Create two columns for the output
        col1, col2 = st.columns(2)
        
        # Column 1: Match percentage and skills analysis
        with col1:
            # Display match percentage with a progress bar
            st.subheader("ATS Match Score")
            match_percentage = analysis["match_percentage"]
            st.progress(match_percentage / 100)
            
            # Color code based on match percentage
            if match_percentage >= 80:
                st.markdown(f"<h1 style='text-align: center; color: green;'>{match_percentage}%</h1>", unsafe_allow_html=True)
            elif match_percentage >= 60:
                st.markdown(f"<h1 style='text-align: center; color: orange;'>{match_percentage}%</h1>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h1 style='text-align: center; color: red;'>{match_percentage}%</h1>", unsafe_allow_html=True)
            
            # Skills Analysis
            st.subheader("Skills Analysis")
            
            # Create a dataframe for skills comparison
            skills_data = {
                "Requirement": analysis["key_requirements"],
                "Status": ["✅ Found" if req in analysis["matching_skills"] else "❌ Missing" for req in analysis["key_requirements"]]
            }
            skills_df = pd.DataFrame(skills_data)
            st.dataframe(skills_df, use_container_width=True)
            
            # Display pie chart for skills match
            matching_count = len(analysis["matching_skills"])
            missing_count = len(analysis["missing_skills"])
            
            st.subheader("Skills Match Overview")
            data = pd.DataFrame({
                'Category': ['Matching Skills', 'Missing Skills'],
                'Count': [matching_count, missing_count]
            })
            st.bar_chart(data.set_index('Category'))
        
        # Column 2: Recommendations and strengths
        with col2:
            # Resume Strengths
            st.subheader("Resume Strengths")
            for strength in analysis["resume_strengths"]:
                st.markdown(f"✨ {strength}")
            
            # Improvement Recommendations
            st.subheader("Recommended Improvements")
            for recommendation in analysis["improvement_recommendations"]:
                st.markdown(f"📝 {recommendation}")
            
            # Detailed Analysis
            st.subheader("Detailed Analysis")
            st.write(analysis["detailed_analysis"])
        
    except json.JSONDecodeError:
        st.error("Error parsing the analysis response. Please try again.")
        st.text(analysis_json)
    except KeyError as e:
        st.error(f"Error: Missing key {e} in analysis response.")
        st.text(analysis_json)

def main():
    # Sidebar for app navigation
    st.sidebar.title("ResumeMatch ATS System")
    st.sidebar.image("https://static.vecteezy.com/system/resources/previews/011/484/460/non_2x/recruitment-interview-vacancy-job-search-hr-check-resume-free-png.png", width=200)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["ATS Scanner", "Resume Tips", "About"])
    
    with tab1:
        st.header("Resume ATS Scanner")
        st.markdown("""
        This tool helps you analyze how well your resume matches a specific job description using Google Gemini Pro AI.
        Upload your resume and paste the job description to get a detailed analysis.
        """)
        
        # File uploader for resume
        uploaded_file = st.file_uploader("Upload your Resume (PDF, DOCX, TXT)", type=['pdf', 'docx', 'doc', 'txt'])
        
        # Job description input
        job_description = st.text_area("Paste the Job Description here", height=200)
        
        if uploaded_file is not None and job_description:
            if st.button("Analyze Resume"):
                with st.spinner("Analyzing your resume..."):
                    # Extract text from resume
                    resume_text = extract_text_from_file(uploaded_file)
                    
                    # Get sample of extracted text to show user
                    preview_length = min(1000, len(resume_text))
                    with st.expander("Resume Text Preview"):
                        st.markdown(f"**First {preview_length} characters extracted from resume:**")
                        st.text(resume_text[:preview_length] + "...")
                    
                    # Get analysis from Gemini
                    analysis_json = get_gemini_response(resume_text, job_description)
                    
                    # Display the analysis
                    display_analysis(analysis_json)
                    
                    # Provide download option for the analysis
                    buffer = StringIO()
                    buffer.write(analysis_json)
                    st.download_button(
                        label="Download Analysis Report",
                        data=buffer.getvalue(),
                        file_name="resume_analysis.json",
                        mime="application/json"
                    )
    
    with tab2:
        st.header("Resume Optimization Tips")
        st.markdown("""
        ### How to Optimize Your Resume for ATS
        
        1. **Use keywords from the job description**
           - Identify important skills and terms in the job posting
           - Incorporate these keywords naturally throughout your resume
        
        2. **Maintain a clean, simple format**
           - Use standard section headings (Experience, Education, Skills)
           - Avoid complex formatting, tables, or graphics
           - Use a standard font like Arial, Calibri, or Times New Roman
        
        3. **Include a skills section**
           - List both hard skills (technical abilities) and soft skills
           - Prioritize skills mentioned in the job posting
        
        4. **Quantify achievements**
           - Use numbers and percentages to showcase results
           - Be specific about your accomplishments
        
        5. **Use standard file formats**
           - Save your resume as a .docx or .pdf file
           - Avoid image-based files (.jpg, .png) or specialized formats
        
        6. **Avoid headers and footers**
           - Some ATS systems can't properly read content in headers/footers
           - Put all important information in the main body of the document
        
        7. **Proofread carefully**
           - Spelling and grammar errors can negatively impact ATS scoring
        """)
    
    with tab3:
        st.header("About This Application")
        st.markdown("""
        ### Resume ATS Analyzer
        
        This application uses Google's Gemini Pro language model to analyze how well your resume matches a specific job description.
        
        **Features:**
        - Resume text extraction from PDF, DOCX, and TXT files
        - Detailed matching analysis against job descriptions
        - Skill gap identification
        - Tailored improvement recommendations
        - Resume strength highlights
        
        **How it works:**
        1. You upload your resume
        2. You paste the job description
        3. Gemini AI analyzes the match between your resume and the job requirements
        4. The application displays a comprehensive analysis with actionable insights
        
        **Privacy Notice:**
        - Your resume and job description data are only used for this analysis
        - No data is stored permanently on our servers
        - The analysis is performed using Google's Gemini Pro API
        """)

if __name__ == "__main__":
    main()