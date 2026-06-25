def check_sections(text):

    text = text.lower()

    sections = {
        "Contact": False,
        "Education": False,
        "Skills": False,
        "Projects": False,
        "Experience": False
    }

    if "email" in text or "@" in text:
        sections["Contact"] = True

    if "education" in text:
        sections["Education"] = True

    if "skill" in text:
        sections["Skills"] = True

    if "project" in text:
        sections["Projects"] = True

    if "experience" in text:
        sections["Experience"] = True

    return sections
def section_score(sections):

    score = 0

    score += 20 if sections.get("Education") else 0
    score += 20 if sections.get("Skills") else 0
    score += 20 if sections.get("Projects") else 0
    score += 20 if sections.get("Experience") else 0
    score += 20 if sections.get("Contact") else 0

    return score