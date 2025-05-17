from docx import Document
import os


def handle_docx(filename):
    input_path = os.path.join("storage/temp_files", filename)
    output_path = os.path.join("storage/processed", filename.replace(".docx", ".txt"))

    doc = Document(input_path)
    text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return text