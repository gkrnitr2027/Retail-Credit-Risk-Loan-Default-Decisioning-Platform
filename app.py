import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.risk_engine import evaluate_applicant

st.set_page_config(page_title="Retail Finance - Credit Underwriting", page_icon="🏦", layout="wide")

st.title("🏦 Retail Lending Credit Risk Engine")
st.markdown("Automated credit decisioning, risk banding, and inference platform.")
st.divider()

st.subheader("📝 New Loan Application")

with st.form("loan_application_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        person_age = st.number_input("Borrower Age", min_value=18, max_value=85, value=29)
        person_income = st.number_input("Annual Income (INR/USD)", min_value=1000.0, value=65000.0, step=1000.0)
        person_emp_length = st.number_input("Employment Length (Years)", min_value=0.0, max_value=50.0, value=4.0)

    with col2:
        person_home_ownership = st.selectbox("Home Ownership Status", ["RENT", "MORTGAGE", "OWN", "OTHER"])
        loan_intent = st.selectbox("Loan Intent", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"])
        loan_grade = st.selectbox("Credit Rating Grade (Internal)", ["A", "B", "C", "D", "E", "F", "G"])

    with col3:
        loan_amnt = st.number_input("Requested Loan Amount", min_value=500.0, value=12000.0, step=500.0)
        loan_int_rate = st.number_input("Offered Interest Rate (%)", min_value=1.0, max_value=35.0, value=11.25)
        cb_person_default_on_file = st.selectbox("Historical Default on Record?", ["N", "Y"])
        cb_person_cred_hist_length = st.number_input("Credit History Length (Years)", min_value=1, value=6)

    submit_btn = st.form_submit_button("⚡ Evaluate Credit Risk & Sanction Loan", use_container_width=True)

if submit_btn:
    applicant_payload = {
        "person_age": person_age,
        "person_income": person_income,
        "person_home_ownership": person_home_ownership,
        "person_emp_length": person_emp_length,
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "loan_amnt": loan_amnt,
        "loan_int_rate": loan_int_rate,
        "cb_person_default_on_file": cb_person_default_on_file,
        "cb_person_cred_hist_length": cb_person_cred_hist_length
    }

    with st.spinner("Processing application & scoring risk..."):
        eval_result = evaluate_applicant(applicant_payload)
    
    st.divider()
    st.subheader("🎯 Automated Underwriting Decision")

    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.metric(label="Calculated Credit Score", value=eval_result["credit_score"])
        if eval_result["decision"] == "AUTO APPROVE":
            st.success(f"**Decision: {eval_result['decision']}**")
        elif eval_result["decision"] == "MANUAL REVIEW":
            st.warning(f"**Decision: {eval_result['decision']}**")
        else:
            st.error(f"**Decision: {eval_result['decision']}**")

    with res_col2:
        prob = eval_result['default_probability'] * 100
        st.metric(label="Default Probability", value=f"{prob:.2f}%")
        st.caption(f"Assigned Risk Tier: **{eval_result['risk_band']}**")

    with res_col3:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=eval_result["credit_score"],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [300, 850]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [300, 580], 'color': "#FF4B4B"},
                    {'range': [580, 700], 'color': "#FFAA00"},
                    {'range': [700, 850], 'color': "#00CC96"}
                ]
            }
        ))
        fig_gauge.update_layout(height=200, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)