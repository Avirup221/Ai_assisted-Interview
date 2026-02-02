import os
from pypdf import PdfReader

def extract_text_from_resume(file_path):
    """
    Reads text from a PDF or TXT file path.
    """
    if not file_path or not os.path.exists(file_path):
        return None

    text = ""
    try:
        if file_path.lower().endswith('.pdf'):
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        else:
            # Assume text file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        print(f"Error reading resume: {e}")
        return None
        
    return text.strip()