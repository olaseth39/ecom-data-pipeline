import requests
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_products(url):
    """Fetches product data from the FakeStore API."""
    print("Fetching data from API...")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def upload_to_azure(df, container_name, blob_name):
    """Uploads a DataFrame as a Parquet file directly to Azure Data Lake."""
    print(f"Uploading data to Azure Data Lake as {blob_name}...")
    
    # 1. Convert DataFrame to Parquet in memory (no local files cluttering your computer!)
    buffer = BytesIO()
    df.to_parquet(buffer, engine='pyarrow', index=False)
    buffer.seek(0) # Reset buffer position to the beginning
    
    # 2. Connect to Azure using your connection string
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # 3. Upload the file
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(buffer, overwrite=True)
    
    print("Data successfully uploaded to Azure!")

def main():
    api_url = "https://fakestoreapi.com/products"
    container_name = "raw-data"
    
    # Create a filename with today's date
    today_date = datetime.now().strftime("%Y-%m-%d")
    blob_name = f"products_raw_{today_date}.parquet"
    
    try:
        # Fetch and convert
        data = fetch_products(api_url)
        df = pd.DataFrame(data)
        
        # Upload to Cloud
        upload_to_azure(df, container_name, blob_name)
        print("Pipeline execution completed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()