import PyPDF2
import docx

def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # skip None pages
                text += page_text + " "
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + " "
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file.type}")

    return text.strip()
