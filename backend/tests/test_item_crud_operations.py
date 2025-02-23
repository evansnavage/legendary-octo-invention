import unittest

from backend.src.item_access import *

class TestItemCRUDOperations(unittest.TestCase):
    
    def setUp(self):
        set_active_database(testing=True)
        drop_all_items()
        item_test_documents = [{ "name": "Green Paint", "price": 3.99, "quantity": 10, "description": "Paint that is green", "tags": ["paint"], "distributor": "Sherwin Williams" },
                    { "name": "Blue Paint", "price": 3.99, "quantity": 10, "description": "Paint that is blue", "tags": ["paint", "favorite"], "distributor": "Sherwin Williams" },
                    { "name": "Red Paint", "price": 3.99, "quantity": 10 },
                    { "name": "Yellow Paint", "price": 3.99, "quantity": 10 }]
        
        insert_many_items(item_test_documents)
        super().setUp()
    
    def test_create_item(self): 
        drop_all_items()
        self.assertIsNotNone(create_item("test", 10.0, 10, "test", ["test"]))

    def test_get_all_items_initially_empty(self):
        drop_all_items()
        self.assertEqual(get_all_items(), [])

    def test_create_and_get_item(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        items = get_all_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], "test")

    def test_get_items_by_name(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        items = get_items_by_name("test")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], "test")

    def test_get_id_from_name(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        item_id = get_id_from_name("test")
        self.assertIsNotNone(item_id)

    def test_get_item_by_id(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        item_id = get_id_from_name("test")
        item = get_item_by_id(item_id)
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], "test")
    
    def test_update_item_price(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        update_item_price("test", 20)
        item = get_items_by_name("test")[0]
        self.assertEqual(item['price'], 20)
    
    def test_update_item_description(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        update_item_description("test", "test2")
        item = get_items_by_name("test")[0]
        self.assertEqual(item['description'], "test2")
    
    def test_add_tags(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        add_tags("test", ["test2", "test3", "test4"])
        item = get_items_by_name("test")[0]
        self.assertEqual(item['tags'], ["test2", "test3", "test4"])
    
    def test_remove_tags(self):
        drop_all_items()
        create_item("test", 10, 10, "test", ["test", "test2", "test3", "test4"])
        remove_tags("test", ["test"])
        item = get_items_by_name("test")[0]
        self.assertEqual(item['tags'], ["test2", "test3", "test4"])
    
    def test_delete_item_by_name(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        delete_item_by_name("test")
        self.assertEqual(get_all_items(), [])
    
    def test_delete_item_by_id(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        item_id = get_id_from_name("test")
        delete_item_by_id(item_id)
        self.assertEqual(get_all_items(), [])
        
    def test_update_distributor(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        update_item_distributor("test", "test")
        item = get_items_by_name("test")[0]
        self.assertEqual(item['distributor'], "test")
        
    def test_update_item_quantity(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        update_item_quantity("test", 20)
        item = get_items_by_name("test")[0]
        self.assertEqual(item['quantity'], 20)
    
    def test_get_items_by_tag(self):
        drop_all_items()
        create_item("test", 10, 10, "test", ["test", "test2", "test3"])
        create_item("test2", 10, 10, "test", ["test", "test2", "test3"])
        create_item("test3", 10, 10, "test", ["test", "test2", "test3"])
        items = get_items_by_tag("test")
        self.assertEqual(len(items), 3)
    
    def test_get_item_price(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        price = get_item_price("test")
        self.assertEqual(price, 10)
    
    def test_get_item_quantity(self):
        drop_all_items()
        create_item("test", 10, 10, "test")
        quantity = get_item_quantity("test")
        self.assertEqual(quantity, 10)
        
if __name__ == '__main__':
    unittest.main()
