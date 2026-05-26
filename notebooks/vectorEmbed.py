import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


processed_dir = "data/processed_texts/" # Take all the chunks from processed_texts folder to do the embedding process

def build_vector_db():
    texts = [] # Make a list to collect all the chunked texts
    metadatas = []

    for file in os.listdir(processed_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(processed_dir, file)
        with open(file_path, "r", encoding="utf-8") as f: # Join all the files from processed_dir to read and gather them to list (texts)
            texts.append(f.read())
            metadatas.append({"source": file})

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") # Prepare the model for the embedding process
    database = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas) # FAISS (Facebook AI Similarity Search) all of the texts that have been embedded and store as variable database
    database.save_local("vector_db") # Store the FAISS vector database locally so future runs can load it quickly (vector_db is the folder that we will store the db locally in)

if __name__ == "__main__":
    build_vector_db()