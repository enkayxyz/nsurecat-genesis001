from circle.web3 import developer_controlled_wallets
from app.client import get_circle_client

def create_wallet_set(name: str):
    client = get_circle_client()
    api_instance = developer_controlled_wallets.WalletSetsApi(client)

    request = developer_controlled_wallets.CreateWalletSetRequest.from_dict({
        "name": name
    })

    try:
        response = api_instance.create_wallet_set(request)
        return response.to_dict()
    except developer_controlled_wallets.ApiException as e:
        return {"error": str(e)}
