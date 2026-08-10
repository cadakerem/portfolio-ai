import pytest
from core.finance import is_fund_code, is_stock_code

def test_is_fund_code():
    assert is_fund_code("YAY") == True
    assert is_fund_code("MAC") == True
    assert is_fund_code("TI3") == True
    assert is_fund_code("AAPL") == False
    assert is_fund_code("THYAO.IS") == False
    assert is_fund_code("123") == False

def test_is_stock_code():
    assert is_stock_code("AAPL") == True
    assert is_stock_code("THYAO.IS") == True
    assert is_stock_code("MSFT") == True
    assert is_stock_code("YAY") == False
    assert is_stock_code("MAC") == False
