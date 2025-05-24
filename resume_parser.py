import PyPDF2
import docx2txt

def extract_text_from_resume(file):
    if file.name.endswith('.pdf'):
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    elif file.name.endswith('.docx'):
        return docx2txt.process(file)
    else:
        return ""
