import streamlit as st
import os
from preprocessing.database.db_manager import DatabaseManager
from preprocessing.processors.document_processor import DocumentProcessor

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/resume_db"

# Helper function to parse job description input into a simple object
class JobDescription:
    def __init__(self, skills, experience, education):
        self.required_skills = [skill.strip().lower() for skill in skills.split(',')] if skills else []
        self.required_experience = float(experience) if experience else 0.0
        self.required_education = education.strip().lower() if education else ""

def extract_resume_data(uploaded_file):
    processor = DocumentProcessor()
    name = uploaded_file.name
    temp_path = os.path.join("temp_uploads", name)
    os.makedirs("temp_uploads", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    if name.lower().endswith('.pdf'):
        analysis = processor.process_pdf(temp_path)
    elif name.lower().endswith('.docx'):
        analysis = processor.process_docx(temp_path)
    else:
        analysis = None
    os.remove(temp_path)

    extracted_data = {
        'name': name,
        'email': analysis.get('email', '') if analysis else '',
        'phone': analysis.get('phone', '') if analysis else '',
        'linkedin': analysis.get('linkedin', '') if analysis else '',
        'github': analysis.get('github', '') if analysis else '',
        'total_experience': 0.0,
        'highest_qualification': '',
        'university': analysis.get('university', '') if analysis else '',
        'location': analysis.get('location', '') if analysis else '',
        'resume_text': analysis.get('text', '') if analysis else '',
        'skills': [],
        'projects': [],
        'work_experience': [],
        'certifications': [],
        'analysis_insights': {}
    }

    if analysis:
        extracted_data['skills'] = [{'name': skill.lower(), 'proficiency': None} for skill in analysis.get('skills', [])]
        if 'dates' in analysis and 'experience' in analysis['dates']:
            extracted_data['total_experience'] = len(analysis['dates']['experience'])
        if 'entities' in analysis and 'ORG' in analysis['entities']:
            extracted_data['highest_qualification'] = "bachelor"  # Placeholder, can be improved

    return extracted_data

def main():
    st.title("Recruiter Resume Upload App")

    db_manager = DatabaseManager(DATABASE_URL)

    tab1, tab2 = st.tabs(["Recruiter - Add Job Description", "User - Upload Resumes"])

    with tab1:
        st.header("Enter Job Description")
        skills_input = st.text_input("Required Skills (comma separated)", "")
        experience_input = st.text_input("Required Experience (years)", "")
        education_input = st.text_input("Required Education", "")

    with tab2:
        st.header("Upload Resumes")
        uploaded_files = st.file_uploader("Upload one or more resumes (PDF, DOCX)", type=['pdf', 'docx'], accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                extracted_data = extract_resume_data(uploaded_file)
                try:
                    candidate_id = db_manager.insert_candidate_data(extracted_data)
                    st.success(f"Stored resume '{uploaded_file.name}' in database with candidate ID {candidate_id}.")
                except Exception as e:
                    st.error(f"Failed to store resume '{uploaded_file.name}': {str(e)}")

if __name__ == "__main__":
    main()
