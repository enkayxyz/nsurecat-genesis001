from circle.web3 import utils
from backend.app.config import Config

def get_circle_client():
    """
    Initializes and returns a Circle Developer-Controlled Wallet client.
    """
    client = utils.init_developer_controlled_wallets_client(
        api_key=Config.TEST_API_KEY,
        entity_secret=Config.ENTITY_SECRET,
    )
    return client
