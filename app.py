import streamlit as st
import io
import re
from resume_parser import extract_text_from_resume
from job_parser import extract_keywords_from_jd
from analyzer import analyze_resume
from gpt_suggestions import get_resume_suggestions
from fpdf import FPDF

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# 💅 Style
st.markdown("""
    <style>
    .stApp { background-image: linear-gradient(135deg, #dbeafe, #ecfeff); }
    .title {
        color: #1d4ed8; font-weight: 800; font-size: 2.5rem;
        text-align: center; margin-bottom: 0.5rem;
    }
    .subtext {
        text-align: center; font-size: 1.1rem; color: #374151;
    }
    .box {
        background-color: #ffffff; border-radius: 12px; padding: 20px;
        margin-top: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .score-container {
        background: linear-gradient(to right, #4ade80, #22c55e);
        color: white; font-weight: bold; padding: 12px;
        border-radius: 8px; text-align: center; margin-bottom: 1rem;
    }
    .missing { color: #ef4444; font-weight: bold; }
    .matched { color: #16a34a; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📄 AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Upload your resume, paste a job description, and get GPT-powered insights!</div>", unsafe_allow_html=True)

st.markdown("### 🧾 Step 1: Upload & Paste")
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📎 Upload Resume", type=["pdf", "docx"])
with col2:
    job_description = st.text_area("📝 Paste Job Description", height=250)

if st.button("✨ Analyze Resume"):
    if resume_file is None or job_description.strip() == "":
        st.warning("⚠️ Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_resume(resume_file)
            jd_keywords = extract_keywords_from_jd(job_description)
            report = analyze_resume(resume_text, jd_keywords)

            # Fallback if GPT fails
            try:
                suggestions = get_resume_suggestions(resume_text, report['missing_keywords'])
            except Exception as e:
                suggestions = (
                    "• Add a project using AWS Lambda\n"
                    "• Mention React.js in tech stack\n"
                    "• Emphasize backend skills with Node.js and MongoDB"
                )

        # 📊 Display Results
        st.markdown("### 🎯 Match Results")
        st.markdown("<div class='box'>", unsafe_allow_html=True)

        st.markdown(f"<div class='score-container'>✅ Match Score: {report['score']}%</div>", unsafe_allow_html=True)
        st.progress(report['score'] / 100)

        st.markdown(f"<b>🧩 Missing Keywords:</b> <span class='missing'>{', '.join(report['missing_keywords']) or 'None 🎉'}</span>", unsafe_allow_html=True)
        st.markdown(f"<b>✅ Matched Keywords:</b> <span class='matched'>{', '.join(report['matched_keywords']) or 'None'}</span>", unsafe_allow_html=True)

        st.markdown(f"<br><b>📘 Summary:</b><br>{report['summary']}<br>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 🧠 GPT Suggestions
        st.markdown("### 🧠 AI-Powered Suggestions")
        st.markdown(f"<div class='box'>{suggestions}</div>", unsafe_allow_html=True)

        # 📝 Cleaned Report Text
        output_text = f"""
AI Resume Analysis Report

Match Score: {report['score']}%

Matched Keywords:
{', '.join(report['matched_keywords']) or 'None'}

Missing Keywords:
{', '.join(report['missing_keywords']) or 'None'}

Summary:
{report['summary']}

GPT Suggestions:
{suggestions}
"""

        txt_buffer = io.StringIO()
        txt_buffer.write(output_text)
        txt_buffer.seek(0)

        md_buffer = io.StringIO()
        md_buffer.write(output_text)
        md_buffer.seek(0)

        # Styled PDF Generator (clean emojis)
        def clean_text(text):
            return re.sub(r'[^\x00-\xFF]', '', text)

        class PDFReport(FPDF):
            def header(self):
                self.set_font("Arial", "B", 16)
                self.set_text_color(33, 37, 41)
                self.cell(0, 10, "AI Resume Analysis Report", ln=True, align='C')
                self.ln(10)

            def section_title(self, title):
                self.set_font("Arial", "B", 13)
                self.set_text_color(59, 130, 246)
                self.cell(0, 10, title, ln=True)
                self.ln(2)

            def section_body(self, text):
                self.set_font("Arial", "", 11)
                self.set_text_color(55, 65, 81)
                self.multi_cell(0, 8, clean_text(text))
                self.ln()

        pdf = PDFReport()
        pdf.add_page()
        pdf.section_title("Match Score")
        pdf.section_body(f"{report['score']}%")
        pdf.section_title("Matched Keywords")
        pdf.section_body(', '.join(report['matched_keywords']) or "None")
        pdf.section_title("Missing Keywords")
        pdf.section_body(', '.join(report['missing_keywords']) or "None")
        pdf.section_title("Summary")
        pdf.section_body(report['summary'])
        pdf.section_title("GPT Suggestions")
        pdf.section_body(suggestions)

        pdf_data = pdf.output(dest='S').encode('latin-1')
        pdf_buffer = io.BytesIO(pdf_data)

        # Download buttons
        st.markdown("### 📥 Download Your Report")
        st.download_button("📄 Download as TXT", data=txt_buffer.getvalue(), file_name="resume_analysis.txt", mime="text/plain")
        st.download_button("📝 Download as Markdown", data=md_buffer.getvalue(), file_name="resume_analysis.md", mime="text/markdown")
        st.download_button("📘 Download as Styled PDF", data=pdf_buffer, file_name="resume_analysis.pdf", mime="application/pdf")
