# gpt_feedback.py
import openai
import streamlit as st

def get_feedback(resume_text, jd_text,api_key):
    """
    Generates feedback on a resume based on a job description.
    Works with OpenAI Python library >=1.0 and Streamlit secrets.
    """

    # Safely get API key from Streamlit secrets
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found! Add it to secrets.toml or Streamlit Cloud secrets.")
        return "API key missing."

    openai.api_key = api_key

    # Construct the prompt
    system_prompt = "You are an expert career coach. Provide concise, actionable feedback on resumes."
    user_prompt = f"Resume:\n{resume_text}\n\nJob Description:\n{jd_text}\n\nGive feedback on how well this resume matches the job description and suggestions to improve."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # You can switch to gpt-3.5-turbo if preferred
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=15
        )

        # Extract the assistant's reply
        feedback = response.choices[0].message.content
        return feedback

    except Exception as e:
        st.error(f"Error generating feedback: {e}")
        return None
