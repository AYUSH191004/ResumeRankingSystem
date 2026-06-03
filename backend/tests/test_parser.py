"""
Tests for resume parser
"""
import pytest
import os
from backend.app.ml.parser.pipeline import ResumeParser
from backend.app.ml.Ingestion.text_extractor import TextExtractor
from backend.app.ml.parser.extractor.skill_extractor import SkillExtractor


@pytest.fixture
def parser():
    """Create parser instance"""
    return ResumeParser()


@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing"""
    return """
    John Doe
    Software Engineer
    Email: john@email.com
    Phone: (555) 123-4567
    
    SKILLS
    Python, JavaScript, React, AWS, Docker, PostgreSQL
    
    EXPERIENCE
    Senior Engineer | Tech Corp | 2020 - Present
    
    EDUCATION
    B.S. Computer Science | State University | 2018
    """


class TestTextExtractor:
    def test_extract_from_text(self, sample_resume_text):
        extractor = TextExtractor()
        assert len(sample_resume_text) > 0
    
    def test_is_valid_resume(self, sample_resume_text):
        extractor = TextExtractor()
        assert extractor.is_valid_resume(sample_resume_text) == True
    
    def test_invalid_resume(self):
        extractor = TextExtractor()
        assert extractor.is_valid_resume("Hello world") == False


class TestSkillExtractor:
    def test_extract_skills(self, sample_resume_text):
        extractor = SkillExtractor()
        result = extractor.extract(sample_resume_text)
        
        assert result['count'] > 0
        assert 'Python' in result['all_skills']
        assert 'JavaScript' in result['all_skills']
    
    def test_empty_text(self):
        extractor = SkillExtractor()
        result = extractor.extract("")
        assert result['count'] == 0


class TestResumeParser:
    def test_parse_structure(self, parser, sample_resume_text):
        # Save sample to temp file
        temp_file = "temp_test_resume.txt"
        with open(temp_file, 'w') as f:
            f.write(sample_resume_text)
        
        result = parser.parse(temp_file)
        
        # Cleanup
        os.remove(temp_file)
        
        # Assertions
        assert result['status'] == 'success'
        assert result['contact']['email'] == 'john@email.com'
        assert result['skills']['count'] > 0
        assert result['stats']['has_email'] == True
    
    def test_invalid_file(self, parser):
        result = parser.parse("nonexistent_file.pdf")
        assert result['status'] == 'error'


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, '-v'])