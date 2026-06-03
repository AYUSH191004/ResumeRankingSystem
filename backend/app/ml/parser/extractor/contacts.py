import re
from typing import Dict
def _extract_contact(self, text: str, doc) -> Dict:
        """Extract contact information"""
        contact = {
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None,
            'location': None
        }
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone
        phone_match = re.search(r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}', text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/([a-zA-Z0-9-]+)', text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(0)
        
        # GitHub
        github_match = re.search(r'github\.com/([a-zA-Z0-9-]+)', text, re.IGNORECASE)
        if github_match:
            contact['github'] = github_match.group(0)
        
        # Location (use spaCy NER)
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        if locations:
            contact['location'] = locations[0]
        
        return contact