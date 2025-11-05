# Arc Testnet Deployment Requirements

**Status**: 🔴 CRITICAL - Required for Payment Integration
**Priority**: HIGH
**Owner**: Backend Engineer
**Created**: 2025-11-05
**Estimated Time**: 3-4 hours

---

## 📋 Overview

This document outlines the steps required to deploy the NsureCat smart contract to Arc Testnet and integrate it with the backend payment flow. The smart contract (`NsureCatFee.sol`) handles the 0.01 USDC fee collection from users when they choose to save on their insurance.

**Current Status**: Smart contract code is complete but NOT deployed. The `arc_service.py` has placeholder addresses that need to be updated.

---

## 🎯 Objectives

1. Deploy `NsureCatFee.sol` smart contract to Arc Testnet
2. Create and fund a treasury wallet for fee collection
3. Update backend configuration with deployed addresses
4. Implement real payment logic in `arc_service.py`
5. Test end-to-end USDC payment flow

---

## 📁 Files Involved

| File | Location | Status | Action Required |
|------|----------|--------|-----------------|
| Smart Contract | `src/contracts/NsureCatFee.sol` | ✅ Complete | Deploy to Arc Testnet |
| Arc Service | `src/services/arc_service.py` | ⚠️ Placeholders | Update with real addresses |
| Environment Config | `.env` | ❌ Missing values | Add contract addresses |
| Service Caller | `src/api_routes/save.py` | ✅ Complete | No changes needed |

---

## 🔧 Prerequisites

Before starting, ensure you have:

- [ ] **Solidity Development Environment**
  - Hardhat, Foundry, or Remix IDE
  - Node.js 16+ (if using Hardhat)

- [ ] **Arc Testnet Access**
  - Arc Testnet RPC URL: `https://rpc-testnet.arbitrum.io`
  - Arc Testnet Chain ID: Check official Arc documentation

- [ ] **Wallets**
  - MetaMask or compatible wallet
  - Two wallet addresses:
    1. **Deployer wallet** (to deploy contract)
    2. **Treasury wallet** (to receive fees)

- [ ] **Testnet Tokens**
  - Testnet ETH for gas fees (from Arc faucet)
  - USDC testnet tokens for testing

- [ ] **Python Dependencies**
  - `web3==7.14.0` (already in requirements.txt)
  - `python-dotenv==1.0.0` (already in requirements.txt)

---

## 📝 Step-by-Step Deployment Guide

### Step 1: Get USDC Contract Address on Arc Testnet

```bash
# Find the official USDC testnet contract on Arc
# Check Arc documentation or block explorer
# Example format: 0x1234567890123456789012345678901234567890
```

**Update**:
- Look up Arc Testnet USDC address from official docs
- If not available, may need to deploy a mock ERC20 USDC for testing

**Expected Output**: `USDC_ADDRESS=0x...`

---

### Step 2: Create Treasury Wallet

```bash
# Option A: Use existing MetaMask wallet
# - Create new account in MetaMask
# - Copy the address (treasury wallet)

# Option B: Generate programmatically
from web3 import Web3
w3 = Web3()
account = w3.eth.account.create()
print(f"Treasury Address: {account.address}")
print(f"Private Key: {account.key.hex()}")  # KEEP SECRET!
```

**Security**:
- Store treasury private key securely (not in code!)
- Consider using a multisig wallet for production

**Expected Output**: `TREASURY_ADDRESS=0x...`

---

### Step 3: Fund Wallets with Testnet Tokens

```bash
# 1. Get testnet ETH for gas
# Visit Arc Testnet faucet and request tokens
# Send to both deployer and treasury wallets

# 2. Get USDC testnet tokens
# Use USDC faucet or request from team
```

**Amounts Needed**:
- Deployer: ~0.1 testnet ETH (for deployment gas)
- Test User: ~1-5 USDC testnet (for testing payments)

---

### Step 4: Deploy Smart Contract

#### Option A: Using Remix IDE (Easiest)

1. **Open Remix**: https://remix.ethereum.org/
2. **Create Contract File**:
   - Copy contents of `src/contracts/NsureCatFee.sol`
   - Paste into new file in Remix
3. **Compile**:
   - Select Solidity Compiler (0.8.x)
   - Click "Compile NsureCatFee.sol"
4. **Deploy**:
   - Switch to "Deploy & Run Transactions" tab
   - Set Environment to "Injected Provider - MetaMask"
   - Connect to Arc Testnet in MetaMask
   - Fill constructor parameters:
     - `_treasury`: Your treasury wallet address
     - `_usdcToken`: USDC contract address from Step 1
   - Click "Deploy" and confirm in MetaMask

#### Option B: Using Hardhat (Advanced)

```bash
# Initialize Hardhat project
npx hardhat init

# Install dependencies
npm install --save-dev @nomicfoundation/hardhat-toolbox

# Create deployment script: scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const TREASURY = "0x...";  // From Step 2
  const USDC = "0x...";      // From Step 1

  const NsureCatFee = await hre.ethers.getContractFactory("NsureCatFee");
  const contract = await NsureCatFee.deploy(TREASURY, USDC);
  await contract.deployed();

  console.log("NsureCatFee deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

# Configure hardhat.config.js
module.exports = {
  networks: {
    arcTestnet: {
      url: "https://rpc-testnet.arbitrum.io",
      accounts: [process.env.DEPLOYER_PRIVATE_KEY]
    }
  },
  solidity: "0.8.0"
};

# Deploy
npx hardhat run scripts/deploy.js --network arcTestnet
```

**Expected Output**:
```
NsureCatFee deployed to: 0x1234567890abcdef...
```

**Save This**: `CONTRACT_ADDRESS=0x...`

---

### Step 5: Verify Contract ABI

After deployment, get the full contract ABI:

```json
[
  {
    "inputs": [
      {"internalType": "address", "name": "_treasury", "type": "address"},
      {"internalType": "address", "name": "_usdcToken", "type": "address"}
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "payFee",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "feeAmount",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
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
```

---

### Step 6: Update Backend Configuration

#### 6.1 Update `.env` file

```bash
# Add these to your .env file
ARC_RPC_URL=https://rpc-testnet.arbitrum.io
CONTRACT_ADDRESS=0x...  # From Step 4
TREASURY_ADDRESS=0x...  # From Step 2
USDC_ADDRESS=0x...      # From Step 1

# Optional: Backend wallet for signing transactions
BACKEND_WALLET_PRIVATE_KEY=0x...  # If backend needs to sign transactions
```

#### 6.2 Update `src/services/arc_service.py`

Replace the placeholder code with real implementation:

```python
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# Load from environment variables
ARC_RPC_URL = os.getenv("ARC_RPC_URL", "https://rpc-testnet.arbitrum.io")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
TREASURY_ADDRESS = os.getenv("TREASURY_ADDRESS")
USDC_ADDRESS = os.getenv("USDC_ADDRESS")
BACKEND_PRIVATE_KEY = os.getenv("BACKEND_WALLET_PRIVATE_KEY")

# Full contract ABI (from Step 5)
CONTRACT_ABI = [
    # ... paste full ABI here
]

def process_fee(user_wallet: str):
    """
    Calls the smart contract to transfer 0.01 USDC fee from user wallet.

    Note: This assumes the user has already approved the contract to spend USDC.
    Frontend should handle the approval transaction first.
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
        # Option A: User signs transaction (frontend handles)
        # Return transaction data for frontend to sign
        tx_data = contract.functions.payFee().build_transaction({
            'from': Web3.to_checksum_address(user_wallet),
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(user_wallet)),
        })

        return {
            "status": "pending",
            "tx_data": tx_data,
            "message": "Transaction prepared. User must sign and send."
        }

        # Option B: Backend signs transaction (requires BACKEND_PRIVATE_KEY)
        # Only use if backend manages user wallets (Circle wallet flow)
        # if BACKEND_PRIVATE_KEY:
        #     account = w3.eth.account.from_key(BACKEND_PRIVATE_KEY)
        #     tx = contract.functions.payFee().build_transaction({...})
        #     signed_tx = account.sign_transaction(tx)
        #     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        #     return {"status": "success", "tx_hash": tx_hash.hex()}

    except Exception as e:
        raise Exception(f"Payment processing failed: {str(e)}")
```

---

### Step 7: Test the Integration

#### 7.1 Unit Test with Web3

Create `tests/backend/test_arc_service.py`:

```python
import pytest
from unittest.mock import Mock, patch
from services.arc_service import process_fee

@patch('services.arc_service.Web3')
def test_process_fee_success(mock_web3):
    # Mock Web3 connection
    mock_w3_instance = Mock()
    mock_w3_instance.is_connected.return_value = True
    mock_w3_instance.eth.gas_price = 1000000000
    mock_w3_instance.eth.get_transaction_count.return_value = 5
    mock_web3.return_value = mock_w3_instance

    # Mock contract
    mock_contract = Mock()
    mock_contract.functions.payFee().build_transaction.return_value = {
        'to': '0x123...',
        'data': '0xabc...',
        'gas': 100000
    }
    mock_w3_instance.eth.contract.return_value = mock_contract

    # Test
    result = process_fee("0xUserWallet...")

    assert result['status'] == 'pending'
    assert 'tx_data' in result
```

Run: `pytest tests/backend/test_arc_service.py -v`

#### 7.2 Integration Test (Manual)

```bash
# 1. Start backend server
cd src/backend
python main.py

# 2. Test shop endpoint
curl -X POST http://localhost:8000/v1/shop \
  -H "Content-Type: application/json" \
  -d '{
    "bodily_injury": "100000/300000",
    "property_damage": "50000",
    "uninsured_motorist": "100000/300000",
    "collision": "1000",
    "comprehensive": "500",
    "personal_injury_protection": "10000"
  }'

# Expected: {"savings": 246.0, "carrier": "Rebel Mutual"}

# 3. Test save endpoint
curl -X POST http://localhost:8000/v1/save \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "0xYourTestWallet..."}'

# Expected: {"status": "success"} or {"status": "pending", "tx_data": {...}}
```

#### 7.3 Frontend Integration Test

1. Open frontend: `http://localhost:8001`
2. Complete chat flow and get quote
3. Click "Let's Save Money!"
4. Connect MetaMask wallet
5. Approve USDC spending (2-step process):
   - First: Approve contract to spend USDC
   - Second: Call payFee() function
6. Verify transaction on Arc Testnet explorer
7. Check treasury wallet received 0.01 USDC

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Contract deployed successfully to Arc Testnet
- [ ] Contract address saved in `.env` file
- [ ] Treasury wallet address saved in `.env` file
- [ ] USDC contract address saved in `.env` file
- [ ] `arc_service.py` updated with real implementation
- [ ] Backend connects to Arc Testnet RPC
- [ ] `/v1/shop` endpoint returns savings quote
- [ ] `/v1/save` endpoint processes payment
- [ ] Unit tests pass for `arc_service.py`
- [ ] Manual API tests work
- [ ] Frontend can trigger payment flow
- [ ] Transaction appears on Arc Testnet block explorer
- [ ] Treasury wallet receives USDC

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Arc Testnet"

**Cause**: RPC URL incorrect or network down
**Solution**:
- Verify Arc Testnet RPC URL in official docs
- Try alternative RPC endpoints
- Check network status

### Error: "Insufficient funds for gas"

**Cause**: Deployer wallet doesn't have testnet ETH
**Solution**:
- Use Arc Testnet faucet to get testnet ETH
- Ensure wallet is funded before deployment

### Error: "ERC20: insufficient allowance"

**Cause**: User hasn't approved contract to spend USDC
**Solution**:
- Frontend must call USDC.approve(CONTRACT_ADDRESS, amount) first
- Add 2-step transaction flow: approve → payFee

### Error: "CONTRACT_ADDRESS not configured"

**Cause**: `.env` file not loaded or missing values
**Solution**:
- Ensure `.env` file exists in project root
- Verify `python-dotenv` is installed
- Add `load_dotenv()` to `arc_service.py`

---

## 📚 Resources

- **Arc Testnet Documentation**: [Check official Arc docs]
- **Arbitrum Testnet Info**: https://developer.arbitrum.io/
- **Hardhat Documentation**: https://hardhat.org/docs
- **Remix IDE**: https://remix.ethereum.org/
- **Web3.py Documentation**: https://web3py.readthedocs.io/
- **ERC20 Standard**: https://eips.ethereum.org/EIPS/eip-20

---

## 🔐 Security Considerations

1. **Private Keys**:
   - Never commit private keys to Git
   - Use environment variables for all secrets
   - Consider hardware wallets for production treasury

2. **Contract Security**:
   - Consider audit for production deployment
   - Test on testnet extensively before mainnet
   - Implement emergency pause mechanism for production

3. **API Security**:
   - Add rate limiting to prevent abuse
   - Validate all wallet addresses
   - Log all payment transactions
   - Monitor for suspicious activity

---

## 📞 Support

If you encounter issues during deployment:

1. Check this document's troubleshooting section
2. Review Arc Testnet documentation
3. Test with Remix IDE first (simplest deployment method)
4. Verify all prerequisites are met
5. Check backend logs for detailed error messages

---

## 📊 Success Criteria

Deployment is considered **COMPLETE** when:

✅ Smart contract deployed and verified on Arc Testnet
✅ All addresses updated in `.env` and `arc_service.py`
✅ Backend can connect to Arc Testnet
✅ Payment flow works end-to-end (frontend → backend → blockchain)
✅ Treasury wallet receives test USDC payments
✅ Tests pass for `arc_service.py`
✅ Documentation updated with actual addresses (for demo purposes only)

---

**Last Updated**: 2025-11-05
**Document Version**: 1.0
**Status**: 🔴 Awaiting Implementation
