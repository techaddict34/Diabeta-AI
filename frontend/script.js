// Global State Tracking for Language
let currentLang = "en";

// Translation Dictionaries for Instant UI Swapping
const uiTranslations = {
    en: {
        lblLanguage: "🌐 Language:",
        mainHeader: "🏥 Diabetes AI Assistant",
        gptHeader: "🚀 Try Diabeta AI (Advanced)",
        gptSub: "Access our specialized Custom GPT directly on the ChatGPT platform for advanced analysis.",
        ragHeader: "💬 Ask the Guidelines",
        ragSub: "Get answers from diabetes management guidelines using our AI-powered system.",
        placeholder: "e.g., What is the BMI cutoff for Asian populations?",
        btnText: "Ask Our RAG",
        thinking: "Thinking...",
        answerLabel: "Answer:",
        sourcesHeader: "📚 Sources:",
        alertText: "Please type a question!",
        riskHeader: "⚠️ Risk Screening Calculator",
        riskSub: "Calculate your diabetes risk based on key health factors.",
        lblAge: "Age",
        lblBmi: "BMI",
        lblFamily: "Family History",
        optNo: "No History",
        optYes: "Yes (Parents/Siblings)",
        lblSymptoms: "Symptoms Count",
        btnRisk: "Calculate Risk",
        riskLabel: "Risk Level:"
    },
    id: {
        lblLanguage: "🌐 Bahasa:",
        mainHeader: "🏥 Asisten AI Diabetes",
        gptHeader: "🚀 Coba Diabeta AI (Lanjutan)",
        gptSub: "Akses Custom GPT khusus kami langsung di platform ChatGPT untuk analisis tingkat lanjut.",
        ragHeader: "💬 Tanya Pedoman Medis",
        ragSub: "Dapatkan jawaban dari pedoman manajemen diabetes menggunakan sistem bertenaga AI kami.",
        placeholder: "misal, Berapa batas ambang BMI untuk populasi Asia?",
        btnText: "Tanya RAG Kami",
        thinking: "Sedang Berpikir...",
        answerLabel: "Jawaban:",
        sourcesHeader: "📚 Sumber Acuan:",
        alertText: "Silakan ketik pertanyaan Anda!",
        riskHeader: "⚠️ Kalkulator Skrining Risiko",
        riskSub: "Hitung risiko diabetes Anda berdasarkan faktor-faktor kesehatan utama.",
        lblAge: "Usia",
        lblBmi: "BMI (Indeks Massa Tubuh)",
        lblFamily: "Riwayat Keluarga",
        optNo: "Tidak Ada Riwayat",
        optYes: "Ada (Orang Tua/Saudara Kandung)",
        lblSymptoms: "Jumlah Gejala yang Dirasakan",
        btnRisk: "Hitung Risiko",
        riskLabel: "Tingkat Risiko:"
    }
};

// Check Backend Server Connection Status
async function checkStatus() {
    const statusDiv = document.getElementById("status");
    try {
        const res = await fetch("http://127.0.0.1:8000/");
        if (res.ok) {
            statusDiv.innerText = "Server Status: Online";
            statusDiv.className = "online";
        } else {
            statusDiv.innerText = "Server Status: Offline";
            statusDiv.className = "offline";
        }
    } catch {
        statusDiv.innerText = "Server Status: Error Connecting";
        statusDiv.className = "offline";
    }
}

// Function to handle instant UI text translation
function switchUILanguage() {
    currentLang = document.getElementById("langToggle").value;
    const t = uiTranslations[currentLang];
    
    // 🌟 Instantly swaps "🌐 Language:" to "🌐 Bahasa:"
    document.getElementById("lblLanguage").innerText = t.lblLanguage;
    
    // Update Layout Text Elements dynamically
    document.getElementById("mainHeader").innerText = t.mainHeader;
    document.getElementById("gptHeader").innerText = t.gptHeader;
    document.getElementById("gptSub").innerText = t.gptSub;
    document.getElementById("ragHeader").innerText = t.ragHeader;
    document.getElementById("ragSub").innerText = t.ragSub;
    document.getElementById("question").placeholder = t.placeholder;
    document.getElementById("askBtn").innerText = t.btnText;
    document.getElementById("answerLabel").innerText = t.answerLabel;
    
    document.getElementById("riskHeader").innerText = t.riskHeader;
    document.getElementById("riskSub").innerText = t.riskSub;
    document.getElementById("lblAge").innerText = t.lblAge;
    document.getElementById("bmi").placeholder = currentLang === "id" ? "misal, 24.5" : "e.g. 24.5";
    document.getElementById("age").placeholder = currentLang === "id" ? "misal, 45" : "e.g. 45";
    document.getElementById("symptoms").placeholder = currentLang === "id" ? "misal, 2" : "e.g. 2";
    document.getElementById("lblBmi").innerText = t.lblBmi;
    document.getElementById("lblFamily").innerText = t.lblFamily;
    document.getElementById("optNo").innerText = t.optNo;
    document.getElementById("optYes").innerText = t.optYes;
    document.getElementById("lblSymptoms").innerText = t.lblSymptoms;
    document.getElementById("btnRisk").innerText = t.btnRisk; 
    document.getElementById("riskLabel").innerText = t.riskLabel;
}

// Chatbot Logic
async function askBackend() {
    const question = document.getElementById("question").value;
    const btn = document.getElementById("askBtn");
    const resultArea = document.getElementById("chatResult");
    
    if (!question) return alert(uiTranslations[currentLang].alertText);

    btn.disabled = true;
    btn.innerText = uiTranslations[currentLang].thinking;
    resultArea.style.display = "none";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                question: question,
                language: currentLang // Pass active language code down to FastAPI
            })
        });

        const data = await response.json();

        // Scrub out formatting asterisks from the text before sending it to the screen
        const cleanAnswer = data.answer.replace(/\*\*/g, "").replace(/\*/g, "");
        document.getElementById("answerText").innerText = cleanAnswer;
        
        // Citations Output Generator
        const citationsArea = document.getElementById("citationsArea");
        if (data.citations && data.citations.length > 0) {
            let html = `<h4 style='margin-top: 20px; color: #1e293b;'>${uiTranslations[currentLang].sourcesHeader}</h4>`;
            
            data.citations.forEach(cit => {
                html += `
                    <div class="citation" style="margin-bottom: 12px; padding: 12px; background-color: #eff6ff; border-left: 4px solid #2563eb; border-radius: 6px; text-align: left;">
                        <a href="${cit.url}" target="_blank" style="color: #2563eb; font-weight: bold; text-decoration: underline; display: inline-block; margin-bottom: 4px;">
                            📂 ${cit.title}
                        </a> 
                        <span style="color: #64748b; font-size: 0.85em; font-weight: 500;">(p. ${cit.page})</span>
                        <br>
                        <em style="color: #475569; display: block; margin-top: 4px; font-size: 0.95rem; line-height: 1.4;">
                            "${cit.snippet}"
                        </em>
                    </div>
                `;
            });
            citationsArea.innerHTML = html;
        } else {
            citationsArea.innerHTML = "";
        }
        
        resultArea.style.display = "block";

    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        btn.disabled = false;
        btn.innerText = uiTranslations[currentLang].btnText;
    }
}

// Risk Calculator Client-Side Logic
function calculateRisk() {
    const age = parseInt(document.getElementById("age").value);
    const bmi = parseFloat(document.getElementById("bmi").value);
    const family = document.getElementById("family").value;
    const symptoms = parseInt(document.getElementById("symptoms").value);

    if (isNaN(age) || isNaN(bmi) || isNaN(symptoms)) {
        return alert(currentLang === "id" ? "Silakan isi semua bidang data!" : "Please fill in all fields!");
    }

    let points = 0;

    // Age Evaluation
    if (age >= 45) points += 2;
    else if (age >= 35) points += 1;

    // BMI Evaluation (Asian population target cut-offs)
    if (bmi >= 25) points += 2;
    else if (bmi >= 23) points += 1;

    // Family Profile Evaluation
    if (family === "yes") points += 2;

    // Symptom Profile Evaluation
    if (symptoms >= 2) points += 2;
    else if (symptoms === 1) points += 1;

    // Risk Classification Mapping Matrix
    let risk = "";
    let color = "";

    if (points >= 5) {
        risk = currentLang === "id" ? "Tinggi 🚨 (Silakan berkonsultasi dengan dokter)" : "High 🚨 (Please consult a doctor)";
        color = "#ef4444";
    } else if (points >= 3) {
        risk = currentLang === "id" ? "Sedang ⚠️ (Disarankan menjaga pola makan)" : "Moderate ⚠️ (Watch your lifestyle)";
        color = "#f59e0b";
    } else {
        risk = currentLang === "id" ? "Rendah ✅ (Pertahankan pola hidup sehat)" : "Low ✅ (Keep staying active)";
        color = "#10b981";
    }

    const resDiv = document.getElementById("riskResult");
    const valSpan = document.getElementById("riskValue");

    valSpan.innerText = risk;
    valSpan.style.color = color;
    resDiv.style.display = "block";
}

// Run Initial Validation Hooks on Application Start
window.onload = function() {
    checkStatus();        
    switchUILanguage();   
};