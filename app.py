import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from resume_parser import extract_text
from skills import find_skills
from ai_engine import get_ai_feedback
from resume_score import section_score
from section_checker import (
    check_sections,
    get_recommendations,
    check_links
)

# ---------------- AI FEEDBACK ----------------
def ai_feedback(missing_skills, score):

    feedback = []

    if score < 50:
        feedback.append(
            "⚠️ Your ATS score is low. Add more relevant skills and projects."
        )

    elif score < 80:
        feedback.append(
            "👍 Good resume, but can be improved with more relevant skills."
        )

    else:
        feedback.append(
            "🔥 Excellent resume! You are job-ready."
        )

    if missing_skills:

        feedback.append(
            "📌 Focus on learning these skills:"
        )

        for skill in missing_skills:
            feedback.append(f"👉 {skill}")

    return feedback


# ---------------- PDF FUNCTION ----------------
def generate_pdf(score, ats_score, skills, missing_skills):

    file_name = "resume_report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Resume Score: {score}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"ATS Score: {ats_score}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Skills Found:",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            ", ".join(skills) if skills else "None",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Missing Skills:",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            ", ".join(missing_skills)
            if missing_skills else "None",
            styles["Normal"]
        )
    )

    doc.build(content)

    return file_name


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;color:#4CAF50;'>
🤖 AI Resume Analyzer
</h1>

<p style='text-align:center;color:gray;'>
Upload your resume and get AI-powered ATS insights
</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Dashboard")
st.sidebar.success("AI Resume Analyzer")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

st.sidebar.markdown("---")
st.sidebar.info("Built with Streamlit + Python 🚀")

# ---------------- MAIN APP ----------------
if uploaded_file:

    text = extract_text(uploaded_file)

    skills = find_skills(text)

    sections = check_sections(text)

    links = check_links(text)

    recommendations = get_recommendations(sections)

    overall_resume_score = section_score(sections)

    # ---------------- TOP SECTION ----------------

    col1, col2 = st.columns([1, 2])

    with col1:

        st.subheader("📄 Resume Content")

        st.text_area(
            "Resume",
            text,
            height=300,
            key="resume_text"
        )

    with col2:

        st.subheader("🧠 Skills Analysis")

        if skills:

            st.success("Skills Found")

            st.write(", ".join(skills))

        else:

            st.warning("No skills found")

        score = min(len(skills) * 10, 100)

        st.subheader("📊 Resume Score")

        st.progress(score / 100)

        st.metric(
            "Resume Score",
            f"{score}%"
        )

        # OVERALL QUALITY SCORE

        st.subheader("🏆 Overall Resume Quality")

        st.progress(overall_resume_score / 100)

        st.metric(
            "Resume Quality",
            f"{overall_resume_score}%"
        )

    st.markdown("---")
  

   

    # ---------------- CHECKLIST ----------------

    st.subheader("📋 Resume Checklist")

    for section, present in sections.items():

        if present:
            st.success(f"✅ {section} Found")
        else:
            st.error(f"❌ {section} Missing")

    st.markdown("---")

    # ---------------- IMPROVEMENTS ----------------

    st.subheader("💡 Resume Improvement Suggestions")

    if recommendations:

        for rec in recommendations:
            st.warning(rec)

    else:

        st.success(
            "🎉 Great! Your resume contains all major sections."
        )

    st.markdown("---")

    # ---------------- PROFILE LINKS ----------------

    st.subheader("🌐 Professional Profile Check")

    for name, found in links.items():

        if found:
            st.success(f"✅ {name} Link Found")

        else:
            st.error(f"❌ {name} Link Missing")

    st.markdown("---")

    # ---------------- JOB DESCRIPTION ----------------

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description Here",
        key="job_desc"
    )

    if job_description:

        job_skills = find_skills(job_description)

        matched_skills = set(skills).intersection(
            set(job_skills)
        )

        missing_skills = set(job_skills) - set(skills)

        ats_score = int(
            len(matched_skills) / len(job_skills) * 100
        ) if job_skills else 0

        # ---------------- GPT REVIEW ----------------

        with st.spinner(
            "Analyzing resume with AI..."
        ):

            ai_result = get_ai_feedback(
                text,
                job_description
            )

        st.subheader("🤖 GPT Resume Review")

        st.write(ai_result)

        st.markdown("---")

        # ---------------- FEEDBACK ----------------

        st.subheader("🤖 AI Feedback")

        feedback = ai_feedback(
            missing_skills,
            ats_score
        )

        for line in feedback:
            st.write(line)

        st.markdown("---")

        # ---------------- METRICS ----------------
        overall_score = int(
    (score + ats_score + overall_resume_score) / 3
)

        col3, col4, col5, col6 = st.columns(4)

        with col3:
           st.metric(
        "Resume Score",
        f"{score}%"
    )

        with col4:
          st.metric(
        "ATS Match",
        f"{ats_score}%"
    )

        with col5:
           st.metric(
        "Skills Found",
        len(skills)
    )

        with col6:
         st.metric(
        "Overall Score",
        f"{overall_score}%"
    ) 
        st.markdown("---")
        st.subheader("🏆 Overall Resume Quality")

        st.progress(overall_score / 100)

        st.metric(
    "Overall Resume Score",
    f"{overall_score}%"
)
        
        st.markdown("---")
        st.markdown("---")

        st.subheader("⭐ Resume Rating")

        if overall_score >= 90:
         st.success("⭐⭐⭐⭐⭐ Outstanding")

        elif overall_score >= 80:
         st.success("⭐⭐⭐⭐ Very Good")

        elif overall_score >= 70:
          st.info("⭐⭐⭐ Good")

        elif overall_score >= 60:
          st.warning("⭐⭐ Average")

        else:
         st.error("⭐ Needs Improvement")

        st.markdown("---")

        st.subheader("💪 Resume Strengths")

        if len(skills) >= 5:
          st.success("Strong technical skill set")

        if ats_score >= 70:
          st.success("Good ATS compatibility")

        if overall_resume_score >= 80:
         st.success("Well-structured resume")

        if overall_score >= 80:
          st.success("Excellent overall resume quality")
        st.markdown("---")

        st.subheader("⚠️ Areas to Improve")

        if ats_score < 60:
          st.warning("Add more skills matching the job description")

        if overall_resume_score < 80:
          st.warning("Improve missing resume sections")

        if len(skills) < 5:
          st.warning("Add more technical skills to your resume")

        st.markdown("---")


        # ---------------- ATS SCORE ----------------

        st.subheader("🎯 ATS Match Score")

        st.progress(ats_score / 100)

        st.write(f"{ats_score}%")

        # ---------------- MATCHED SKILLS ----------------

        st.subheader("✅ Matched Skills")

        if matched_skills:

            for skill in matched_skills:
                st.write("✅", skill)

        else:

            st.write("No matching skills found")

        # ---------------- MISSING SKILLS ----------------

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                st.write("❌", skill)

        else:

            st.write("No missing skills found")

        st.markdown("---")

        # ---------------- AI SUGGESTIONS ----------------

        st.subheader("💡 AI Suggestions")

        if missing_skills:

            for skill in missing_skills:
                st.write(
                    f"👉 Learn {skill} to improve ATS score"
                )

        else:

            st.success(
                "Your resume matches all required skills 🎉"
            )

        st.markdown("---")

        # ---------------- PDF DOWNLOAD ----------------

        if st.button("📥 Generate PDF Report"):

            file_path = generate_pdf(
                score,
                ats_score,
                list(skills),
                list(missing_skills)
            )

            with open(file_path, "rb") as f:

                st.download_button(
                    "Download PDF Report",
                    data=f,
                    file_name="AI_Resume_Report.pdf",
                    mime="application/pdf"
                )