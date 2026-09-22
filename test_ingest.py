import requests

def test_api_returns_successful_data():
    """Tests that the FakeStore API is reachable and returns a list of products."""
    url = "https://fakestoreapi.com/products"
    
    # 1. Call the API
    response = requests.get(url)
    
    # 2. Assert it returned a 200 OK status
    assert response.status_code == 200
    
    # 3. Assert it returned data and isn't empty
    data = response.json()
    assert len(data) > 0
    
    # 4. Assert the data is actually a list
    assert isinstance(data, list)