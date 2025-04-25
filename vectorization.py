from gensim.models.doc2vec import Doc2Vec,\
	TaggedDocument
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('punkt_tab') 
import os
# define a list of documents.
folder_path = os.path.join(os.getcwd(), 'Data', 'CleanedData')
output_folder = os.path.join(os.getcwd(), 'Data', 'VectorizedData')

data = []
file_names = []  
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data.append(file.read())  
        file_names.append(filename)  


# preproces the documents, and create TaggedDocuments
tagged_data = [TaggedDocument(words=word_tokenize(doc.lower()), tags=[str(i)]) for i, doc in enumerate(data)]

# train the Doc2vec model
model = Doc2Vec(vector_size=20, min_count=1, epochs=50)
model.build_vocab(tagged_data)
model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)

# get the document vectors
document_vectors = [model.infer_vector(word_tokenize(doc.lower())) for doc in data]

for i, doc in enumerate(data):
    vector = model.infer_vector(word_tokenize(doc.lower()))
    
    output_file_path = os.path.join(output_folder, file_names[i])
    
    # Save the vector in a .txt file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(' '.join(map(str, vector)))  # Salvează vectorul sub formă de string, valorile fiind separate prin spațiu

    print(f"Documentul '{file_names[i]}' a fost vectorizat și salvat în '{output_file_path}'.")
