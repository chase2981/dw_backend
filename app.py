from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import snowflake.connector
import os
import pandas as pd

app = FastAPI()

# Add this before defining routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Or restrict to ["http://localhost:8000"] if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_snowflake_data():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vw_customer_summary")
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[col[0] for col in cursor.description])
    cursor.close()
    conn.close()
    return df.to_dict(orient="records")

@app.get("/data")
def read_data():
    return get_snowflake_data()
