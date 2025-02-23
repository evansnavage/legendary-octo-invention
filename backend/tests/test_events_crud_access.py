import unittest

from backend.src.event_access import *

class TestEventCRUDOperations(unittest.TestCase):
    def setUp(self):
        set_active_database(testing=True)
        drop_all_events()
        event_test_documents = [
            { "name": "Dog painting event", "date": "2021-10-10", "time": "12:00", "description": "Painting event for dogs", "tags": ["Paint"], "kits": [], "people": 10},
            { "name": "Turtle painting event", "date": "2021-10-11", "time": "12:00", "description": "Painting event for turtles", "tags": ["Paint"], "kits": [], "people": 5},
            { "name": "Sculpting event", "date": "2021-10-12", "time": "12:00", "description": "Sculpting event with clay", "tags": ["Clay"], "kits": [], "people": 15},
            { "name": "Oil painting event", "date": "2021-10-13", "time": "12:00", "description": "Painting event with oil", "tags": ["Paint","Oil"], "kits": [], "people": 20}
        ]
        
        insert_many_events(event_test_documents)
        super().setUp()
    def test_create_event(self):
        drop_all_events()
        self.assertIsNotNone(create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], []))
    def test_get_all_events_initially_empty(self):
        drop_all_events()
        self.assertEqual(get_all_events(), [])
    def test_create_and_get_event(self):
        drop_all_events()
        create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], [])
        events = get_all_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['name'], "test name")
    def test_get_event_by_name(self):
        drop_all_events()
        create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], [])
        event = get_event_by_name("test name")
        self.assertIsNotNone(event)
        self.assertEqual(event['name'], "test name")
    def test_get_id_from_name(self):
        drop_all_events()
        create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], [])
        event_id = get_id_from_name("test name")
        self.assertIsNotNone(event_id)
    def test_update_event_people(self):
        drop_all_events()
        create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], [])
        update_event("test name", people=10)
        event = get_event_by_name("test name")
        self.assertEqual(event['people'], 10)
    def test_get_events_between(self):
        drop_all_events()
        create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], [])
        create_event("test name 2", "2021-10-11", "12:00", 0, "test description", ["test tags"], [])
        create_event("test name 3", "2021-10-12", "12:00", 0, "test description", ["test tags"], [])
        events = get_events_in_date_range("2021-10-10", "2021-10-12")
        self.assertEqual(len(events), 3)
    def test_delete_event_by_name(self):
        drop_all_events()
        create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], [])
        delete_event_by_name("test name")
        self.assertEqual(get_all_events(), [])
    def test_add_kits_to_event(self):
        drop_all_events()
        ka.set_active_database(testing=True)
        ka.create_kit("test kit", 0, [], 0.0, "test description", ["test tags"])
        create_event("test name", "2021-10-10", "12:00", 0, "test description", ["test tags"], [])
        update_event("test name", kits=["test kit"])
        event = get_event_by_name("test name")
        self.assertIsNotNone(event['kits'])