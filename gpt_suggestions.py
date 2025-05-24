import openai
import os

client = openai.OpenAI(api_key=os.getenv(""))  # Or hardcode your key if testing

def get_resume_suggestions(resume_text, missing_keywords):
    prompt = f"""
You are an expert resume reviewer. Analyze the following resume and suggest improvements.

Resume Text:
{resume_text}

Missing Keywords (based on job description):
{', '.join(missing_keywords)}

Please suggest 3–5 specific bullet points the candidate can add or improve to match the job description better.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating suggestions:\n{e}"

