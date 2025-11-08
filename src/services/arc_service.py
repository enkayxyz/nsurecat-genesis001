from web3 import Web3

# Placeholder values - replace with actual deployed contract details
ARC_RPC_URL = "https://rpc-testnet.arbitrum.io"  # Arc Testnet RPC
CONTRACT_ADDRESS = "0x..."  # Deployed contract address
TREASURY_ADDRESS = "0x..."  # NsureCat treasury wallet
USDC_ADDRESS = "0x..."  # USDC on Arc Testnet

# Contract ABI - updated for variable fee amounts
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_treasury", "type": "address"},
            {"internalType": "address", "name": "_usdcToken", "type": "address"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "payFee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "treasury",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "usdcToken",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def process_fee(user_wallet: str, fee_amount: int):
    """
    Prepares a smart contract transaction to transfer fee_amount USDC from user wallet to treasury.
    
    Args:
        user_wallet: User's wallet address
        fee_amount: Amount in USDC smallest units (6 decimals)
    
    Returns:
        dict with transaction data for frontend signing
    """
    # Validate configuration
    if not CONTRACT_ADDRESS or CONTRACT_ADDRESS == "0x...":
        raise Exception("CONTRACT_ADDRESS not configured. Please deploy contract first.")

    if not USDC_ADDRESS or USDC_ADDRESS == "0x...":
        raise Exception("USDC_ADDRESS not configured. Please check .env file.")

    # Connect to Arc Testnet
    w3 = Web3(Web3.HTTPProvider(ARC_RPC_URL))
    if not w3.is_connected():
        raise Exception("Cannot connect to Arc Testnet. Check RPC_URL.")

    # Initialize contract
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS),
        abi=CONTRACT_ABI
    )

    try:
        # Build transaction data for frontend signing
        tx_data = contract.functions.payFee(fee_amount).build_transaction({
            'from': Web3.to_checksum_address(user_wallet),
            'gas': 100000,  # Conservative gas limit
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(user_wallet)),
        })

        return {
            "status": "pending",
            "tx_data": tx_data,
            "message": "Transaction prepared. User must sign and send."
        }

    except Exception as e:
        raise Exception(f"Payment processing failed: {str(e)}")