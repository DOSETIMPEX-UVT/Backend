import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Găsește calea absolută către rădăcina proiectului
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Load model o singură dată
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Încarcă vectorii FAISS
folder_path = os.path.join(BASE_DIR, "Data", "VectorizedDataNormalized")
vectori = []
nume_fisiere = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        vector = np.loadtxt(os.path.join(folder_path, filename))
        vectori.append(vector)
        nume_fisiere.append(filename)

vectori = np.array(vectori).astype("float32")
index = faiss.IndexFlatL2(vectori.shape[1])
index.add(vectori)

# Funcția care va fi apelată în router
async def generate_response_from_LLM(user_message: str) -> str:
    # Encodează întrebarea
    query_vector = model.encode([user_message]).astype("float32")

    # Caută cei mai apropiați 3 vectori
    D, I = index.search(query_vector, k=3)

    # Încearcă să extragi contextul din fișierele corespunzătoare
    context_parts = []
    for idx in I[0]:
        if idx < 0 or idx >= len(nume_fisiere):
            continue

        nume_fisier = nume_fisiere[idx]
        path_text = os.path.join(BASE_DIR, "Data", "CleanedData", nume_fisier.replace(".txt", ".txt"))

        try:
            with open(path_text, "r", encoding="utf-8") as f:
                text = f.read()
                context_parts.append(text)
        except FileNotFoundError:
            continue

    # Construiește contextul final
    if not context_parts:
        return "Am găsit vectori similari, dar nu am putut extrage contextul din fișierele originale."

    context = "\n".join(context_parts)

    # Returnează răspunsul cu context
    response = f"{context[:1000]}"
    return response

