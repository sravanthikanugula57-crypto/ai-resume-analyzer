import google.generativeai as genai

# ✅ USE GEMINI KEY (NOT OpenAI KEY)
genai.configure(api_key="AIzaSyByLLfSXwBzg4EbsMYIPBbm8DIKquWYYfA")

model = genai.GenerativeModel("models/gemini-2.5-flash")

def get_ai_feedback(resume_text, job_description):
    prompt = f"""
    Analyze this resume:

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Give:
    - ATS score
    - missing skills
    - improvement suggestions
    """

    response = model.generate_content(prompt)
    return response.text