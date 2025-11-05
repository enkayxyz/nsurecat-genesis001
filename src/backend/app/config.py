import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TEST_API_KEY = os.getenv("TEST_API_KEY")
    ENTITY_SECRET = os.getenv("ENTITY_SECRET")
    WALLET_SET_ID = os.getenv("WALLET_SET_ID")
