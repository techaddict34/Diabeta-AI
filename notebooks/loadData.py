import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_dir = os.path.join(base_dir, "data", "guidelines")
out_dir = os.path.join(base_dir, "data", "processed_texts")

# What steps this code file covers:
# 1) Load Data
# 2) Extract Sentences
# 3) Then Turn Them into Chunks

# Define function to split long texts into chunks
def extract_n_chunks():
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"CRITICAL ERROR: Source directory not found at {raw_dir}")
    
    txt_splitter = RecursiveCharacterTextSplitter(
        # size (900) and overlap (200) so that the chunks hold meaningful 
        # context, and doesn't let the sentences get bluntly chopped
        chunk_size = 900,        
        chunk_overlap = 200, 
        separators = ["\n\n", "\n", ".", " ", ""]
    )

    # Make sure that the variable for storing the chunks exists
    os.makedirs(out_dir, exist_ok=True)
    for file in os.listdir(raw_dir):
        if file.endswith(".pdf"): 
            pdf_path = os.path.join(raw_dir, file) 
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            chunks = txt_splitter.split_documents(docs)
            for a, chunk in enumerate(chunks):
                chunk_file = os.path.join(out_dir, f"{file}_{a}.txt") 
                # Encode to format of utf-8
                with open(chunk_file, "w", encoding="utf-8") as f: 
                    f.write(chunk.page_content)

if __name__ == "__main__": 
    extract_n_chunks()