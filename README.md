# 🏦 Retail Lending Credit Risk & Loan Default Prediction Platform

An end-to-end **machine learning and data engineering platform** for retail lending, designed to support **automated credit risk assessment, portfolio monitoring, and real-time loan default prediction**.

The project integrates **PostgreSQL, advanced SQL analytics, feature engineering, cost-sensitive machine learning, XGBoost, and Streamlit** into a production-oriented credit risk workflow.

---

## 🚀 Key Features

### 🗄️ Relational Database & Feature Store

* Built on **PostgreSQL** with custom database schemas, indexes, and SQL views.
* Implements a reusable feature engineering layer through:

```text
vw_engineered_risk_features
```

* Automates borrower-level feature transformation directly within the database.
* Separates raw application data from engineered risk features and inference audit information.

### 📊 Advanced SQL Analytics

Uses advanced SQL techniques for borrower and portfolio-level risk analysis, including:

* Common Table Expressions (**CTEs**)
* Window Functions
* `PARTITION BY`
* Debt-to-Income (**DTI**) calculations
* Interest-rate spread calculations
* Payment and borrower risk indicators

These SQL transformations provide structured features for downstream machine learning models.

### 🤖 Machine Learning & Model Evaluation

* Developed a supervised **loan default classification** pipeline using **XGBoost**.
* Implemented **scikit-learn Pipelines** for reproducible preprocessing and model inference.
* Addressed class imbalance using cost-sensitive learning with:

```python
scale_pos_weight
```

* Dataset contains an approximately **21% default rate**, making minority-class detection an important modeling consideration.

### 📈 Rigorous ML Evals

Model performance is evaluated using metrics appropriate for imbalanced classification:

* **ROC-AUC:** ~0.94
* **PR-AUC:** ~0.88

ROC-AUC measures the model's ability to rank borrowers by default risk, while PR-AUC provides a more focused evaluation of minority-class detection under precision-recall constraints.

### 🖥️ Interactive Underwriting Dashboard

Built an interactive **Streamlit** application for real-time borrower risk assessment.

The dashboard provides:

* Borrower information input
* Credit score interpretation
* Default probability
* Risk-tier classification
* Real-time model inference
* Underwriting-oriented risk assessment

Credit scores are translated to a standardized **300–850 scale** and mapped into risk tiers for easier interpretation.

### 🔬 Exploratory Data Analysis

Includes dedicated Jupyter notebooks covering:

* Data exploration
* Missing-value analysis
* Distribution analysis
* Default-rate analysis
* Feature relationships
* Risk pattern discovery
* Feature engineering experiments
* Model evaluation and comparison

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   Raw Loan Data      │
                    │   CSV / Applications │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      PostgreSQL      │
                    │                      │
                    │  Raw Tables          │
                    │  Indexes             │
                    │  SQL Transformations │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Feature Engineering  │
                    │                      │
                    │ CTEs                 │
                    │ Window Functions     │
                    │ Risk Ratios          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ML Feature Store   │
                    │                      │
                    │ Engineered Risk      │
                    │ Features             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    XGBoost Model     │
                    │                      │
                    │ Cost-Sensitive       │
                    │ Classification       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Default Probability  │
                    │ + Risk Tier          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Streamlit Dashboard  │
                    │                      │
                    │ Real-Time Underwriting│
                    │ & Portfolio Insights │
                    └──────────────────────┘
```

---

# 📁 Project Structure

```text
credit-risk-platform/
│
├── sql/
│   ├── 01_schema.sql
│   └── 02_feature_engineering.sql
│
├── src/
│   ├── db.py
│   └── risk_engine.py
│
├── notebooks/
│   ├── 01_EDA_and_Feature_Engineering.ipynb
│   └── 02_Model_Training_and_Evals.ipynb
│
├── data/
│   └── credit_risk_dataset.csv
│
├── models/
│   └── credit_risk_xgb_pipeline.pkl
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🛠️ Technology Stack

| Category          | Technologies                       |
| ----------------- | ---------------------------------- |
| Programming       | Python                             |
| Data Processing   | Pandas, NumPy                      |
| Database          | PostgreSQL                         |
| SQL               | CTEs, Window Functions, Views      |
| Machine Learning  | Scikit-learn, XGBoost              |
| Model Evaluation  | ROC-AUC, PR-AUC, Precision, Recall |
| Dashboard         | Streamlit                          |
| Visualization     | Matplotlib / Seaborn               |
| Development       | Jupyter Notebook                   |
| Configuration     | Python-dotenv                      |
| Model Persistence | Pickle                             |

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/credit-risk-platform.git
cd credit-risk-platform
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
PG_PASSWORD=your_actual_postgres_password
```

> **Important:** Never commit `.env` or database credentials to GitHub.

Add the following to `.gitignore`:

```text
.env
__pycache__/
*.pyc
.ipynb_checkpoints/
```

## 4. Create the PostgreSQL Database

Create a database named:

```text
retail_finance
```

Using pgAdmin or the PostgreSQL command line.

## 5. Initialize Database Schema

Execute the SQL scripts in order:

```text
sql/01_schema.sql
```

followed by:

```text
sql/02_feature_engineering.sql
```

This creates the required tables, indexes, and engineered risk-feature view.

## 6. Load and Validate Data

Run:

```bash
python -m src.db
```

This loads the dataset into PostgreSQL and validates database connectivity and feature extraction.

## 7. Run the Streamlit Application

Launch the underwriting dashboard:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📊 Model Performance

### XGBoost Classifier

The final model uses an **XGBoost classification pipeline** with cost-sensitive learning to address class imbalance.

| Metric       | Score |
| ------------ | ----: |
| ROC-AUC      | ~0.94 |
| PR-AUC       | ~0.88 |
| Default Rate |  ~21% |

### Why ROC-AUC and PR-AUC?

Because loan default is an imbalanced classification problem, accuracy alone can provide a misleading view of model performance.

**ROC-AUC** evaluates how effectively the model ranks borrowers according to default risk.

**PR-AUC** focuses more directly on the model's ability to identify the minority default class while maintaining useful precision.

---

# 💡 Business Use Cases

The platform can support several retail lending workflows:

### Automated Credit Underwriting

Estimate borrower default probability before loan approval.

### Risk-Based Segmentation

Classify applicants into risk tiers for differentiated underwriting decisions.

### Portfolio Risk Monitoring

Analyze default patterns across borrower and loan segments.

### Early Risk Identification

Identify borrower profiles associated with elevated default probability.

### Data-Driven Lending Decisions

Combine SQL-derived financial features with machine learning predictions to support credit decision-making.

---

# 🔍 Example Workflow

```text
Borrower Application
        ↓
PostgreSQL Data Retrieval
        ↓
SQL Feature Engineering
        ↓
Risk Feature Generation
        ↓
XGBoost Inference
        ↓
Default Probability
        ↓
Risk Tier
        ↓
Underwriting Recommendation
```

Example:

```text
Credit Score:        640
Loan Amount:         ₹5,00,000
Debt-to-Income:      48%
Previous Delays:     3

Predicted Default Risk: 78%
Risk Tier:              HIGH
```

---

# 📓 Notebooks

### `01_EDA_and_Feature_Engineering.ipynb`

Contains:

* Exploratory data analysis
* Data quality checks
* Distribution analysis
* Default-rate analysis
* Feature relationships
* Feature engineering
* Initial modeling experiments

### `02_Model_Training_and_Evals.ipynb`

Contains:

* Train/test preparation
* Scikit-learn pipeline
* XGBoost training
* Class imbalance handling
* Hyperparameter tuning
* ROC-AUC evaluation
* PR-AUC evaluation
* Model comparison

---

# 🔐 Security Considerations

* Database credentials are stored using environment variables.
* `.env` is excluded from version control.
* No production credentials are included in the repository.
* The exported model artifact is separated from source code and data pipelines.

---

# 🎯 Project Highlights

```text
✓ End-to-end ML pipeline
✓ PostgreSQL feature engineering
✓ Advanced SQL analytics
✓ CTEs & Window Functions
✓ XGBoost classification
✓ Cost-sensitive learning
✓ Imbalanced classification
✓ ROC-AUC & PR-AUC evaluation
✓ Real-time inference
✓ Streamlit underwriting dashboard
✓ Reproducible ML pipeline
✓ Production-oriented project architecture
```

---

## 👨‍💻 Skills Demonstrated

**Python • SQL • PostgreSQL • Pandas • NumPy • Scikit-learn • XGBoost • Feature Engineering • Exploratory Data Analysis • Machine Learning • Classification • Model Evaluation • Streamlit • Data Engineering • Risk Analytics • Credit Risk**

---

## 📌 Disclaimer

This project is developed for **educational and portfolio purposes**. The predictions and risk classifications should not be used as the sole basis for real-world lending or financial decisions.
