import requests
from unittest.mock import patch, Mock

@patch('requests.get')
def test_api_returns_successful_data(mock_get):
    """Tests that our logic handles a successful API response correctly."""
    url = "https://fakestoreapi.com/products"
    
    # 1. Create a fake (mock) successful API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "title": "Test Product", "price": 9.99}]
    mock_get.return_value = mock_response
    
    # 2. Call the API (it will actually return our mock response)
    response = requests.get(url)
    
    # 3. Assert it returned a 200 OK status
    assert response.status_code == 200
    
    # 4. Assert it returned data and isn't empty
    data = response.json()
    assert len(data) > 0
    
    # 5. Assert the data is actually a list
    assert isinstance(data, list)