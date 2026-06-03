import re
from typing import Dict
def _extract_education(self, text: str) -> Dict:
        """Extract education"""
        education = {
            'degrees': [],
            'institutions': [],
            'raw_sections': []
        }
        
        # Find education section
        edu_pattern = r'EDUCATION|ACADEMIC\s+BACKGROUND|QUALIFICATIONS'
        match = re.search(edu_pattern, text, re.IGNORECASE)
        
        if match:
            edu_text = text[match.end():]
            sections = re.split(r'\n{2,}', edu_text[:500])
            education['raw_sections'] = [s.strip() for s in sections if len(s.strip()) > 10]
            
            # Common degrees
            degree_keywords = [
                'bachelor', 'master', 'phd', 'doctorate', 'mba',
                'b.s.', 'm.s.', 'b.a.', 'm.a.', 'b.tech', 'm.tech'
            ]
            
            for section in education['raw_sections']:
                section_lower = section.lower()
                for degree in degree_keywords:
                    if degree in section_lower:
                        education['degrees'].append(section)
                        break
        
        return education
    