# gpt_feedback.py
import openai

def get_feedback(resume_text, jd_text, api_key):
    """
    Returns career feedback from GPT given a resume and job description.
    """
    openai.api_key = api_key  # use key passed from Streamlit

    prompt = f"""
    You are a career coach AI.
    Given this resume and job description, suggest improvements:
    - Fix grammar/style issues
    - Suggest 3 stronger bullet points tailored to the JD
    - Highlight missing skills briefly

    Resume:
    {resume_text[:2000]}  # limit to avoid token overflow

    Job Description:
    {jd_text[:1500]}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response["choices"][0]["message"]["content"]
