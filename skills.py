skills_list = [
    "python",
    "java",
    "sql",
    "machine learning",
    "html",
    "css",
    "javascript",
    "pandas",
    "numpy"
]

def find_skills(text):
    found_skills = []

    text = text.lower()

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills

print("skills.py loaded")


