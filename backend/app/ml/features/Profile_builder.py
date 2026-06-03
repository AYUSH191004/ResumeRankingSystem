def build_resume_text(parsed: dict) -> str:
    """
    Convert structured parser output into natural language profile
    suitable for semantic embeddings.
    """

    lines = []

    # -------- Skills --------
    skills = parsed.get("skills", {})
    skill_list = skills.get("all_skills") or skills.get("skills") or []

    if isinstance(skill_list, list) and skill_list:
        lines.append(
            "Skills: " + ", ".join(skill_list)
        )

    # -------- Experience --------
    exp = parsed.get("experience", {})
    if exp.get("raw_sections"):
     lines.append("Work experience in software development")


    raw_sections = exp.get("raw_sections", [])
    if isinstance(raw_sections, list):
        for section in raw_sections[:3]:
            if isinstance(section, str) and len(section) > 20:
                lines.append(section)

    # -------- Education --------
    edu = parsed.get("education", {})
    degrees = edu.get("degrees", [])

    if isinstance(degrees, list):
        for d in degrees[:2]:
            lines.append(d)

    # -------- Projects / summary fallback --------
    for key in ["summary", "objective", "projects"]:
        val = parsed.get(key)
        if isinstance(val, str) and len(val) > 30:
            lines.append(val)

    # -------- Final fallback (last resort) --------
    if not lines:
        raw = parsed.get("raw_text")
        if raw and len(raw) > 50:
            return raw

        return "Resume information available but limited textual content."

    return "\n".join(lines)