import os
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_community.embeddings import FastEmbedEmbeddings
from dotenv import load_dotenv

# What step this codefile covers:
# 1) Get API Key
# 2) Load DB to do the "Nearest Neighbor" Search
# 3) Set Up LLM
# 4) Create Well Structured Prompt
# 5) Let the LLM Predict with the help of the Prompt

# Load env vars
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY not found. Please add it to your .env file.")

embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Absolute path targeting so it doesn't act blind
vector_db_path = os.path.join(base_dir, "vector_db")

if not os.path.exists("vector_db"):
    raise FileNotFoundError("The 'vector_db' folder was not found.")

# load db
database = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True)
retriever = database.as_retriever(search_kwargs={"k": 8})
# do the "nearest neighbor" search (k = 8)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key,
    temperature=0
)

def ask_question(q, lang="en"):
    try:
        docs = retriever.get_relevant_documents(q)
    except Exception:
        docs = []

    context = "\n\n".join([doc.page_content for doc in docs]) if docs else "No specific guideline text found."

    lang_clean = str(lang).strip().lower()

    if lang_clean in ["en", "english"]:
        # Eng prompt
        prompt = f"""You are a professional medical AI assistant specializing in Type 2 Diabetes management.
        You MUST respond in English only, regardless of the language of the context provided below.
        Answer the user's question clearly, comprehensively, and educationally.
        Use the official guideline text provided below as your primary reference:

        Context:
        {context}

        Question: {q}
        Answer in English:"""
    else:
        # Default fallback to the indo layout
        prompt = f"""Anda adalah asisten AI medis spesialis manajemen Diabetes Tipe 2 di Indonesia.
        Jawablah pertanyaan pengguna menggunakan Bahasa Indonesia yang baik, ramah, mudah dipahami oleh awam, dan edukatif.
        Gunakan konteks pedoman resmi di bawah ini sebagai acuan utama Anda:

        Konteks:
        {context}

        Pertanyaan: {q}
        Jawaban:"""

    response = llm.predict(prompt)
    return response, docs
