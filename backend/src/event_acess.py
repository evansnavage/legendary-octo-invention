from typing import Collection, Optional
import pymongo
import sys
import bson
import os

from .dbEnvironmentVariable import setEnvironmentVariables

setEnvironmentVariables()

try:
    client = pymongo.MongoClient(os.getenv("MONGODB_URI", ""))
    
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)
    
db = client.inventory

test_events = db["test_events"]

test_event_documents = [
    {
        "name": "test",
        "date": "2021-01-01",
        "time": "12:00",
        "people": 10,
        "description": "test",
        "tags": ["test"],
        "kits": []
    },
    {
        "name": "test2",
        "date": "2021-12-01",
        "time": "12:00",
        "people": 10,
        "description": "test",
        "tags": ["test"],
        "kits": []
    }
]

try:
        test_events.drop()
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are your username and password correct in your connection string?")
        sys.exit(1)

try:
        result = test_events.insert_many(test_event_documents)
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
else:
        inserted_count = len(result.inserted_ids)
        print("Inserted %x documents for test setup." %(inserted_count))
        print ("\n")
        
events = db["events"]

event_documents_default = [
    {
        "name": "test",
        "date": "2025-01-01",
        "time": "12:00",
        "people": 10,
        "description": "test",
        "tags": ["test"],
        "kits": []
    },
    {
        "name": "test2",
        "date": "2025-02-24",
        "time": "12:00",
        "people": 10,
        "description": "test",
        "tags": ["test"],
        "kits": []
    }
]

try:
        events.insert_many(event_documents_default)
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
else:
        inserted_count = len(result.inserted_ids)
        print("Inserted %x documents for operation setup." %(inserted_count))
        print ("\n")
        print ("Database prepared.")
        
### CRUD OPERATIONS ###
def set_active_database(testing: bool = False):
    """Sets the active database to either the test database or the production database

    Args:
        testing (bool, optional): If True, sets the active database to the test database. Defaults to False.
    """
    global events
    if testing:
        events = db["test_events"]
    else:
        events = db["events"]

# Set the default active database to production
set_active_database(testing=False)

def drop_all_events():
    """Drops all events from the active database
    """
    events.drop()
    
def get_all_events() -> Collection:
    """Returns all events from the active database

    Returns:
        Collection: Collection of all events
    """
    return list(events.find())

def get_events_by_name(name: str) -> Collection:
    """Returns all events with the given name from the active database

    Args:
        name (str): Name of the event
    Returns:
        Collection: Collection of all events with the given name
    """
    return list(events.find({"name": name}))

def get_event_by_name(name: str) -> Optional[any]:
    """Returns the first event with the given name from the active database

    Args:
        name (str): Name of the event
    Returns:
        Optional[any]: Event with the given name
    """
    return events.find_one({"name": name})

def get_id_from_name(name: str) -> Optional[any]:
    """Returns the ID of the event with the given name from the active database

    Args:
        name (str): Name of the event
    Returns:
        Optional[any]: ID of the event with the given name
    """
    return events.find_one({"name": name})["_id"]

def get_event_by_id(id: str) -> Optional[any]:
    """Returns the event with the given ID from the active database

    Args:
        id (str): ID of the event
    Returns:
        Optional[any]: Event with the given ID
    """
    return events.find_one({"_id": bson.ObjectId(id)})

def update_event(name: str, date: str = None, time: str = None, people: int = None, description: str = None, tags: list = None, kits: list = None) -> Optional[any]:
    """Updates the event with the given name in the active database

    Args:
        name (str): Name of the event
        date (str, optional): Date of the event. Defaults to None.
        time (str, optional): Time of the event. Defaults to None.
        people (int, optional): Number of people at the event. Defaults to None.
        description (str, optional): Description of the event. Defaults to None.
        tags (list, optional): Tags for the event. Defaults to None.
        kits (list, optional): Kits for the event. Defaults to None.
    Returns:
        Optional[any]: Updated event
    """
    update_fields = {}
    if date is not None:
        update_fields["date"] = date
    if time is not None:
        update_fields["time"] = time
    if people is not None:
        update_fields["people"] = people
    if description is not None:
        update_fields["description"] = description
    if tags is not None:
        update_fields["tags"] = tags
    if kits is not None:
        update_fields["kits"] = kits

    if update_fields:
        events.update_one({"name": name}, {"$set": update_fields})
    
    return get_event_by_name(name)

def add_tags(name: str, tags: list[str]) -> Optional[any]:
    """Adds tags to the event with the given name in the active database

    Args:
        name (str): Name of the event
        tags (list[str]): Tags to add to the event
    Returns:
        Optional[any]: Updated event
    """
    for tag in tags:
            events.update_one({"name": name}, {"$push": {"tags": tag}})
    return events.find_one({"name": name})

def remove_tags(name: str, tags: list[str]) -> Optional[any]:
    """Removes tags from the event with the given name in the active database

    Args:
        name (str): Name of the event
        tags (list[str]): Tags to remove from the event
    Returns:
        Optional[any]: Updated event
    """
    for tag in tags:
            events.update_one({"name": name}, {"$pull": {"tags": tag}})
    return events.find_one({"name": name})

def delete_event_by_name(name: str):
    """Deletes the event with the given name from the active database

    Args:
        name (str): Name of the event
    """
    events.delete_one({"name": name})

def delete_event_by_id(id: str):
    """Deletes the event with the given ID from the active database

    Args:
        id (str): ID of the event
    """
    events.delete_one({"_id": bson.ObjectId(id)})
    
def create_event(name: str, date: str, time: str, people: int = 0, description: str = "", tags: list[str] = None, kits: list[str] = None) -> Optional[any]:
    """Creates an event with the given information in the active database

    Args:
        name (str): Name of the event
        date (str): Date of the event
        time (str): Time of the event
        people (int, optional): Number of people at the event. Defaults to 0.
        description (str, optional): Description of the event. Defaults to "".
        tags (list[str], optional): Tags for the event. Defaults to None.
        kits (list[str], optional): Kits for the event. Defaults to None.
    Returns:
        Optional[any]: Created event
    """
    event = {
        "name": name,
        "date": date,
        "time": time,
        "people": people,
        "description": description,
        "tags": tags if tags is not None else [],
        "kits": kits if kits is not None else []
    }
    events.insert_one(event)
    return get_event_by_name(name)

def get_people(name: str) -> int:
    """Returns the number of people at the event with the given name from the active database

    Args:
        name (str): Name of the event
    Returns:
        int: Number of people at the event
    """
    return events.find_one({"name": name})["people"]

def get_date(name: str) -> str:
    """Returns the date of the event with the given name from the active database

    Args:
        name (str): Name of the event
    Returns:
        str: Date of the event
    """
    return events.find_one({"name": name})["date"]

def get_events_on_date(date: str) -> Collection:
    """Returns all events on the given date from the active database

    Args:
        date (str): Date of the events
    Returns:
        Collection: Collection of all events on the given date
    """
    return list(events.find({"date": date}))

def get_events_on_date_range(start_date: str, end_date: str) -> Collection:
    """Returns all events in the given date range from the active database

    Args:
        start_date (str): Start date of the range (inclusive)
        end_date (str): End date of the range (inclusive)
    Returns:
        Collection: Collection of all events in the given date range
    """
    return list(events.find({"date": {"$gte": start_date, "$lte": end_date}}))

def get_events_with_tag(tag: str) -> Collection:
    """Returns all events with the given tag from the active database

    Args:
        tag (str): Tag to search for
    Returns:
        Collection: Collection of all events with the given tag
    """
    return list(events.find({"tags": tag}))

def get_events_with_tags(tags: list[str]) -> Collection:
    """Returns all events with the given tags from the active database

    Args:
        tags (list[str]): Tags to search for
    Returns:
        Collection: Collection of all events with the given tags
    """
    return list(events.find({"tags": {"$all": tags}}))