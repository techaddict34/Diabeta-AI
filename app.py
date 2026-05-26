from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import your logic
# Ensure python can find this. If 'notebooks' is a folder, this is correct.
from notebooks.ragQuery import ask_question
from notebooks.riskScreening import calculate_risk

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ENABLE CORS (Essential for Frontend Integration)
app.add_middleware(
    CORSMiddleware,
    # In production, replace ["*"] with your specific frontend domain (e.g., ["http://localhost:5500"])
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Data Models
class ChatQuery(BaseModel):
    question: str
    language: str = "en"

class RiskInput(BaseModel):
    age: int
    bmi: float
    family_history: str
    symptoms_count: int

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

# Refactored for Clean JSON
@app.post("/chat")
def chat(data: ChatQuery):
    try:
        # Call the function from ragQuery.py
        answer, raw_sources = ask_question(data.question, data.language)
        
        # Process sources to be "Frontend Friendly" and Clickable
        clean_sources = []
        for src in raw_sources:
            full_source = src.metadata.get("source", "Unknown")
            filename = os.path.basename(full_source)
            
            # Clean up the file extension (Turns "guideline_1.pdf_32.txt" into "guideline_1.pdf")
            clean_pdf_name = filename.split(".pdf")[0] + ".pdf"
            
            # Organization & Ministry Title Mapping
            display_title_map = {
                "guideline_1.pdf": "PERKENI (Perkumpulan Endokrinologi Indonesia) Guidelines",
                "guideline_2.pdf": "KMK Kemenkes RI (Pedoman Nasional Pelayanan Kedokteran)"
            }
            final_title = display_title_map.get(clean_pdf_name, clean_pdf_name)
            
            # Create the local web link pointing straight to the mounted static file folder
            file_url = f"http://127.0.0.1:8000/static/{clean_pdf_name}"

            # CRITICAL: Ensure all 4 of these keys match what script.js expects!
            clean_sources.append({
                "title": final_title,
                "page": src.metadata.get("page", "N/A"),
                "snippet": src.page_content[:200] + "...",
                "url": file_url  # 🌟 MAKE SURE THIS LINE EXISTS NATIVELY HERE!
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
            symptoms_count=data.symptoms_count
        )
        return {"risk": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))