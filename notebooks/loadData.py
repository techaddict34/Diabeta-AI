import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Prepare the guidelines in a variable and make a variable to store the processed chunks after splitting
raw_dir = "data/guidelines/"
out_dir = "data/processed_texts/"

# Define function to split long texts into chunks
def extract_n_chunks():
    txt_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 900,
        chunk_overlap = 200,
        separators = ["\n\n", "\n", ".", " ", ""]
    )

# Make sure that the variable for storing the chunks exists
    os.makedirs(out_dir, exist_ok=True)
    for file in os.listdir(raw_dir):
        if file.endswith(".pdf"): # If file is in format pdf
            pdf_path = os.path.join(raw_dir, file) # Gather all the file(s)' paths from raw_dir and join all of them into one path
            loader = PyPDFLoader(pdf_path) # Make a loader for your composite pdf path
            docs = loader.load() # Load them to a variable (docs)

            chunks = txt_splitter.split_documents(docs) # Split the loaded documents into smaller chunks for processing
            for a, chunk in enumerate(chunks):
                chunk_file = os.path.join(out_dir, f"{file}_{a}.txt") # Join all chunk files and put them into out_dir (folder path) and define all of this as variable chunk_file
                with open(chunk_file, "w", encoding="utf-8") as f: # Open chunk_file to write all the chunk content in the encoding format of utf-8
                    f.write(chunk.page_content)

if __name__ == "__main__": # Only run extract_n_chunks() when this file is executed directly
    extract_n_chunks()