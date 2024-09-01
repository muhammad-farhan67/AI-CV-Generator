import streamlit as st
import os
from groq import Groq
import io  
from docx import Document
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import base64

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

def main():
    st.set_page_config(
        page_title="JobMate AI",
        page_icon="pic.png",  
        layout="wide"
    )

    # Enhanced Styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {
            color: #2C3E50;
            background-color: #ECF0F1;
            font-family: 'Roboto', sans-serif;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #3498DB;
            border-radius: 5px;
            border: none;
            padding: 10px 24px;
            transition: all 0.3s ease 0s;
        }
        .stButton>button:hover {
            background-color: #2980B9;
        }
        h1, h2 {
            color: #87CEEB;
            font-size: 36px;
            text-align: center;
            margin-top: 20px;
            animation: fadeInDown 1s ease-in-out;
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .reportview-container .markdown-text-container {
            font-family: 'Roboto', sans-serif;
            color: #2C3E50;
            font-size: 18px;
        }
        .card {
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 20px auto;
            max-width: 800px;
            transition: all 0.3s ease;
            text-align: center;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        .card h3 {
            color: #3498DB;
            font-size: 24px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .card p {
            color: #2C3E50;
        }
        .stRadio > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        .stRadio > div > label {
            background-color: #ffffff;
            border-radius: 5px;
            padding: 15px;
            width: 80%;
            text-align: center;
            border: 1px solid #3498DB;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 400;
            color: #2C3E50;
        }
        .stRadio > div > label:hover, .stRadio > div > label[data-baseweb="radio"]:hover {
            background-color: #E8F6FF;
            color: #3498DB;
        }
        .stRadio > div > label[data-baseweb="radio"]:checked {
            background-color: #3498DB;
            color: #ffffff;
            animation: pulse 0.5s;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: -30px;
        }
        .logo {
            max-width: 50px;
            animation: fadeIn 1s ease-in-out;
        }
        .welcome-message {
            text-align: center;
            font-size: 28px;
            color: #87CEEB;
            margin-top: 20px;
            animation: fadeIn 1s ease-in-out;
            font-weight: 700;
        }
        .sidebar .sidebar-content {
            background-color: #F0F8FF;
        }
        .sidebar .sidebar-content h3 {
            color: #87CEEB;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        @keyframes fadeInDown {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        </style>
        """, unsafe_allow_html=True)

    # Display logo
    display_logo()

    # Sidebar navigation with styled radio buttons
    st.sidebar.markdown("<h1>Navigate<h1>", unsafe_allow_html=True)
    page = st.sidebar.radio("", ["Welcome To JOBMATE AI", "Personalized Cover Letter", "Generate Interview Questions", "Answers To Custom Questions"], key="navigation")

    if page == "Welcome To JOBMATE AI":
        display_home_page()
    elif page == "Personalized Cover Letter":
        handle_cv_cover_letter_generation()
    elif page == "Generate Interview Questions":
        handle_interview_question_generation()
    elif page == "Answers To Custom Questions":
        handle_custom_question()

def display_logo():
    """Displays the JobMate AI logo."""
    
    logo_path = 'pic.png'
    
    # Read the image file and encode it to base64
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # Display the image using HTML
    st.markdown(f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{encoded_string}" alt="JobMate AI Logo" class="logo">
    </div>
    """, unsafe_allow_html=True)

def display_home_page():
    """Displays the home page with information about the application."""
    st.markdown('<div class="welcome-message">Welcome to JobMate AI</div>', unsafe_allow_html=True)
    st.markdown("<h1>Your Path to Professional Success</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h3>Cover Letter Assistance</h3>
        <p>Generate tailored cover letters that complement your CVs, enhancing your job application and increasing your chances of landing interviews.</p>
    </div>
    <div class="card">
        <h3>Interview Preparation</h3>
        <p>Prepare for interviews with custom questions based on the job description you are applying for, helping you to better anticipate and prepare for potential questions.</p>
    </div>
    <div class="card">
        <h3>AI-Driven Insights</h3>
        <p>Leverage advanced AI techniques, including Retrieval-Augmented Generation (RAG), to ensure your applications are optimized and relevant.</p>
    </div>
    <div class="card">
        <h3>Custom Question Answering</h3>
        <p>Get answers to your specific questions about the job or company using our AI-powered custom question feature.</p>
    </div>
    """, unsafe_allow_html=True)
    

def handle_job_description_input():
    """Handles job description input, allowing both file upload and text input."""
    job_description_file = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=['pdf', 'docx', 'txt'])
    job_description_text = st.text_area("Or paste the job description here")
    
    if job_description_file:
        return read_file(job_description_file)
    elif job_description_text:
        return job_description_text
    else:
        return None

def handle_cv_cover_letter_generation():
    """Handles the CV/Cover Letter generation process."""
    st.markdown("<h1>Generate Personalized Cover Letter</h1>", unsafe_allow_html=True)

    with st.form(key='cv_form'):
        job_description = handle_job_description_input()
        cv_file = st.file_uploader("Upload Your CV (PDF or DOCX)", type=['pdf', 'docx'])
        submit_button = st.form_submit_button("Generate Cover Letter")

    if submit_button:
        if not job_description or not cv_file:
            st.error("Please provide both the job description and your CV.")
        else:
            try:
                cv_content = read_file(cv_file)
                cover_letter = generate_cover_letter(job_description, cv_content)
                st.markdown(f"<div class='card'><h3>Generated Cover Letter:</h3><p>{cover_letter}</p></div>", unsafe_allow_html=True)
                
                # Download button for the cover letter
                if st.button("Download as PDF"):
                    pdf = create_pdf(cover_letter, "Cover Letter")
                    st.download_button(
                        label="Download as PDF",
                        data=pdf,
                        file_name="cover_letter.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def handle_interview_question_generation():
    """Handles the interview question generation process."""
    st.markdown("<h1>Generate Interview Questions</h1>", unsafe_allow_html=True)

    with st.form(key='interview_form'):
        job_description = handle_job_description_input()
        cv_file = st.file_uploader("Upload Your CV (PDF or DOCX)", type=['pdf', 'docx'])
        submit_interview_button = st.form_submit_button("Generate Interview Questions")

    if submit_interview_button:
        if not job_description or not cv_file:
            st.error("Please provide both the job description and your CV.")
        else:
            try:
                cv_content = read_file(cv_file)
                interview_questions = generate_interview_questions(job_description, cv_content)
                st.markdown(f"<div class='card'><h3>Generated Interview Questions:</h3><p>{interview_questions}</p></div>", unsafe_allow_html=True)
                
                # Download button for the interview questions
                if st.button("Download as PDF"):
                    pdf = create_pdf(interview_questions, "Interview Questions")
                    st.download_button(
                        label="Download as PDF",
                        data=pdf,
                        file_name="interview_questions.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def handle_custom_question():
    """Handles the custom question answering process."""
    st.markdown("<h1>Generate Answers to Custom Questions</h1>", unsafe_allow_html=True)

    with st.form(key='custom_question_form'):
        cv_file = st.file_uploader("Upload Your CV (PDF or DOCX)", type=['pdf', 'docx'])
        job_description = handle_job_description_input()
        custom_question = st.text_area("Enter your custom question")
        submit_custom_question_button = st.form_submit_button("Get Answer")

    if submit_custom_question_button:
        if not cv_file or not job_description or not custom_question:
            st.error("Please provide your CV, job description, and enter a custom question.")
        else:
            try:
                cv_content = read_file(cv_file)
                custom_answer = answer_custom_question(cv_content, job_description, custom_question)
                st.markdown(f"<div class='card'><h3>Answer to Custom Question:</h3><p>{custom_answer}</p></div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def read_file(file):
    """Reads content from PDF, DOCX, or TXT file."""
    if file.type == "application/pdf":
        return read_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(file)
    else:
        return file.getvalue().decode("utf-8")

def read_pdf(file):
    """Reads content from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    """Reads content from a DOCX file."""
    doc = Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def create_pdf(content, title):
    """Creates a PDF file from the given content."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []

    # Add title
    flowables.append(Paragraph(title, styles['Title']))
    flowables.append(Spacer(1, 12))

    # Add content
    for paragraph in content.split('\n'):
        if paragraph.strip():
            flowables.append(Paragraph(paragraph, styles['Normal']))
            flowables.append(Spacer(1, 6))

    doc.build(flowables)
    buffer.seek(0)
    return buffer

def generate_cover_letter(job_description, cv_content):
    """Generates a cover letter based on the job description and CV content."""
    prompt = f"""
    Given the following job description and CV, generate a tailored cover letter:

    Job Description:
    {job_description}

    CV:
    {cv_content}

    Generate a professional cover letter that highlights the applicant's relevant skills and experiences for this specific job.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert in resume writing and job applications."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.6,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error in generating cover letter: {str(e)}")

def generate_interview_questions(job_description, cv_content):
    """Generates interview questions based on the job description and CV content."""
    prompt = f"""
    Based on the following job description and CV, generate a list of potential interview questions:

    Job Description:
    {job_description}

    CV:
    {cv_content}

    Generate 5 specific interview questions that are tailored to this job and the applicant's background. Format the questions as a numbered list.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert in conducting job interviews."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error in generating interview questions: {str(e)}")

def answer_custom_question(cv_content, job_description, custom_question):
    """Answers a custom question based on the CV, job description, and the question itself."""
    prompt = f"""
    Given the following CV and job description, please answer the custom question:

    CV:
    {cv_content}

    Job Description:
    {job_description}

    Custom Question:
    {custom_question}

    Provide a detailed and relevant answer to the custom question, considering the information from both the CV and job description.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert career advisor with deep knowledge of various industries and job roles."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error in answering custom question: {str(e)}")


if __name__ == "__main__":
    main()
