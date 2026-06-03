"""
Extract skills from resume text
"""
import json
import re
from typing import List, Dict, Set
from pathlib import Path
from rapidfuzz import fuzz, process
from app.ml.Resources.nlp import get_spacy
from app.ml.Resources import skilltaxanomy

class SkillExtractor:
    """Extract skills from resume text using NLP and fuzzy matching"""
    
    def __init__(self, skills_db_path: str = "ml_artifacts/skills_taxonomy.json"):
        # Load spaCy model
        self.nlp = get_spacy()
        
        # Load skills database
        self.skills_db = skilltaxanomy.get_skills_taxonomy()
        
        # Flatten all skills into a searchable list
        self.all_skills = self._flatten_skills()
        
        # Create lowercase mapping for exact matching
        self.skill_variations = skilltaxanomy.get_skill_variations()

    
    def _flatten_skills(self) -> List[str]:
        """Flatten skills from all categories"""
        skills = []
        for category, skill_list in self.skills_db.items():
            skills.extend(skill_list)
        return skills
 
    
    def extract(self, text: str) -> Dict[str, any]:
        """
        Extract skills from text
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with extracted skills by category
        """
        if not text:
            return self._empty_result()
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # Extract using multiple methods
        exact_matches = self._extract_exact_matches(text)
        fuzzy_matches = self._extract_fuzzy_matches(text)
        context_skills = self._extract_from_context(doc)
        
        # Combine and deduplicate
        all_found_skills = set(exact_matches + fuzzy_matches + context_skills)
        
        # Categorize skills
        categorized = self._categorize_skills(all_found_skills)
        
        return {
            'all_skills': sorted(list(all_found_skills)),
            'by_category': categorized,
            'count': len(all_found_skills),
            'confidence': self._calculate_confidence(len(all_found_skills))
        }
    
    def _extract_exact_matches(self, text: str) -> List[str]:
        """Find exact and variation matches"""
        found = set()
        text_lower = text.lower()
        
        # Check each skill variation
        for variation, canonical in self.skill_variations.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(variation) + r'\b'
            if re.search(pattern, text_lower):
                found.add(canonical)
        
        return list(found)
    
    def _extract_fuzzy_matches(self, text: str, threshold: int = 85) -> List[str]:
        """Find fuzzy matches for potential typos"""
        found = set()
        
        # Split text into words/phrases
        words = re.findall(r'\b[A-Za-z][A-Za-z+#.]+\b', text)
        
        for word in words:
            if len(word) < 3:  # Skip very short words
                continue
            
            # Find best match
            match = process.extractOne(
                word.lower(),
                [s.lower() for s in self.all_skills],
                scorer=fuzz.ratio
            )
            
            if match and match[1] >= threshold:
                # Find original skill name
                matched_skill = next(
                    (s for s in self.all_skills if s.lower() == match[0]),
                    None
                )
                if matched_skill:
                    found.add(matched_skill)
        
        return list(found)
    
    def _extract_from_context(self, doc) -> List[str]:
        """Extract skills mentioned in context"""
        found = set()
        
        # Look for common patterns
        skill_patterns = [
            r'experience (?:with|in) ([^,.]+)',
            r'proficient in ([^,.]+)',
            r'knowledge of ([^,.]+)',
            r'skilled in ([^,.]+)',
            r'expertise in ([^,.]+)',
        ]
        
        text = doc.text
        for pattern in skill_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                phrase = match.group(1).strip()
                # Check if phrase contains known skills
                for skill in self.all_skills:
                    if skill.lower() in phrase.lower():
                        found.add(skill)
        
        return list(found)
    
    def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Organize skills by category"""
        categorized = {category: [] for category in self.skills_db.keys()}
        
        for skill in skills:
            for category, skill_list in self.skills_db.items():
                if skill in skill_list:
                    categorized[category].append(skill)
                    break
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def _calculate_confidence(self, skill_count: int) -> float:
        """Calculate confidence score based on number of skills found"""
        if skill_count == 0:
            return 0.0
        elif skill_count < 3:
            return 0.3
        elif skill_count < 8:
            return 0.6
        elif skill_count < 15:
            return 0.8
        else:
            return 1.0
    
    def _empty_result(self) -> Dict:
        """Return empty result structure"""
        return {
            'all_skills': [],
            'by_category': {},
            'count': 0,
            'confidence': 0.0
        }
