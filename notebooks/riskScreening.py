def calculate_risk(age, bmi, family_history, symptoms_count, language="en"):
    risk_score = 0

    if age >= 45:
        risk_score += 1

    if bmi >= 25:
        risk_score += 1

    fam_clean = str(family_history).strip().lower()
    if fam_clean in ["yes", "parent", "sibling"]:
        risk_score += 1

    if symptoms_count >= 2:
        risk_score += 2
    
    lang_clean = str(language).strip().lower()
    
    if lang_clean in ["id", "indonesian"]:
        # Indonesian Output Translations
        if risk_score <= 1:
            return "Risiko Rendah"
        elif risk_score == 2:
            return "Risiko Sedang"
        else:
            return "Risiko Tinggi (silakan lakukan tes glukosa)"
    else:
        # English Output Configuration (Default Fallback)
        if risk_score <= 1:
            return "Low Risk"
        elif risk_score == 2:
            return "Moderate Risk"
        else:
            return "High Risk (please take a glucose test)"