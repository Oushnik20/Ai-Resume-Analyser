def analyze_resume(resume_text, jd_keywords):
    resume_text = resume_text.lower()

    matched_keywords = []
    missing_keywords = []

    for keyword in jd_keywords:
        if keyword in resume_text:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    score = int((len(matched_keywords) / len(jd_keywords)) * 100) if jd_keywords else 0

    summary = f"Your resume matches {len(matched_keywords)} out of {len(jd_keywords)} job-specific keywords."

    return {
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "score": score,
        "summary": summary
    }
