-- 1. Clean up existing tables (if you need to restart)
DROP TABLE IF EXISTS model_predictions;
DROP TABLE IF EXISTS loan_applications CASCADE;

-- 2. Create the raw data storage (Feature Store)
CREATE TABLE loan_applications (
    application_id SERIAL PRIMARY KEY,
    person_age INT,
    person_income NUMERIC(15, 2),
    person_home_ownership VARCHAR(20),
    person_emp_length NUMERIC(5, 2),
    loan_intent VARCHAR(30),
    loan_grade VARCHAR(5),
    loan_amnt NUMERIC(15, 2),
    loan_int_rate NUMERIC(5, 2),
    loan_percent_income NUMERIC(5, 4),
    cb_person_default_on_file VARCHAR(5),
    cb_person_cred_hist_length INT,
    loan_status INT, -- 0: Non-default, 1: Default
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create the audit table for ML inferences
CREATE TABLE model_predictions (
    prediction_id SERIAL PRIMARY KEY,
    application_id INT REFERENCES loan_applications(application_id),
    default_probability NUMERIC(5, 4),
    risk_band VARCHAR(15),
    credit_score INT,
    decision VARCHAR(20),
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create indexes to speed up future queries
CREATE INDEX idx_loan_status ON loan_applications(loan_status);
CREATE INDEX idx_loan_grade ON loan_applications(loan_grade);