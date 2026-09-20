import requests
import pandas as pd
import os
from datetime import datetime

def fetch_products(url):
    """Fetches product data from the FakeStore API."""
    print("Fetching data from API...")
    response = requests.get(url)
    response.raise_for_status()  # This will throw an error if the API call fails
    return response.json()

def save_to_parquet(data, folder_name="data"):
    """Converts JSON data to a DataFrame and saves it as a Parquet file."""
    print("Converting data to Pandas DataFrame...")
    df = pd.DataFrame(data)
    
    # Create a data folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)
    
    # Create a filename with today's date (good practice for daily batches)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f"{folder_name}/products_raw_{today_date}.parquet"
    
    print(f"Saving data to {file_path}...")
    df.to_parquet(file_path, engine='pyarrow', index=False)
    print("Data successfully saved!")
    
    return file_path

def main():
    api_url = "https://fakestoreapi.com/products"
    
    try:
        data = fetch_products(api_url)
        save_to_parquet(data)
        print("Pipeline execution completed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()