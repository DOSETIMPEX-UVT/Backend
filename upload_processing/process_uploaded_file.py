import sys, os
from process_docx import handle_docx
from clean_text import clean_text
from vectorize_text import vectorize_text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def process_file(filename):
    ext = os.path.splitext(filename)[-1].lower()
    os.makedirs("storage/processed", exist_ok=True)

    # 1. Extrage textul brut
    if ext != ".docx":
        raise Exception("Se acceptă doar fișiere .docx.")
    raw_text = handle_docx(filename)

    # 2. Curăță textul
    cleaned_text = clean_text(raw_text)

    # 3. Salvează textul curățat în .txt
    base_name = os.path.splitext(filename)[0].lower()
    out_path = os.path.join("storage/processed", f"{base_name}.txt")
    with open(out_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(cleaned_text)

    # 4. Vectorizează textul
    vectorize_text(cleaned_text, filename)

    return cleaned_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Foloseste: python process_uploaded_file.py nume_fisier")
        sys.exit(1)

    result = process_file(sys.argv[1])
    print("Text procesat:", result[:300])
