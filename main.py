import os
from preprocessing.dataextraction import DocumentProcessor

def main():
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Configure input directory relative to the script location
    input_dir = os.path.join(current_dir, 'datafiles', 'Input_files', 'sample resume')
    
    # Database URI - adjust as needed
    db_uri = "mysql+pymysql://root:123456@localhost:3306/resume_db"  # Example using SQLite, replace with actual DB URI
    
    # Create processor instance
    processor = DocumentProcessor(input_dir, None, db_uri)
    
    # Process all files and insert mapped data into DB
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if filename.lower().endswith('.pdf'):
            analysis = processor.process_pdf(file_path)
        elif filename.lower().endswith('.docx'):
            analysis = processor.process_docx(file_path)
        else:
            continue
        
        if analysis:
            # Insert mapped data into database
            success = processor.map_and_insert(filename, analysis)
            if success:
                print(f"Processed and inserted data for {filename}")
            else:
                print(f"Failed to insert data for {filename}")

if __name__ == "__main__":
    main()
