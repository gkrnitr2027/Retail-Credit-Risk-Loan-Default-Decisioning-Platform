-- Create a View that Python can easily query
CREATE OR REPLACE VIEW vw_engineered_risk_features AS

WITH BorrowerRiskProfiles AS (
    SELECT 
        application_id,
        person_age,
        person_income,
        person_home_ownership,
        person_emp_length,
        loan_intent,
        loan_grade,
        loan_amnt,
        loan_int_rate,
        loan_percent_income,
        cb_person_default_on_file,
        cb_person_cred_hist_length,
        loan_status,
        -- Feature 1: Debt-to-Income / Burden Ratio
        ROUND(loan_amnt / NULLIF(person_income, 0), 4) AS calculated_dti,
        -- Feature 2: Window Function - Grade-Level Average Interest Rate
        AVG(loan_int_rate) OVER(PARTITION BY loan_grade) AS avg_grade_int_rate,
        -- Feature 3: Window Function - Relative Loan Size vs Intent Group
        AVG(loan_amnt) OVER(PARTITION BY loan_intent) AS avg_intent_loan_amount
    FROM loan_applications
)
SELECT 
    application_id,
    person_age,
    person_income,
    person_home_ownership,
    person_emp_length,
    loan_intent,
    loan_grade,
    loan_amnt,
    loan_int_rate,
    loan_percent_income,
    cb_person_default_on_file,
    cb_person_cred_hist_length,
    calculated_dti,
    -- Feature 4: Spread metrics (Individual vs Peer Group)
    ROUND((loan_int_rate - avg_grade_int_rate), 2) AS int_rate_spread,
    ROUND((loan_amnt - avg_intent_loan_amount), 2) AS intent_amount_deviation,
    -- Feature 5: Extreme Risk Flag
    CASE WHEN calculated_dti > 0.35 THEN 1 ELSE 0 END AS is_high_debt_burden,
    loan_status
FROM BorrowerRiskProfiles
WHERE loan_int_rate IS NOT NULL;