import re

def clean_text(text):
    text = text.replace('\x0c', ' ')
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'(?i)pagina[:]?\s*\d+\s*/\s*\d+', '', text)
    text = re.sub(r'(?i)pagina\s+\d+\s*(din)?\s*\d*', '', text)
    text = re.sub(r'[\u2022\-\*\|\u203a\u00ab\u00bb]', ' ', text)
    text = re.sub(r'[\.]{3,}', '', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'__+', '', text)
    text = re.sub(r'[":{}()\[\]~]', '', text)
    return text.strip()
