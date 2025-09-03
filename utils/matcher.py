from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare(resume_text, jd_keywords):
    resume_text = resume_text.lower()
    jd_text = " ".join(jd_keywords)

    vectorizer = CountVectorizer().fit([resume_text, jd_text])
    vectors = vectorizer.transform([resume_text, jd_text])
    sim = cosine_similarity(vectors[0], vectors[1])[0][0]

    # Missing keywords
    missing = [kw for kw in jd_keywords if kw not in resume_text]

    return round(sim * 100, 2), missing
