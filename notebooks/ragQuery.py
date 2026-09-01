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
    model="openai/gpt-oss-120b",
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
        prompt = f"""You are a medical AI assistant for Type 2 Diabetes management.
        You MUST respond in English only.
        You MUST answer ONLY using the guideline text provided in the Context below.
        Do NOT use your own training knowledge, assumptions, or any information outside of the provided Context.
        If the Context does not contain enough information to answer the question, respond with exactly:
        "I'm sorry, I can't answer that based on the available guidelines."

        Context:
        {context}

        Question: {q}
        Answer in English:"""
    else:
        # Default fallback to the indo layout
        prompt = f"""Anda adalah asisten AI medis untuk manajemen Diabetes Tipe 2.
        Anda HARUS menjawab dalam Bahasa Indonesia.
        Anda HANYA boleh menjawab berdasarkan teks pedoman yang tersedia di bagian Konteks di bawah ini.
        JANGAN gunakan pengetahuan pelatihan Anda sendiri, asumsi, atau informasi apapun di luar Konteks yang diberikan.
        Jika Konteks tidak memiliki cukup informasi untuk menjawab pertanyaan, balas dengan tepat:
        "Maaf, saya tidak dapat menjawab pertanyaan tersebut berdasarkan pedoman yang tersedia."

        Konteks:
        {context}

        Pertanyaan: {q}
        Jawaban:"""

    response = llm.predict(prompt)
    return response, docs
