import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from backend.main import app

client = TestClient(app)


def test_shop_endpoint_success():
    """Test successful shop request"""

    # Mock the find_savings function
    with patch('api_routes.shop.find_savings') as mock_find_savings:
        mock_find_savings.return_value = {
            "savings_6mo": 275.50,
            "new_carrier": "Liberty Shield"
        }

        response = client.post("/v1/shop", json={
            "bodily_injury": "100000/300000",
            "property_damage": "50000",
            "uninsured_motorist": "100000/300000",
            "collision": "1000",
            "comprehensive": "500",
            "personal_injury_protection": "10000"
        })

        assert response.status_code == 200
        data = response.json()
        assert "savings_6mo" in data
        assert "new_carrier" in data
        assert data["savings_6mo"] == 275.50
        assert data["new_carrier"] == "Liberty Shield"

        # Verify find_savings was called with correct data
        mock_find_savings.assert_called_once()


def test_shop_endpoint_missing_fields():
    """Test shop request with missing required fields"""

    response = client.post("/v1/shop", json={
        "bodily_injury": "100000/300000",
        # Missing other required fields
    })

    # FastAPI validation should return 422 for missing fields
    assert response.status_code == 422


def test_shop_endpoint_invalid_json():
    """Test shop request with invalid JSON"""

    response = client.post("/v1/shop", data="not json", headers={"Content-Type": "application/json"})

    assert response.status_code == 422


def test_shop_endpoint_agent_error():
    """Test shop endpoint when agent throws error"""

    with patch('api_routes.shop.find_savings') as mock_find_savings:
        mock_find_savings.side_effect = Exception("Agent service unavailable")

        response = client.post("/v1/shop", json={
            "bodily_injury": "100000/300000",
            "property_damage": "50000",
            "uninsured_motorist": "100000/300000",
            "collision": "1000",
            "comprehensive": "500",
            "personal_injury_protection": "10000"
        })

        assert response.status_code == 500
        assert "detail" in response.json()


def test_shop_endpoint_realistic_data():
    """Test with realistic insurance policy data"""

    with patch('api_routes.shop.find_savings') as mock_find_savings:
        mock_find_savings.return_value = {
            "savings_6mo": 246.00,
            "new_carrier": "Rebel Mutual"
        }

        response = client.post("/v1/shop", json={
            "bodily_injury": "250000/500000",
            "property_damage": "100000",
            "uninsured_motorist": "250000/500000",
            "collision": "500",
            "comprehensive": "500",
            "personal_injury_protection": "50000"
        })

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["savings_6mo"], (int, float))
        assert isinstance(data["new_carrier"], str)
        assert data["savings_6mo"] > 0


def test_shop_endpoint_returns_json():
    """Test that shop endpoint returns proper JSON"""

    with patch('api_routes.shop.find_savings') as mock_find_savings:
        mock_find_savings.return_value = {
            "savings_6mo": 200.00,
            "new_carrier": "Test Carrier"
        }

        response = client.post("/v1/shop", json={
            "bodily_injury": "100000/300000",
            "property_damage": "50000",
            "uninsured_motorist": "100000/300000",
            "collision": "1000",
            "comprehensive": "500",
            "personal_injury_protection": "10000"
        })

        assert response.headers["content-type"] == "application/json"
        # Should be valid JSON
        data = response.json()
        assert isinstance(data, dict)
