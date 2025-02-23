import unittest
import backend.src.item_access as item_access
from backend.src.kit_access import *

class TestCRUDOperations(unittest.TestCase):

    def setUp(self):
        set_active_database(testing=True)
        drop_all_kits()
        kit_test_documents = [
            { "name": "Dog painting kit", "quantity": 10, "items": [{ "name": "Green Paint", "price": 3.99, "quantity": 10, "description": "Paint that is green", "tag": ["paint"], "distributor": "Sherwin Williams" }],"cost": 0.0,"description": "kit for painting dogs", "tags": ["Paint"]},
            { "name": "Turtle painting kit", "quantity": 8, "items": [],"description": "kit for painting turtles", "tags": ["Paint"]},
            { "name": "Sculpting Kit", "quantity": 4, "items": [],"cost": 0.0,"description": "kit for sculpting with clay", "tags": ["Clay"]},
            { "name": "Oil painting kit", "quantity": 6, "items": [],"cost": 0.0,"description": "kit for painting dogs", "tags": ["Paint","Oil"]}
        ]
        insert_many_kits(kit_test_documents)
        super().setUp()

    def test_create_kit(self):
        drop_all_kits()
        self.assertIsNotNone(create_kit("test name", 8, [], 0.0, "test description", ["test tags"]))

    def test_get_all_kits_initially_empty(self):
        drop_all_kits()
        self.assertEqual(get_all_kits(), [])

    def test_create_and_get_kit(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        kits = get_all_kits()
        self.assertEqual(len(kits), 1)
        self.assertEqual(kits[0]['name'], "test name")

    def test_get_kit_by_name(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        kit = get_kit_by_name("test name")
        self.assertIsNotNone(kit)
        self.assertEqual(kit['name'], "test name")

    def test_get_id_from_name(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        kit_id = get_id_from_name("test name")
        self.assertIsNotNone(kit_id)

    def test_update_kit_quantity(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        update_kit_quantity("test name", 10)
        kit = get_kit_by_name("test name")
        self.assertEqual(kit['quantity'], 10)

    def test_calculate_kit_total_price(self):
        drop_all_kits()
        item_access.set_active_database(testing=True)
        item_access.create_item("Green Paint", 10, 3.99,"Gallon bucket of paint", ["paint"])
        create_kit("test name", 8, ["Green Paint"], 0.0, "test description", ["test tags"])
        price = calculate_kit_total_price("test name")
        self.assertEqual(price, 3.99)  # Assuming Green Paint price is 3.99 for this test

    def test_update_item_description(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        update_item_description("test name", "updated description")
        kit = get_kit_by_name("test name")
        self.assertEqual(kit['description'], "updated description")

    def test_add_and_remove_tags(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        add_tags("test name", ["new_tag"])
        kit = get_kit_by_name("test name")
        self.assertIn("new_tag", kit['tags'])
        
        remove_tags("test name", ["new_tag"])
        kit = get_kit_by_name("test name")
        self.assertNotIn("new_tag", kit['tags'])

    def test_delete_kit_by_name(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        delete_kit_by_name("test name")
        kits = get_all_kits()
        self.assertEqual(len(kits), 0)

    def test_delete_kit_by_id(self):
        drop_all_kits()
        create_kit("test name", 8, [], 0.0, "test description", ["test tags"])
        kit_id = get_id_from_name("test name")
        delete_kit_by_id(kit_id)
        kits = get_all_kits()
        self.assertEqual(len(kits), 0)

if __name__ == '__main__':
    unittest.main()
