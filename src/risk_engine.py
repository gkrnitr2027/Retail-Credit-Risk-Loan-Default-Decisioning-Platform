import joblib
import pandas as pd

# Load the trained pipeline
MODEL_PATH = "models/credit_risk_xgb_pipeline.pkl"
pipeline = joblib.load(MODEL_PATH)

# Production approximations for real-time feature engineering
GRADE_AVG_INT_RATE = {'A': 7.3, 'B': 11.0, 'C': 13.5, 'D': 16.0, 'E': 19.0, 'F': 21.0, 'G': 23.0}
INTENT_AVG_AMOUNT = {
    'PERSONAL': 12000, 'EDUCATION': 10000, 'MEDICAL': 8500, 
    'VENTURE': 15000, 'HOMEIMPROVEMENT': 14000, 'DEBTCONSOLIDATION': 16000
}

def evaluate_applicant(data: dict):
    """
    1. Calculates engineered features on-the-fly for real-time inference.
    2. Generates default probability using the XGBoost pipeline.
    3. Converts probability to a Credit Score (300-850) & Underwriting Decision.
    """
    # 1. Calculate loan_percent_income (Debt-to-Income / Loan-to-Income ratio)
    income = max(data['person_income'], 1.0) # Prevent division by zero
    loan_percent_income = data['loan_amnt'] / income
    data['loan_percent_income'] = round(loan_percent_income, 4)

    # 2. Calculate other engineered features
    calc_dti = data['loan_percent_income']
    is_high_burden = 1 if calc_dti > 0.35 else 0
    
    grade_avg = GRADE_AVG_INT_RATE.get(data['loan_grade'], 11.0)
    rate_spread = data['loan_int_rate'] - grade_avg
    
    intent_avg = INTENT_AVG_AMOUNT.get(data['loan_intent'], 12000)
    amt_deviation = data['loan_amnt'] - intent_avg
    
    # Add calculated features to the applicant payload
    data['calculated_dti'] = round(calc_dti, 4)
    data['is_high_debt_burden'] = is_high_burden
    data['int_rate_spread'] = round(rate_spread, 2)
    data['intent_amount_deviation'] = round(amt_deviation, 2)
    
    # 3. Predict using the Pipeline
    df_input = pd.DataFrame([data])
    proba_default = float(pipeline.predict_proba(df_input)[0, 1])

    # 4. Convert probability to credit score scale (300 to 850)
    credit_score = int(850 - (proba_default * 550))

    # 5. Business Rules for Automated Decisioning
    if proba_default >= 0.50:
        decision = "REJECT"
        risk_band = "High Risk"
    elif proba_default >= 0.25:
        decision = "MANUAL REVIEW"
        risk_band = "Medium Risk"
    else:
        decision = "AUTO APPROVE"
        risk_band = "Low Risk"

    return {
        "enriched_data": data,
        "default_probability": proba_default,
        "credit_score": credit_score,
        "decision": decision,
        "risk_band": risk_band
    }