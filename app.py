import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from resume_parser import extract_text
from skills import find_skills

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("🤖 AI Resume Analyzer")

st.sidebar.title("📊 Dashboard")
st.sidebar.success("AI-powered Resume Analyzer")
st.sidebar.write("✔ Upload Resume")
st.sidebar.write("✔ Skill Detection")
st.sidebar.write("✔ ATS Score")
st.sidebar.write("✔ PDF Report")

uploaded_file = st.sidebar.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)

# ---------------- PDF FUNCTION ----------------
def generate_pdf(score, ats_score, skills, missing_skills):
    file_name = "resume_report.pdf"
    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("AI Resume Analysis Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Resume Score: {score}%", styles["Normal"]))
    content.append(Paragraph(f"ATS Score: {ats_score}%", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Skills Found:", styles["Heading2"]))
    content.append(Paragraph(", ".join(skills) if skills else "None", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Missing Skills:", styles["Heading2"]))
    content.append(Paragraph(", ".join(missing_skills) if missing_skills else "None", styles["Normal"]))

    doc.build(content)
    return file_name

# ---------------------------------------------

if uploaded_file:

    text = extract_text(uploaded_file)

    st.success("Resume Uploaded Successfully! 🎉")

    st.subheader("📄 Resume Content")
    st.write(text)

    skills = find_skills(text)

    st.subheader("🧠 Skills Found")

    if skills:
        for skill in skills:
            st.write("✅", skill)
    else:
        st.write("No skills found.")

    st.markdown("---")

    # Resume Score
    score = min(len(skills) * 10, 100)

    st.subheader("📊 Resume Score")
    st.progress(score / 100)
    st.write(f"{score}/100")

    st.markdown("---")

    # Job Description
    st.subheader("💼 Job Description")

    job_description = st.text_area("Paste Job Description Here")

    if job_description:

        job_skills = find_skills(job_description)

        matched_skills = set(skills).intersection(set(job_skills))
        missing_skills = set(job_skills) - set(skills)

        ats_score = 0
        if len(job_skills) > 0:
            ats_score = int(len(matched_skills) / len(job_skills) * 100)

        st.subheader("🎯 ATS Match Score")
        st.progress(ats_score / 100)
        st.write(f"{ats_score}%")

        st.markdown("---")

        st.subheader("📌 Analysis Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Resume Score", f"{score}%")

        with col2:
            st.metric("ATS Match", f"{ats_score}%")

        with col3:
            st.metric("Skills Found", len(skills))

        st.markdown("---")

        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write("✔", skill)
        else:
            st.write("No matching skills found.")

        st.subheader("❌ Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write("❌", skill)
        else:
            st.write("No missing skills found!")

        st.markdown("---")

        st.subheader("💡 AI Suggestions")

        if missing_skills:
            for skill in missing_skills:
                st.write(f"👉 Learn {skill} to improve ATS score")
        else:
            st.write("Your resume matches all required skills 🎉")

        st.markdown("---")

        # -------- DOWNLOAD BUTTON --------
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
                    f,
                    file_name="AI_Resume_Report.pdf"
                )