import json
from pathlib import Path

_taxonomy = None

def get_skills_taxonomy():
    global _taxonomy
    if _taxonomy is None:
        skills_path = Path(__file__).resolve().parents[2] / "ml_artifacts/skills_taxonomy.json"
        with open(skills_path, "r") as f:
            _taxonomy = json.load(f)
    return _taxonomy

_variations = None

def get_skill_variations():
    global _variations
    if _variations is None:
        db = get_skills_taxonomy()
        variations = {}
        for category, skill_list in db.items():
            for skill in skill_list:
                variations[skill.lower()] = skill
                if '.' in skill:
                    variations[skill.replace('.', '').lower()] = skill
                if ' ' in skill:
                    variations[skill.replace(' ', '').lower()] = skill
                    variations[skill.replace(' ', '-').lower()] = skill
        _variations = variations
    return _variations
