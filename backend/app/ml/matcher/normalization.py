import re
from datetime import datetime


def normalize_resume_skills(parsed_data: dict) -> list:
    if not parsed_data:
        return []

    skills = parsed_data.get("skills", {})

    # flat list
    if isinstance(skills, list):
        return [s.lower().strip() for s in skills if s]

    # categorized dict
    if isinstance(skills, dict) and "by_category" in skills:
        collected = []
        for group in skills["by_category"].values():
            if isinstance(group, list):
                collected.extend(group)
        return [s.lower().strip() for s in collected if s]

    return []


def normalize_job_skills(required_skills: str) -> list:
    if not required_skills:
        return []

    return [
        s.strip().lower()
        for s in required_skills.split(",")
        if s.strip()
    ]



MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def _months_between(start, end):
    return (end.year - start.year) * 12 + (end.month - start.month)


def _parse_date(text):
    text = text.lower()

    # present handling
    if "present" in text or "current" in text:
        return datetime.now()

    # match "June 2025"
    m = re.search(r"([a-zA-Z]+)\s+(\d{4})", text)
    if m:
        month = MONTHS.get(m.group(1)[:3])
        year = int(m.group(2))
        if month:
            return datetime(year, month, 1)

    # match year only "2025"
    m = re.search(r"\b(20\d{2})\b", text)
    if m:
        return datetime(int(m.group(1)), 1, 1)

    return None


def _extract_from_ranges(raw_sections):
    total_months = 0

    for text in raw_sections:
        ranges = re.findall(r"([A-Za-z]+\s+\d{4})\s*[–-]\s*([A-Za-z]+\s+\d{4}|Present|Current)", text)

        for start_txt, end_txt in ranges:
            start = _parse_date(start_txt)
            end = _parse_date(end_txt)

            if start and end:
                months = max(0, _months_between(start, end))
                total_months += months

    return total_months / 12


def normalize_experience(parsed_data: dict) -> float:
    if not parsed_data:
        return 0

    exp = parsed_data.get("experience", {})

    # -----------------------
    # 1) explicit years field
    # -----------------------
    years = exp.get("years_of_experience") or exp.get("years")
    if isinstance(years, (int, float)):
        return float(years)

    if isinstance(years, str):
        m = re.search(r"\d+(\.\d+)?", years)
        if m:
            return float(m.group())

    # -----------------------
    # 2) infer from dates
    # -----------------------
    raw_sections = exp.get("raw_sections", [])
    if isinstance(raw_sections, list):

        # 1) try real duration
        inferred = _extract_from_ranges(raw_sections)
        if inferred > 0:
            return round(inferred, 2)

        # 2) fallback: exposure inference
        exposure = _infer_exposure(raw_sections)
        if exposure > 0:
            return exposure

    return 0


EXPOSURE_KEYWORDS = {
    "intern": 0.25,
    "internship": 0.25,
    "trainee": 0.25,
    "apprentice": 0.3,
    "virtual experience": 0.15,
    "forage": 0.15,
    "project": 0.2,
    "freelance": 0.4,
    "self employed": 0.4,
}
def _infer_exposure(raw_sections):
    if not isinstance(raw_sections, list):
        return 0

    text = " ".join(raw_sections).lower()

    score = 0
    for keyword, value in EXPOSURE_KEYWORDS.items():
        if keyword in text:
            score = max(score, value)

    return score
