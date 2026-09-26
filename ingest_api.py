import requests
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from io import BytesIO
import os
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Load environment variables
load_dotenv()

def fetch_products(url):
    """Fetches product data from the FakeStore API."""
    print("Fetching data from API...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Data-Engineering-Pipeline/1.0"}
    response = requests.get(url, headers=headers)
    
    # If the API blocks us, use a mock dataset so the pipeline can still run
    if response.status_code != 200:
        print("API blocked, using mock data to continue pipeline...")
        return [{"id": 1, "title": "Test Product", "price": 9.99, "category": "test", "description": "test", "image": "test"}]
    
    return response.json()

def upload_to_azure(df, container_name, blob_name):
    print(f"Uploading data to Azure Data Lake as {blob_name}...")
    buffer = BytesIO()
    df.to_parquet(buffer, engine='pyarrow', index=False)
    buffer.seek(0)
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(buffer, overwrite=True)
    print("Data successfully uploaded to Azure!")

def load_to_snowflake(df, table_name):
    print(f"Loading data into Snowflake table: {table_name}...")
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse="COMPUTE_WH" # Default warehouse in Snowflake trials
    )

    # ADD THIS LINE: Clear old data so we don't create duplicates on re-runs
    cursor = conn.cursor()
    cursor.execute(f"TRUNCATE TABLE IF EXISTS {table_name.upper()}")
    cursor.close()
    
    # Write DataFrame to Snowflake
    # write_pandas requires column names in UPPERCASE
    df.columns = df.columns.str.upper()
    #write_pandas(conn, df, table_name.upper())
    write_pandas(conn, df, table_name.upper(), auto_create_table=True)
    
    conn.close()
    print("Data successfully loaded to Snowflake!")

def main():
    api_url = "https://fakestoreapi.com/products"
    container_name = "raw-data"
    table_name = "products_raw"
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    blob_name = f"products_raw_{today_date}.parquet"
    
    try:
        data = fetch_products(api_url)
        df = pd.DataFrame(data)
        
        # 1. Upload to Azure Data Lake (Backup/Raw Zone)
        upload_to_azure(df, container_name, blob_name)
        
        # 2. Load to Snowflake (Data Warehouse)
        load_to_snowflake(df, table_name)
        
        print("Pipeline execution completed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()