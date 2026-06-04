import os
from dotenv import load_dotenv

if not os.path.exists("vector_db"):
    print("--- vector_db not found, building data pipeline ---")
    os.system("python notebooks/loadData.py")
    os.system("python notebooks/vectorEmbed.py")
    print("--- data pipeline complete ---")

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel

from notebooks.ragQuery import ask_question
from notebooks.riskScreening import calculate_risk

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

# enable CORS (important for Frontend Integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# define data models
class ChatQuery(BaseModel):
    question: str
    language: str = "en"

class RiskInput(BaseModel):
    age: int
    bmi: float
    family_history: str
    symptoms_count: int
    language: str = "en"

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.post("/chat")
def chat(data: ChatQuery):
    try:
        # force name mapping declaration down the data channel
        answer, raw_sources = ask_question(q=data.question, lang=data.language)
        
        clean_sources = []
        for src in raw_sources:
            full_source = src.metadata.get("source", "Unknown")
            filename = os.path.basename(full_source)
            clean_pdf_name = filename.split(".pdf")[0] + ".pdf"
            
            display_title_map = {
                "guideline_1.pdf": "PERKENI (Perkumpulan Endokrinologi Indonesia) Guidelines",
                "guideline_2.pdf": "KMK Kemenkes RI (Pedoman Nasional Pelayanan Kedokteran)"
            }
            final_title = display_title_map.get(clean_pdf_name, clean_pdf_name)
            file_url = f"http://127.0.0.1:8000/static/{clean_pdf_name}"

            clean_sources.append({
                "title": final_title,
                "page": src.metadata.get("page", "N/A"),
                "snippet": src.page_content[:200] + "...",
                "url": file_url 
            })

        return {
            "answer": answer,
            "citations": clean_sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/screen")
def screen(data: RiskInput):
    try:
        result = calculate_risk(
            age=data.age,
            bmi=data.bmi,
            family_history=data.family_history,
            symptoms_count=data.symptoms_count,
            language=data.language
        )
        return {"risk": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))