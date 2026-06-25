def check_sections(text):

    text = text.lower()

    return {
        "Education": "education" in text,
        "Skills": "skills" in text,
        "Projects": "project" in text,
        "Experience": "experience" in text,
        "Certifications": "certification" in text
    }


def get_recommendations(sections):

    recommendations = []

    if not sections["Projects"]:
        recommendations.append("📌 Add 2-3 real projects with clear tech stack and outcomes.")

    if not sections["Experience"]:
        recommendations.append("📌 Add internship or real-world experience.")

    if not sections["Certifications"]:
        recommendations.append("📌 Add certifications (Python / AI / ML / Data Science).")

    if not sections["Skills"]:
        recommendations.append("📌 Add a dedicated Skills section in your resume.")

    return recommendations


def check_links(text):

    text = text.lower()

    return {
        "GitHub": "github.com" in text,
        "LinkedIn": "linkedin.com" in text
    }