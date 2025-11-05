import pytest
from agent.mock_shopper import find_savings

def test_find_savings():
    data = {"key": "value"}
    result = find_savings(data)
    assert "savings_6mo" in result
    assert result["savings_6mo"] == 246.00
    assert result["new_carrier"] == "Rebel Mutual"