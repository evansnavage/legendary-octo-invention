import pytest
from src.dbaccess import *

def test_create_product(): 
    assert create_product("test", 10, 10, "test", "test") == {"name": "test", "quantity": 10, "price": 10, "description": "test", "category": "test"}
    print("create_product PASSED")
    print(get_all_products())