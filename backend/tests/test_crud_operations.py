import unittest

from backend.src.dbaccess import *

class TestCRUDOperations(unittest.TestCase):
    
    def setUp(self):
        set_active_database(testing=True)
        drop_all_products()
        product_test_documents = [{ "name": "Green Paint", "price": 3.99, "quantity": 10, "description": "Paint that is green", "category": "Paint", "distributor": "Sherwin Williams" },
                    { "name": "Blue Paint", "price": 3.99, "quantity": 10 },
                    { "name": "Red Paint", "price": 3.99, "quantity": 10 },
                    { "name": "Yellow Paint", "price": 3.99, "quantity": 10 }]
        
        insert_many_products(product_test_documents)
        super().setUp()
    
    def test_create_product(self): 
        drop_all_products()
        self.assertIsNotNone(create_product("test", 10, 10, "test", "test"))

    def test_get_all_products_initially_empty(self):
        drop_all_products()
        self.assertEqual(get_all_products(), [])

    def test_create_and_get_product(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        products = get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['name'], "test")

    def test_get_products_by_name(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        products = get_products_by_name("test")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['name'], "test")

    def test_get_id_from_name(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        product_id = get_id_from_name("test")
        self.assertIsNotNone(product_id)

    def test_get_product_by_id(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        product_id = get_id_from_name("test")
        product = get_product_by_id(product_id)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "test")
    
    def test_update_product_price(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        update_product_price("test", 20)
        product = get_products_by_name("test")[0]
        self.assertEqual(product['price'], 20)
    
    def test_update_product_description(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        update_product_description("test", "test2")
        product = get_products_by_name("test")[0]
        self.assertEqual(product['description'], "test2")
    
    def test_update_product_category(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        update_product_category("test", "test2")
        product = get_products_by_name("test")[0]
        self.assertEqual(product['category'], "test2")
    
    def test_delete_product_by_name(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        delete_product_by_name("test")
        self.assertEqual(get_all_products(), [])
    
    def test_delete_product_by_id(self):
        drop_all_products()
        create_product("test", 10, 10, "test", "test")
        product_id = get_id_from_name("test")
        delete_product_by_id(product_id)
        self.assertEqual(get_all_products(), [])
        
if __name__ == '__main__':
    unittest.main()
