🏦 Retail Lending Credit Risk & Loan Default Prediction Platform
An end-to-end, production-ready machine learning and data engineering platform designed for automated retail credit underwriting, portfolio risk monitoring, and real-time inference. Built to meet rigorous data science and MLOps standards, integrating relational data stores, advanced SQL analytics, cost-sensitive machine learning, and an interactive web interface.

🚀 Key Features & Technical Capabilities
Relational Database & Feature Store (PostgreSQL): Utilizes custom PostgreSQL schemas, indexing, and virtual SQL views (vw_engineered_risk_features) to automate feature transformation at the database level.

Advanced SQL Analytics: Implements Common Table Expressions (CTEs), window functions (PARTITION BY), and risk ratio calculations to evaluate borrower debt-to-income and interest rate spreads.

Rigorous ML Evals & Imbalance Handling: Employs scikit-learn pipelines and XGBoost with cost-sensitive learning (scale_pos_weight) to handle severe class imbalance (~21% default rate). Evaluated strictly using ROC-AUC and PR-AUC (Precision-Recall).

Interactive Underwriting Dashboard (Streamlit): Features a production-grade web application for credit officers to evaluate risk in real-time, complete with credit score translation (300–850 scale) and risk-tier banding.

Complete EDA & Prototyping: Includes fully documented Jupyter Notebooks detailing exploratory data analysis, pattern discovery, and feature prototyping.

credit-risk-platform/
├── sql/
│   ├── 01_schema.sql                      # PostgreSQL DDL for applications & inference audit logs
│   └── 02_feature_engineering.sql         # SQL view containing CTEs and Window Functions
│
├── src/
│   ├── db.py                              # PostgreSQL connector & data loader module
│   └── risk_engine.py                     # Real-time feature engineering & inference scoring logic
│
├── notebooks/
│   ├── 01_EDA_and_Feature_Engineering.ipynb # Exploratory data analysis & feature prototyping
│   └── 02_Model_Training_and_Evals.ipynb    # XGBoost training, hyperparameter tuning & evaluation
│
├── data/
│   └── credit_risk_dataset.csv            # Raw retail lending dataset
│
├── models/
│   └── credit_risk_xgb_pipeline.pkl       # Exported production pipeline artifact
│
├── app.py                                 # Streamlit web application interface
├── requirements.txt                       # Project python dependencies
└── .env                                   # Secure environment variables (git-ignored)

⚙️ Step-by-Step Setup & Installation
1. Clone the Repository
Bash
git clone https://github.com/your-username/credit-risk-platform.git
cd credit-risk-platform
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Configure Secure Environment Variables
Create a file named .env in the root directory of your project and configure your local PostgreSQL database credentials:

Code snippet
PG_PASSWORD=your_actual_postgres_password
(Note: Create a .gitignore file and include .env to keep your credentials secure.)

4. Initialize PostgreSQL Schema
Open pgAdmin and create a database named retail_finance.

Open the Query Tool and execute the scripts found in the sql/ folder:

Run sql/01_schema.sql to build the required tables and indexes.

Run sql/02_feature_engineering.sql to establish the feature engineering view.

5. Load Data & Test Database Connector
Run the database script to upload the raw Kaggle dataset into PostgreSQL and verify feature extraction:

Bash
python -m src.db
6. Run the Streamlit Application
Launch the interactive underwriting platform locally in your browser:

Bash
streamlit run app.py
📊 Model Performance & Evals Summary
Algorithm: XGBoost Classifier (Optimized via Scikit-Learn Pipelines)

Imbalance Mitigation: scale_pos_weight adjustment

Evaluation Metrics:

ROC-AUC: ~0.94 (Strong capability in ranking default risk)

PR-AUC: ~0.88 (Robust performance under strict precision-recall constraints for minority default detection)
