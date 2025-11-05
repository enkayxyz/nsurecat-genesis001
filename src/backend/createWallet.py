import os
from circle.web3 import developer_controlled_wallets
from circle.web3 import utils
from dotenv import load_dotenv
load_dotenv()

#Step 1: Generate Entity Secret and Entity Secret Ciphertext (only need to run once)
# entity_secret = utils.generate_entity_secret()
# entity_secret_ciphertext = utils.generate_entity_secret_ciphertext(os.getenv("TEST_API_KEY"), os.getenv("ENTITY_SECRET"))
# print(entity_secret_ciphertext)

#Step 2: Initialize the client
client = utils.init_developer_controlled_wallets_client(api_key=os.getenv("TEST_API_KEY"), entity_secret=os.getenv("ENTITY_SECRET"))
try:
  response = client.configuration.get_public_key()
  print(response)
except developer_controlled_wallets.ApiException as e:
  print("Exception when calling configuration->get_public_key: %s" % e)

# Step 3: Create a WalletSet ID (only need to run once)
# api_instance = developer_controlled_wallets.WalletSetsApi(client)

# try:
#     request = developer_controlled_wallets.CreateWalletSetRequest.from_dict({
#         "name": "Entity WalletSet A",
#     })
#     response = api_instance.create_wallet_set(request)
#     print(response)
# except developer_controlled_wallets.ApiException as e:
#     print("Exception when calling WalletSetsApi->create_wallet_set: %s\n" % e)

# Step 4: Create a Wallet using the WalletSet ID from Step 3
api_instance = developer_controlled_wallets.WalletsApi(client)
request = developer_controlled_wallets.CreateWalletRequest.from_dict({
    "accountType": "SCA",
    "blockchains": ["ARC-TESTNET"],
    "count": 1,
    "walletSetId": os.getenv("WALLET_SET_ID"),
})
response = api_instance.create_wallet(create_wallet_request=request)
print(response.json())
