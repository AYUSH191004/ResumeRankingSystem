import re
from typing import Dict
def _extract_experience(self, text: str) -> Dict:
        """Extract work experience"""
        experience = {
            'raw_sections': [],
            'years_of_experience': 0,
            'companies': [],
            'titles': []
        }
        
        # Find experience section
        exp_pattern = r'(?:WORK\s+)?EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EMPLOYMENT\s+HISTORY'
        match = re.search(exp_pattern, text, re.IGNORECASE)
        
        if match:
            # Extract text after experience header
            exp_text = text[match.end():]
            
            # Split by common delimiters
            sections = re.split(r'\n{2,}', exp_text[:1000])  # First 1000 chars
            experience['raw_sections'] = [s.strip() for s in sections if len(s.strip()) > 20]
            
            # Extract years (rough estimate)
            year_mentions = re.findall(r'\b(20\d{2}|19\d{2})\b', exp_text)
            if len(year_mentions) >= 2:
                years = sorted([int(y) for y in year_mentions])
                experience['years_of_experience'] = years[-1] - years[0]
        
        return experience
