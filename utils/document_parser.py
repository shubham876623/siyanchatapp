import fitz 
import docx

def parse_document(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == 'pdf':
        text = ""
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text
    elif file_type == 'docx':
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file_type == 'txt':
        return uploaded_file.read().decode("utf-8")
    else:
        return ""