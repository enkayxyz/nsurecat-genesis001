from circle.web3 import developer_controlled_wallets
from backend.app.client import get_circle_client
from backend.app.config import Config

def create_wallet():
    client = get_circle_client()
    api_instance = developer_controlled_wallets.WalletsApi(client)
    request = developer_controlled_wallets.CreateWalletRequest.from_dict({
        "accountType": "SCA",
        "blockchains": ["ARC-TESTNET"],
        "count": 1,
        "walletSetId": Config.WALLET_SET_ID
    })

    try:
        response = api_instance.create_wallet(create_wallet_request=request)
        return response.to_dict()
    except developer_controlled_wallets.ApiException as e:
        return {"error": str(e)}


def get_wallet_balance(wallet_id: str):
    client = get_circle_client()
    api_instance = developer_controlled_wallets.WalletsApi(client)
    try:
        response = api_instance.list_wallet_balance(id=wallet_id)
        return response.to_dict()
    except developer_controlled_wallets.ApiException as e:
        return {"error": str(e)}
