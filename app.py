import streamlit as st
import openai

from utils import gpt_feedback, jd_parser, matcher, resume_parser

#openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI Career Helper", layout="wide")
st.title("💼 AI Career Helper")
st.write("Upload your resume and paste a job description to get instant feedback!")

# --- Persisted Resume Upload ---
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

resume_file = st.file_uploader("Upload your resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
if resume_file:
    try:
        st.session_state.resume_text = resume_parser.extract_text(resume_file)
        if st.session_state.resume_text:
            st.success("Resume uploaded successfully!")
        else:
            st.error("Could not extract text from the resume. Try another file.")
    except Exception as e:
        st.error(f"Error parsing resume: {e}")

# --- Persisted Job Description Input ---
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

st.session_state.jd_text = st.text_area("Paste Job Description here:", value=st.session_state.jd_text)

# --- Run Analysis ---
if st.button("Analyze"):
    if st.session_state.resume_text and st.session_state.jd_text:
        with st.spinner("Analyzing..."):
            try:
                # Parse JD
                jd_keywords = jd_parser.extract_keywords(st.session_state.jd_text)

                # Match skills
                match_score, missing_skills = matcher.compare(st.session_state.resume_text, jd_keywords)

                # GPT Feedback
                suggestions = gpt_feedback.get_feedback(
                    st.session_state.resume_text,
                    st.session_state.jd_text,
                    st.secrets["OPENAI_API_KEY"]
                )

                # --- Results ---
                st.subheader("📊 Match Analysis")
                st.write(f"**Match Score:** {match_score}%")
                st.write("**Missing Skills:**", ", ".join(missing_skills) if missing_skills else "None 🎉")

                st.subheader("🚀 GPT Suggestions")
                st.write(suggestions)

            except Exception as e:
                st.error(f"Error during analysis: {e}")
    else:
        st.error("Please upload a resume and paste a job description first!")
