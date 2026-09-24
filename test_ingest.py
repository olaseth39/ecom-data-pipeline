import requests

def test_api_returns_successful_data():
    """Tests that the FakeStore API is reachable and returns a list of products."""
    url = "https://fakestoreapi.com/products"
    
    # Add headers to bypass 403 Forbidden blocks on Linux servers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Data-Engineering-Pipeline/1.0"
    }
    
    # 1. Call the API
    response = requests.get(url, headers=headers)
    
    # 2. Assert it returned a 200 OK status
    assert response.status_code == 200
    
    # 3. Assert it returned data and isn't empty
    data = response.json()
    assert len(data) > 0
    
    # 4. Assert the data is actually a list
    assert isinstance(data, list)