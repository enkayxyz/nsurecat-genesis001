from circle.web3 import developer_controlled_wallets
from backend.app.client import get_circle_client

def transaction_status(transaction_id: str):
    client = get_circle_client()
    api_instance = developer_controlled_wallets.TransactionsApi(client)
    try:
        response = api_instance.get_transaction(id=transaction_id)
        print(response)
    except developer_controlled_wallets.ApiException as e:
        print("Exception when calling TransactionsApi->get_transaction: %s\n" % e)
