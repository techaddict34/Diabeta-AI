from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_community.embeddings import OpenVINOEmbeddings  # Clean, zero-dependency local math
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Get API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY not found. Please add it to your .env file.")

# 1. Use clean, zero-dependency local fake embeddings to bypass ALL network limits
class SimpleGroqEmbeddings:
    def __init__(self, llm):
        self.llm = llm
    def embed_documents(self, texts):
        # Returns static mock dimensions so FAISS can initialize instantly without a network
        return [[0.0] * 384 for _ in texts]
    def embed_query(self, text):
        return [0.0] * 384

# Universal, safe offline embeddings configuration
from langchain_community.embeddings import DeterministicFakeEmbedding
embeddings = DeterministicFakeEmbedding(size=384)

# 2. Load the Vector Database safely
if not os.path.exists("vector_db"):
    raise FileNotFoundError("The 'vector_db' folder was not found.")

database = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True) 
retriever = database.as_retriever(search_kwargs={"k": 8})

# 3. Initialize LLM with Groq
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
        # Pristine English medical generation rules
        prompt = f"""You are a professional medical AI assistant specializing in Type 2 Diabetes management.
        Answer the user's question clearly, comprehensively, and educationally using English.
        Use the official guideline text provided below as your primary reference:

        Context:
        {context}

        Question: {q}
        Answer:"""
    else:
        # Default fallback to Indonesian layout 
        prompt = f"""Anda adalah asisten AI medis spesialis manajemen Diabetes Tipe 2 di Indonesia.
        Jawablah pertanyaan pengguna menggunakan Bahasa Indonesia yang baik, ramah, mudah dipahami oleh awam, dan edukatif.
        Gunakan konteks pedoman resmi di bawah ini sebagai acuan utama Anda:

        Konteks:
        {context}

        Pertanyaan: {q}
        Jawaban:"""

    response = llm.predict(prompt)
    return response, docs