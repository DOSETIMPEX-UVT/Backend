import os
import numpy as np
from sentence_transformers import SentenceTransformer

def vectorize_text(text, filename):
    os.makedirs("storage/vectors", exist_ok=True)
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    vector = model.encode(text).astype("float32")
    out_name = filename.replace(".pdf", ".txt").replace(".docx", ".txt")
    out_path = os.path.join("storage/vectors", out_name)
    np.savetxt(out_path, vector)
    print(f"Vector salvat pentru {filename}: {vector.shape}")