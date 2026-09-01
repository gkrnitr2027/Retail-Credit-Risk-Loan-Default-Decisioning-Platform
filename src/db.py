import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Database Connection String
# REPLACE 'your_password_here' with your actual pgAdmin password!
load_dotenv()
db_password = os.getenv("PG_PASSWORD")

if not db_password:
    raise ValueError("No password found! Please ensure PG_PASSWORD is set in your .env file.")

DB_URL = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/retail_finance"

# Create the SQLAlchemy Engine
engine = create_engine(DB_URL)

def upload_initial_data():
    """Uploads the raw Kaggle dataset into the PostgreSQL database."""
    print("--> Loading Kaggle CSV dataset...")
    try:
        df_raw = pd.read_csv("data/credit_risk_dataset.csv")
        
        print(f"--> Found {len(df_raw)} rows. Pushing to PostgreSQL (this may take a minute)...")
        # if_exists='append' adds the rows to the empty table you created in pgAdmin
        df_raw.to_sql("loan_applications", engine, index=False, if_exists="append")
        print("--> Data successfully loaded into 'loan_applications' table!")
        
    except FileNotFoundError:
        print("ERROR: Could not find 'credit_risk_dataset.csv' in the 'data' folder.")
    except Exception as e:
        print(f"ERROR: {e}")

def get_ml_data():
    """Pulls fully transformed data directly from the PostgreSQL View."""
    print("--> Extracting engineered features from PostgreSQL View...")
    
    # We query the View we created in Step 3!
    sql_query = "SELECT * FROM vw_engineered_risk_features;"
    
    with engine.connect() as conn:
        df_features = pd.read_sql_query(text(sql_query), conn)
        
    return df_features

# --- Execution Block ---
if __name__ == "__main__":
    # 1. Run the upload function (You only need to do this ONCE)
    upload_initial_data()
    
    # 2. Test pulling the engineered data back into Python
    print("\nTesting Feature Extraction...")
    ml_df = get_ml_data()
    
    if not ml_df.empty:
        print(f"\n✅ Success! Data ready for ML Training. Shape: {ml_df.shape}")
        print("\nPreview of Engineered Features:")
        # Show a few columns including our custom SQL features
        print(ml_df[['loan_amnt', 'person_income', 'calculated_dti', 'int_rate_spread', 'is_high_debt_burden']].head())