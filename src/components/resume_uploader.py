import streamlit as st
import os

def save_uploaded_file(uploaded_file, target_dir):
    """Save the uploaded file to the target directory"""
    try:
        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(target_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        return False

def main():
    st.title("Resume Uploader")
    st.write("Upload your resume in PDF or DOCX format")
    
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_dir = os.path.join(current_dir, 'src', 'components', 'datafiles', 'Input_files', 'sample resume')
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])
    
    if uploaded_file is not None:
        # Save the file silently
        success = save_uploaded_file(uploaded_file, input_dir)
        
        if success:
            st.success("File uploaded successfully!")
        else:
            st.error("Error uploading file. Please try again.")

if __name__ == "__main__":
    main() 