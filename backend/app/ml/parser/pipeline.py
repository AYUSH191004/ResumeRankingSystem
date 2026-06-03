"""
Main resume parser - orchestrates all extraction
"""
import os
import re
from typing import Dict, Optional
from datetime import datetime
from app.ml.Ingestion.text_extractor import  ResumeTextExtractor
from app.ml.parser.extractor.skill_extractor import SkillExtractor
from app.ml.parser.extractor.contacts import _extract_contact
from app.ml.parser.extractor.experience import _extract_experience
from app.ml.parser.extractor.education import _extract_education
from app.ml.parser.models import _empty_result
from app.ml.Resources.nlp import get_spacy 
from app.ml.features.skill_features import build_skill_embeddings



class ResumeParser:
    """Complete resume parsing pipeline"""
    
    def __init__(self):
        self.text_extractor = ResumeTextExtractor()
        self.skill_extractor = SkillExtractor()
        self.nlp = get_spacy()  # Loaded once from nlp.py
        self._extract_contact = _extract_contact.__get__(self)
        self._extract_experience = _extract_experience.__get__(self)
        self._extract_education = _extract_education.__get__(self)
        self._empty_result = _empty_result.__get__(self)
    
    def parse(self, file_path: str) -> Dict:
        """
        Parse a resume file completely

        Args:
            file_path: Path to resume file

        Returns:
            Structured resume data
        """

        # Step 1: Extract text
        text = self.text_extractor.extract(file_path)

        if not text:
            return self._empty_result("Text extraction failed")

        if not self.text_extractor.is_valid_resume(text):
            return self._empty_result("Invalid resume format")

        # Step 2: Parse with spaCy
        doc = self.nlp(text)

        # Step 3: Extract skills FIRST
        skills_data = self.skill_extractor.extract(text)

        # Extract actual skill list
        skills_list = skills_data.get("all_skills", [])

        # Step 4: Generate skill embeddings (FEATURE LAYER)
        skill_embeddings = build_skill_embeddings(skills_list)

        # Step 5: Build final structured result
        result = {
            'file_name': os.path.basename(file_path),
            'parsed_at': datetime.utcnow().isoformat(),
            '_raw_text': text,
            'text_length': len(text),

            # Contact info
            'contact': self._extract_contact(text, doc),

            # Skills (structured + embeddings)
            'skills': skills_data,
            'skill_embeddings': skill_embeddings,

            # Experience
            'experience': self._extract_experience(text),

            # Education
            'education': self._extract_education(text),

            # Summary stats
            'stats': {
                'word_count': len(text.split()),
                'has_email': '@' in text,
                'has_phone': bool(re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', text)),
                'has_linkedin': 'linkedin' in text.lower(),
                'has_github': 'github' in text.lower(),
            },

            'status': 'success'
        }

        return result
