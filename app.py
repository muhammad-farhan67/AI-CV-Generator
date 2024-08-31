import streamlit as st
import os
from groq import Groq

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

def main():
    st.title('Personalized CV Generator')

    # Enhanced Styling for visibility and aesthetics
    st.markdown("""
        <style>
        body {
            color: #4a4a4a;
            background-color: #f0f2f6;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #4a90e2;
        }
        h1 {
            color: #00BFFF;
            font-size: 36px;
            text-align: center;
        }
        h2 {
            color: #00BFFF;
            font-size: 30px;
            text-align: center;
        }
        .reportview-container .markdown-text-container {
            font-family: sans-serif;
            color: #4a4a4a;
            font-size: 18px;
            text-align: center;
        }
        .card {
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin: 10px;
            text-align: center;
            color: #333;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar navigation
    page = st.sidebar.selectbox("Navigate", ["Home", "Cover Letter Generation", "Interview Questions Generation"])

    if page == "Home":
        display_home_page()
    elif page == "Cover Letter Generation":
        handle_cv_cover_letter_generation()
    elif page == "Interview Questions Generation":
        handle_interview_question_generation()

def display_home_page():
    """Displays the home page with information about the application."""
    st.header("Welcome to the Personalized CV Generator")
    st.markdown("""
    <div class="card">
        <h2>Personalized CVs</h2>
        <p>This application assists job seekers by generating personalized CVs tailored to specific job descriptions and company profiles.</p>
    </div>
    <div class="card">
        <h2>Cover Letter Assistance</h2>
        <p>Generate cover letters that complement your CVs, enhancing your job application and increasing your chances of landing interviews.</p>
    </div>
    <div class="card">
        <h2>Interview Preparation</h2>
        <p>Prepare for interviews with custom questions based on the job description you are applying for, helping you to better anticipate and prepare for potential questions.</p>
    </div>
    <div class="card">
        <h2>AI-Driven Insights</h2>
        <p>Leverage advanced AI techniques, including the Retrieval-Augmented Generation (RAG), to ensure your applications are optimized and relevant.</p>
    </div>
    """, unsafe_allow_html=True)

def handle_cv_cover_letter_generation():
    """Handles the CV/Cover Letter generation process."""
    with st.form(key='cv_form'):
        job_description = st.text_area("Job Description", help="Describe the job you are applying for.")
        cv_content = st.text_area("Your CV", help="Paste your current CV here.")
        submit_button = st.form_submit_button("Generate Cover Letter")

    if submit_button:
        if not job_description or not cv_content:
            st.error("Please provide both the job description and your CV.")
        else:
            try:
                cover_letter = generate_cover_letter(job_description, cv_content)
                st.markdown(f"<div class='card'><h3>Generated Cover Letter:</h3>{cover_letter}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred while generating the cover letter: {str(e)}")

def handle_interview_question_generation():
    """Handles the interview question generation process."""
    with st.form(key='interview_form'):
        job_description = st.text_area("Job Description for Interview", help="Describe the job you are applying for to generate interview questions.")
        cv_content = st.text_area("Your CV", help="Paste your current CV here.")
        submit_interview_button = st.form_submit_button("Generate Interview Questions")

    if submit_interview_button:
        if not job_description or not cv_content:
            st.error("Please provide both the job description and your CV.")
        else:
            try:
                interview_questions = generate_interview_questions(job_description, cv_content)
                st.markdown(f"<div class='card'><h3>Generated Interview Questions:</h3>{interview_questions}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred while generating interview questions: {str(e)}")

def generate_cover_letter(job_description, cv_content):
    """
    Generates a cover letter based on the job description and CV content.
    
    Args:
    job_description (str): The job description.
    cv_content (str): The content of the user's CV.
    
    Returns:
    str: The generated cover letter.
    """
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
            temperature=0.5,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error in generating cover letter: {str(e)}")

def generate_interview_questions(job_description, cv_content):
    """
    Generates interview questions based on the job description and CV content.
    
    Args:
    job_description (str): The job description.
    cv_content (str): The content of the user's CV.
    
    Returns:
    str: The generated interview questions.
    """
    prompt = f"""
    Based on the following job description and CV, generate a list of potential interview questions:

    Job Description:
    {job_description}

    CV:
    {cv_content}

    Generate 5 specific interview questions that are tailored to this job and the applicant's background.
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

if __name__ == "__main__":
    main()
