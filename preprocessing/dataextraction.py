import os
from typing import List, Dict
from PyPDF2 import PdfReader
from docx import Document

class DocumentProcessor:
    """A class to process PDF and DOCX files and extract text content."""
    
    def __init__(self, input_directory: str, output_directory: str):
        self.input_directory = input_directory
        self.output_directory = output_directory
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    
    def extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error processing PDF {file_path}: {str(e)}")
            return ""

    def extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error processing DOCX {file_path}: {str(e)}")
            return ""

    def process_files(self) -> Dict[str, str]:
        """Process all PDF and DOCX files in the input directory."""
        results = {}
        
        for filename in os.listdir(self.input_directory):
            file_path = os.path.join(self.input_directory, filename)
            
            if filename.lower().endswith('.pdf'):
                text = self.extract_from_pdf(file_path)
                output_filename = filename[:-4] + '.txt'
            elif filename.lower().endswith('.docx'):
                text = self.extract_from_docx(file_path)
                output_filename = filename[:-5] + '.txt'
            else:
                continue
                
            # Save extracted text to output file
            output_path = os.path.join(self.output_directory, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results[filename] = output_path
            
        return results

def main():
    # Configure input and output directories
    input_dir = "input_documents"
    output_dir = "extracted_text"
    
    # Create processor instance
    processor = DocumentProcessor(input_dir, output_dir)
    
    # Process all files
    results = processor.process_files()
    
    # Print results
    print("\nProcessing Complete!")
    print("-" * 50)
    for input_file, output_file in results.items():
        print(f"Processed {input_file} -> {output_file}")

if __name__ == "__main__":
    main()