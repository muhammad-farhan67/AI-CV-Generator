import streamlit as st

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
            color: #00BFFF;  /* Sky blue color */
            font-size: 36px;
            text-align: center;
        }
        h2 {
            color: #00BFFF;  /* Sky blue color */
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
            color: #333; /* Dark color for text in card */
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar navigation
    page = st.sidebar.selectbox("Navigate", ["Home", "CV/Cover Letter Generation", "Interview Question Generation"])

    if page == "Home":
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

    elif page == "CV/Cover Letter Generation":
        with st.form(key='cv_form'):
            job_description = st.text_area("Job Description", help="Describe the job you are applying for.")
            skills = st.text_input("Skills", help="List your relevant skills separated by commas.")
            education = st.text_input("Education", help="Describe your highest level of education.")
            submit_button = st.form_submit_button("Generate CV/Cover Letter")

        if submit_button:
            user_data = {
                "job_description": job_description,
                "skills": skills.split(','),
                "education": education
            }
            generated_cv = rag_technique_cv_generation(user_data)
            st.markdown(f"<div class='card'>{generated_cv}</div>", unsafe_allow_html=True)

    elif page == "Interview Question Generation":
        with st.form(key='interview_form'):
            job_description = st.text_area("Job Description for Interview", help="Describe the job you are applying for to generate interview questions.")
            submit_interview_button = st.form_submit_button("Generate Interview Questions")

        if submit_interview_button:
            interview_questions = generate_interview_questions(job_description)
            st.markdown(f"<div class='card'>{interview_questions}</div>", unsafe_allow_html=True)

def rag_technique_cv_generation(user_data):
    job_desc = user_data['job_description']
    skills = ', '.join(user_data['skills'])
    education = user_data['education']
    cv_content = f"""
    **Job Description:** {job_desc}
    **Skills:** {skills}
    **Education:** {education}
    **Experience:** Generated based on job description and skills using RAG.
    """
    return cv_content

def generate_interview_questions(job_description):
    questions = f"**Sample Interview Questions for:** {job_description}\n1. How do your skills match this job?\n2. What experiences make you a good candidate?"
    return questions

if __name__ == "__main__":
    main()
