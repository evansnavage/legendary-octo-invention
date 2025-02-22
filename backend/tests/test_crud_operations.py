import unittest

from backend.src.dbaccess import *

class TestCRUDOperations(unittest.TestCase):
    def test_create_product(self): 
        drop_all_products()
        assert create_product("test", 10, 10, "test", "test") != None
        print("create_product PASSED")

    def test_get_all_products_initially_empty(self):
        drop_all_products()
        assert get_all_products() == []
        print("test_get_all_products_initially_empty PASSED")

    def test_create_and_get_product(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        products = get_all_products()
        assert len(products) == 1
        assert products[0]['name'] == "test"
        print("test_create_and_get_product PASSED")

    def test_get_products_by_name(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        products = get_products_by_name("test")
        assert len(products) == 1
        assert products[0]['name'] == "test"
        print("test_get_products_by_name PASSED")

    def test_get_id_from_name(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        product_id = get_id_from_name("test")
        assert product_id is not None
        print("test_get_id_from_name PASSED")

    def test_get_product_by_id(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        product_id = get_id_from_name("test")
        product = get_product_by_id(product_id)
        assert product is not None
        assert product['name'] == "test"
        print("test_get_product_by_id PASSED")
    
    def test_update_product_price(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        update_product_price("test", 20)
        product = get_products_by_name("test")[0]
        assert product['price'] == 20
        print("test_update_product_price PASSED")
    
    def test_update_product_description(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        update_product_description("test", "test2")
        product = get_products_by_name("test")[0]
        assert product['description'] == "test2"
        print("test_update_product_description PASSED")
    
    def test_update_product_category(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        update_product_category("test", "test2")
        product = get_products_by_name("test")[0]
        assert product['category'] == "test2"
        print("test_update_product_category PASSED")
    
    def test_delete_product_by_name(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        delete_product_by_name("test")
        assert get_all_products() == []
        print("test_delete_product_by_name PASSED")
    
    def test_delete_product_by_id(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        product_id = get_id_from_name("test")
        delete_product_by_id(product_id)
        assert get_all_products() == []
        print("test_delete_product PASSED")
        
if __name__ == '__main__':
    unittest.main()