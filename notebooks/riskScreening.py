def calculate_risk(age, bmi, family_history, symptoms_count):
    risk_score = 0

    if age >= 45:
        risk_score += 1
    if bmi >= 25:
        risk_score += 1
    if family_history.lower() in ["parent", "sibling"]:
        risk_score += 1
    if symptoms_count >= 2:
        risk_score += 2
    
    if risk_score <= 1:
        return "Low Risk"
    elif risk_score == 2:
        return "Moderate Risk"
    else:
        return "High Risk — please take a glucose test"
