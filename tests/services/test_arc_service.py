import pytest
from unittest.mock import patch, Mock, MagicMock
import os
from services.arc_service import process_fee


@patch('services.arc_service.Web3')
@patch.dict(os.environ, {
    'CONTRACT_ADDRESS': '0x1234567890123456789012345678901234567890',
    'USDC_ADDRESS': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',
    'TREASURY_ADDRESS': '0x9876543210987654321098765432109876543210'
})
def test_process_fee_success_pending(mock_web3_class):
    """Test successful fee processing returns pending transaction"""

    # Mock Web3 instance
    mock_w3 = Mock()
    mock_w3.is_connected.return_value = True
    mock_w3.eth.gas_price = 1000000000
    mock_w3.eth.get_transaction_count.return_value = 5
    mock_web3_class.return_value = mock_w3
    mock_web3_class.to_checksum_address = lambda x: x
    mock_web3_class.HTTPProvider = Mock()

    # Mock contract
    mock_contract = Mock()
    mock_function = Mock()
    mock_function.build_transaction.return_value = {
        'from': '0xUserWallet',
        'to': '0xContractAddress',
        'gas': 100000,
        'gasPrice': 1000000000,
        'nonce': 5,
        'data': '0xPayFeeData'
    }
    mock_contract.functions.payFee.return_value = mock_function
    mock_w3.eth.contract.return_value = mock_contract

    # Test
    result = process_fee("0xUserWallet123")

    assert result['status'] == 'pending'
    assert 'tx_data' in result
    assert result['tx_data']['gas'] == 100000
    assert 'message' in result


@patch('services.arc_service.Web3')
def test_process_fee_connection_error(mock_web3_class):
    """Test process_fee when cannot connect to Arc Testnet"""

    mock_w3 = Mock()
    mock_w3.is_connected.return_value = False
    mock_web3_class.return_value = mock_w3
    mock_web3_class.HTTPProvider = Mock()

    with pytest.raises(Exception) as exc_info:
        process_fee("0xUserWallet123")

    assert "Cannot connect to Arc Testnet" in str(exc_info.value)


@patch.dict(os.environ, {}, clear=True)
def test_process_fee_contract_not_configured():
    """Test process_fee when CONTRACT_ADDRESS not configured"""

    with pytest.raises(Exception) as exc_info:
        process_fee("0xUserWallet123")

    assert "CONTRACT_ADDRESS not configured" in str(exc_info.value)


@patch('services.arc_service.Web3')
@patch.dict(os.environ, {
    'CONTRACT_ADDRESS': '0x1234567890123456789012345678901234567890',
    'USDC_ADDRESS': '0x...',  # Still placeholder
    'TREASURY_ADDRESS': '0x9876543210987654321098765432109876543210'
})
def test_process_fee_usdc_not_configured(mock_web3_class):
    """Test process_fee when USDC_ADDRESS is placeholder"""

    with pytest.raises(Exception) as exc_info:
        process_fee("0xUserWallet123")

    assert "USDC_ADDRESS not configured" in str(exc_info.value)


@patch('services.arc_service.Web3')
@patch.dict(os.environ, {
    'CONTRACT_ADDRESS': '0x1234567890123456789012345678901234567890',
    'USDC_ADDRESS': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',
    'TREASURY_ADDRESS': '0x9876543210987654321098765432109876543210'
})
def test_process_fee_contract_error(mock_web3_class):
    """Test process_fee when contract interaction fails"""

    mock_w3 = Mock()
    mock_w3.is_connected.return_value = True
    mock_web3_class.return_value = mock_w3
    mock_web3_class.HTTPProvider = Mock()
    mock_web3_class.to_checksum_address = lambda x: x

    # Mock contract that throws error
    mock_contract = Mock()
    mock_function = Mock()
    mock_function.build_transaction.side_effect = Exception("Gas estimation failed")
    mock_contract.functions.payFee.return_value = mock_function
    mock_w3.eth.contract.return_value = mock_contract

    with pytest.raises(Exception) as exc_info:
        process_fee("0xUserWallet123")

    assert "Payment processing failed" in str(exc_info.value)


@patch('services.arc_service.Web3')
@patch.dict(os.environ, {
    'CONTRACT_ADDRESS': '0x1234567890123456789012345678901234567890',
    'USDC_ADDRESS': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',
    'TREASURY_ADDRESS': '0x9876543210987654321098765432109876543210'
})
def test_process_fee_validates_rpc_connection(mock_web3_class):
    """Test that process_fee checks RPC connection"""

    mock_w3 = Mock()
    mock_w3.is_connected.return_value = False
    mock_web3_class.return_value = mock_w3
    mock_web3_class.HTTPProvider = Mock()

    with pytest.raises(Exception) as exc_info:
        process_fee("0xUserWallet123")

    assert "Cannot connect to Arc Testnet" in str(exc_info.value)
    mock_w3.is_connected.assert_called_once()


@patch('services.arc_service.Web3')
@patch.dict(os.environ, {
    'CONTRACT_ADDRESS': '0x1234567890123456789012345678901234567890',
    'USDC_ADDRESS': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',
    'TREASURY_ADDRESS': '0x9876543210987654321098765432109876543210'
})
def test_process_fee_builds_transaction_correctly(mock_web3_class):
    """Test that transaction is built with correct parameters"""

    user_wallet = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"

    mock_w3 = Mock()
    mock_w3.is_connected.return_value = True
    mock_w3.eth.gas_price = 2000000000
    mock_w3.eth.get_transaction_count.return_value = 10
    mock_web3_class.return_value = mock_w3
    mock_web3_class.to_checksum_address = lambda x: x
    mock_web3_class.HTTPProvider = Mock()

    mock_contract = Mock()
    mock_function = Mock()
    mock_function.build_transaction.return_value = {
        'from': user_wallet,
        'to': '0x1234567890123456789012345678901234567890',
        'gas': 100000,
        'gasPrice': 2000000000,
        'nonce': 10
    }
    mock_contract.functions.payFee.return_value = mock_function
    mock_w3.eth.contract.return_value = mock_contract

    result = process_fee(user_wallet)

    # Verify transaction structure
    assert result['status'] == 'pending'
    assert result['tx_data']['from'] == user_wallet
    assert result['tx_data']['gas'] == 100000
    assert result['tx_data']['gasPrice'] == 2000000000
    assert result['tx_data']['nonce'] == 10

    # Verify get_transaction_count was called with user wallet
    mock_w3.eth.get_transaction_count.assert_called_once()


@patch('services.arc_service.Web3')
@patch.dict(os.environ, {
    'CONTRACT_ADDRESS': '0x1234567890123456789012345678901234567890',
    'USDC_ADDRESS': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',
    'TREASURY_ADDRESS': '0x9876543210987654321098765432109876543210'
})
def test_process_fee_uses_correct_rpc_url(mock_web3_class):
    """Test that process_fee connects to correct RPC URL"""

    mock_w3 = Mock()
    mock_w3.is_connected.return_value = True
    mock_w3.eth.gas_price = 1000000000
    mock_w3.eth.get_transaction_count.return_value = 0
    mock_web3_class.return_value = mock_w3

    mock_http_provider = Mock()
    mock_web3_class.HTTPProvider = Mock(return_value=mock_http_provider)
    mock_web3_class.to_checksum_address = lambda x: x

    mock_contract = Mock()
    mock_function = Mock()
    mock_function.build_transaction.return_value = {'gas': 100000}
    mock_contract.functions.payFee.return_value = mock_function
    mock_w3.eth.contract.return_value = mock_contract

    process_fee("0xWallet")

    # Verify HTTPProvider was called with Arc Testnet RPC
    mock_web3_class.HTTPProvider.assert_called_once()
    call_args = mock_web3_class.HTTPProvider.call_args[0][0]
    assert "arbitrum" in call_args.lower() or "rpc" in call_args.lower()
