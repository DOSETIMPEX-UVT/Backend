import faiss
import numpy as np
import os

folder_path = 'Data/VectorizedDataNormalized'

vectori = []
nume_fisiere = []

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)

        vector = np.loadtxt(file_path)
        vectori.append(vector)

        nume_fisiere.append(filename)

# Transformam lista în numpy array de float32 ptr ca FAISS accepta doar vectori de tip float32 ca să functioneze rapid
vectori = np.array(vectori).astype('float32')

print(f"Am găsit {len(vectori)} vectori.")

# Cream baza FAISS
dimensiune = vectori.shape[1]
index = faiss.IndexFlatL2(dimensiune)

index.add(vectori)

print("Vectori salvați")
