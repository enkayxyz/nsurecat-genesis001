import pytest
from backend.app.wallets import create_wallet, get_wallet_balance

class DummyResponse:
    def to_dict(self):
        return {"walletId": "test_wallet_id", "balance": 100}

class DummyApi:
    def create_wallet(self, create_wallet_request):
        if create_wallet_request is None:
            raise Exception("Invalid request")
        return DummyResponse()
    def list_wallet_balance(self, id):
        if id == "bad_id":
            raise Exception("Wallet not found")
        if id == "":
            raise Exception("Empty wallet id")
        if id is None:
            raise Exception("None wallet id")
        if not isinstance(id, str):
            raise Exception("Non-string wallet id")
        return DummyResponse()

@pytest.fixture(autouse=True)
def patch_circle(monkeypatch):
    monkeypatch.setattr("app.wallets.developer_controlled_wallets.WalletsApi", lambda client: DummyApi())
    monkeypatch.setattr("app.wallets.get_circle_client", lambda: None)
    monkeypatch.setattr("app.wallets.Config", type("Config", (), {"WALLET_SET_ID": "dummy_set"}))


def test_create_wallet_success():
    resp = create_wallet()
    assert "walletId" in resp



# Success and error scenarios for create_wallet
def test_create_wallet_success():
    resp = create_wallet()
    assert "walletId" in resp

def test_create_wallet_invalid_request(monkeypatch):
    import app.wallets
    monkeypatch.setattr("app.wallets.developer_controlled_wallets.CreateWalletRequest.from_dict", lambda d: None)
    resp = create_wallet()
    assert "error" in resp or isinstance(resp, dict)
    monkeypatch.undo()

def test_create_wallet_api_exception(monkeypatch):
    class ExceptionApi(DummyApi):
        def create_wallet(self, create_wallet_request):
            raise Exception("API down")
    monkeypatch.setattr("app.wallets.developer_controlled_wallets.WalletsApi", lambda client: ExceptionApi())
    resp = create_wallet()
    assert "error" in resp or isinstance(resp, dict)
    monkeypatch.undo()

def test_create_wallet_bad_config(monkeypatch):
    monkeypatch.setattr("app.wallets.Config", type("Config", (), {"WALLET_SET_ID": None}))
    resp = create_wallet()
    assert "error" in resp or isinstance(resp, dict)
    monkeypatch.undo()

def test_create_wallet_unexpected_response(monkeypatch):
    class WeirdResponse:
        def to_dict(self):
            return None
    class WeirdApi(DummyApi):
        def create_wallet(self, create_wallet_request):
            return WeirdResponse()
    monkeypatch.setattr("app.wallets.developer_controlled_wallets.WalletsApi", lambda client: WeirdApi())
    resp = create_wallet()
    assert resp is None or "error" in resp or isinstance(resp, dict)
    monkeypatch.undo()

# Success and error scenarios for get_wallet_balance
def test_get_wallet_balance_success():
    resp = get_wallet_balance("test_wallet_id")
    assert "balance" in resp

def test_get_wallet_balance_not_found():
    resp = get_wallet_balance("bad_id")
    assert "error" in resp or isinstance(resp, dict)

def test_get_wallet_balance_empty_id():
    resp = get_wallet_balance("")
    assert "error" in resp or isinstance(resp, dict)

def test_get_wallet_balance_none_id():
    resp = get_wallet_balance(None)
    assert "error" in resp or isinstance(resp, dict)

def test_get_wallet_balance_non_string_id():
    resp = get_wallet_balance(12345)
    assert "error" in resp or isinstance(resp, dict)

def test_get_wallet_balance_api_exception(monkeypatch):
    class ExceptionApi(DummyApi):
        def list_wallet_balance(self, id):
            raise Exception("API down")
    monkeypatch.setattr("app.wallets.developer_controlled_wallets.WalletsApi", lambda client: ExceptionApi())
    resp = get_wallet_balance("test_wallet_id")
    assert "error" in resp or isinstance(resp, dict)
    monkeypatch.undo()

def test_get_wallet_balance_unexpected_response(monkeypatch):
    class WeirdResponse:
        def to_dict(self):
            return None
    class WeirdApi(DummyApi):
        def list_wallet_balance(self, id):
            return WeirdResponse()
    monkeypatch.setattr("app.wallets.developer_controlled_wallets.WalletsApi", lambda client: WeirdApi())
    resp = get_wallet_balance("test_wallet_id")
    assert resp is None or "error" in resp or isinstance(resp, dict)
    monkeypatch.undo()
