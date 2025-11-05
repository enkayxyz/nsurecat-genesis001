from circle.web3 import developer_controlled_wallets
from app.client import get_circle_client

def transfer_tokens(source_wallet_id: str, destination_wallet_id: str, amount: str, token_address: str):
    client = get_circle_client()
    api_instance = developer_controlled_wallets.TransactionsApi(client)
    # create an api instance

    try:
        request = developer_controlled_wallets.CreateTransferTransactionForDeveloperRequest.from_dict({
            "walletId": source_wallet_id,
            "tokenId": token_address,
            "destinationAddress": destination_wallet_id,
            "amounts": [amount],
            "feeLevel": 'LOW',
        })
        response = api_instance.create_developer_transaction_transfer(request)
        print(response)
    except developer_controlled_wallets.ApiException as e:
        print("Exception when calling TransactionsApi->create_developer_transaction_transfer: %s\n" % e)

   