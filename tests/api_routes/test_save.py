import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from backend.main import app

client = TestClient(app)


def test_save_endpoint_success():
    """Test successful save request"""

    # Mock the process_fee function
    with patch('api_routes.save.process_fee') as mock_process_fee:
        mock_process_fee.return_value = {
            "status": "success",
            "tx_hash": "0x1234567890abcdef"
        }

        response = client.post("/v1/save", json={
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # Verify process_fee was called with correct wallet
        mock_process_fee.assert_called_once_with("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0")


def test_save_endpoint_missing_wallet():
    """Test save request with missing wallet address"""

    response = client.post("/v1/save", json={})

    # FastAPI validation should return 422 for missing field
    assert response.status_code == 422


def test_save_endpoint_invalid_json():
    """Test save request with invalid JSON"""

    response = client.post("/v1/save", data="not json", headers={"Content-Type": "application/json"})

    assert response.status_code == 422


def test_save_endpoint_arc_service_error():
    """Test save endpoint when Arc service throws error"""

    with patch('api_routes.save.process_fee') as mock_process_fee:
        mock_process_fee.side_effect = Exception("Arc Testnet connection failed")

        response = client.post("/v1/save", json={
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        })

        assert response.status_code == 500
        assert "detail" in response.json()
        assert "Arc Testnet connection failed" in response.json()["detail"]


def test_save_endpoint_various_wallet_formats():
    """Test save endpoint with different wallet address formats"""

    test_wallets = [
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",  # Standard format
        "0x0000000000000000000000000000000000000000",  # Zero address
        "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",  # Max address
    ]

    with patch('api_routes.save.process_fee') as mock_process_fee:
        mock_process_fee.return_value = {"status": "success"}

        for wallet in test_wallets:
            response = client.post("/v1/save", json={
                "wallet_address": wallet
            })

            assert response.status_code == 200
            assert response.json()["status"] == "success"


def test_save_endpoint_pending_transaction():
    """Test save endpoint when transaction is pending (user needs to sign)"""

    with patch('api_routes.save.process_fee') as mock_process_fee:
        mock_process_fee.return_value = {
            "status": "pending",
            "tx_data": {
                "to": "0xContractAddress",
                "data": "0xPayFeeData",
                "gas": 100000
            },
            "message": "Transaction prepared. User must sign and send."
        }

        response = client.post("/v1/save", json={
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        })

        assert response.status_code == 200
        # Even if Arc service returns pending, endpoint returns success
        assert response.json()["status"] == "success"


def test_save_endpoint_contract_not_configured():
    """Test save endpoint when contract is not deployed"""

    with patch('api_routes.save.process_fee') as mock_process_fee:
        mock_process_fee.side_effect = Exception("CONTRACT_ADDRESS not configured. Please deploy contract first.")

        response = client.post("/v1/save", json={
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        })

        assert response.status_code == 500
        assert "CONTRACT_ADDRESS not configured" in response.json()["detail"]


def test_save_endpoint_returns_json():
    """Test that save endpoint returns proper JSON"""

    with patch('api_routes.save.process_fee') as mock_process_fee:
        mock_process_fee.return_value = {"status": "success"}

        response = client.post("/v1/save", json={
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        })

        assert response.headers["content-type"] == "application/json"
        # Should be valid JSON
        data = response.json()
        assert isinstance(data, dict)
        assert "status" in data


def test_save_endpoint_invalid_wallet_format():
    """Test save endpoint with clearly invalid wallet address"""

    # Note: FastAPI accepts any string for wallet_address
    # Actual validation happens in arc_service.py
    with patch('api_routes.save.process_fee') as mock_process_fee:
        mock_process_fee.side_effect = Exception("Invalid wallet address format")

        response = client.post("/v1/save", json={
            "wallet_address": "not_a_valid_address"
        })

        assert response.status_code == 500
        assert "detail" in response.json()
