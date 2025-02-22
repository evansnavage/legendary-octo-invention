from typing import Collection, Optional
import pymongo
import sys
import bson
import os
from backend import dbEnvironmentVariable

### CONNECT AND TEST CONNECTION ###

dbEnvironmentVariable.setEnvironmentVariables()

try:
    client = pymongo.MongoClient(os.getenv("MONGODB_URI", ""))
    
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)
    
db = client.inventory

test_items = db["items"]

item_test_documents = [{ "name": "Green Paint", "price": 3.99, "quantity": 10, "description": "Paint that is green", "tag": ["paint"], "distributor": "Sherwin Williams" },
                    { "name": "Blue Paint", "price": 3.99, "quantity": 10 },
                    { "name": "Red Paint", "price": 3.99, "quantity": 10 },
                    { "name": "Yellow Paint", "price": 3.99, "quantity": 10 }]

try:
        test_items.drop()
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are your username and password correct in your connection string?")
        sys.exit(1)

try:
        result = test_items.insert_many(item_test_documents)
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
else:
        inserted_count = len(result.inserted_ids)
        print("Inserted %x documents for test setup." %(inserted_count))
        print ("\n")

### END OF TEST OPERATIONS ###

### Basic Operation Setup ###
items = db["items"]
item_documents_default = [{ "name": "Green Paint", "price": 3.99, "quantity": 10, "description": "Paint that is green", "category": "Paint", "distributor": "Sherwin Williams" }]
try:
        items.insert_many(item_documents_default)
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
    global items
    if testing:
        items = db["test_items"]
    else:
        items = db["items"]

# Set the default active database to production
set_active_database(testing=False)
def drop_all_items():
        """Drops all items from the database
        """
        items.drop()

def get_all_items() -> Collection:
        """Returns all items

        Returns:
                Collection: A collection of all items
        """
        curser = items.find({}, {"_id": 0})
        return [doc for doc in curser]
def get_items_by_name(name: str) -> Collection:
        """Returns all items with the given name

        Args:
                name (str): The name of the items to find

        Returns:
                Collection: documents with the given name
        """
        data = items.find({"name": name}, {"_id": 0})
        return [doc for doc in data]

def get_item_by_id(id: str) -> Optional[any]:
        """Returns the item with the id

        Args:
                id (string): The id of the item to find

        Returns:
                Optional[any]: The bson object of the item or None if not found
        """
        return items.find_one({"_id": bson.ObjectId(id)})

def get_first_item_by_name(name:str ) -> Optional[any]:
        """Returns the first item with the given name

        Args:
                name (str): Name of the item to find

        Returns:
                Optional[any]: the bson object of the item or None if not found
        """
        return items.find_one({"name": name})

def update_item_quantity(name: str, quantity: float) -> Optional[any]: 
        """Updates the quantity of the item with the given name
        Will update all items with the given name

        Args:
                name (str): the name of the item to update
                quantity (int): the new quantity of the item

        Returns:
                Optional[any]: the first updated item or None if not found
        """
        items.update_one({"name": name}, {"$set": {"quantity": quantity}})
        return items.find_one({"name": name})

def update_item_price(name: str, price: float) -> Optional[any]:
        """Updates the price of the item with the given name
        Will update all items with the given name

        Args:
                name (str): the name of the item to update
                price (float): the new price of the item

        Returns:
                Optional[any]: the first updated item or None if not found
        """
        items.update_one({"name": name}, {"$set": {"price": price}})
        return items.find_one({"name": name})

def update_item_description(name: str, description: str) -> Optional[any]:
        """Updates the description of the item with the given name
        Will update all items with the given name

        Args:
                name (str): the name of the item to update
                description (str): the new description of the item

        Returns:
                Optional[any]: the first updated item or None if not found
        """
        items.update_one({"name": name}, {"$set": {"description": description}})
        return items.find_one({"name": name})

def add_tags(name: str, tags: list[str]) -> Optional[any]: 
       """Adds the tags to the item with the given name

        Args: 
                name(str): the name of the item to update
                tags(list[str]): the list of tags to add to item

        Return:
                Optional[any}: item updated or none if not found
       
       """
       for tag in tags:
            items.update_one({"name": name}, {"$push": {"tag": tag}})
       return items.find_one({"name": name})

def remove_tags(name: str, tags: list[str]) -> None:
    """Removes the tags of the item with the given name 

    Args:
        name (str): the name of the item to update
        tags (list[str]): the list of tags to remove from item
    """
    for tag in tags:
        items.update_one({"name": name}, {"$pull": {"tag": tag}})


def create_item(name: str, quantity: float, price: float = 0.0, description: str = "", category: str = "") -> Optional[any]:
        """Creates a new item

        Args:
                name (str): the name of the item
                quantity (float): the quantity of the item
                price (float, optional): the price of the item. Defaults to 0.0.
                description (str, optional): the description of the item. Defaults to "".
                category (str, optional): the category of the item. Defaults to "".

        Returns:
                Optional[any]: the created item or None if failed
        """
        items.insert_one({"name": name, "price": price, "quantity": quantity, "description": description, "category": category})
        return items.find_one({"name": name})
    
def get_id_from_name(name: str) -> str:
        """Returns the id of the item with the given name

        Args:
                name (str): the name of the item to find

        Returns:
                str: the id of the item
        """
        return items.find_one({"name": name}, {"_id": 1})["_id"]
    
def delete_item_by_name(name: str) -> None:
        """Deletes the item with the given name

        Args:
                name (str): the name of the item to delete
        """
        items.delete_one({"name": name})

def delete_item_by_id(id: str) -> None:
        """Deletes the item with the given id
        
        Args:
                id (str): the id of the item to delete
        """
        items.delete_one({"_id": bson.ObjectId(id)})

def insert_many_items(item_documents: Collection) -> int:
        """Inserts many items into the database

        Args:
                item_documents (Collection): the documents to insert

        Returns:
                int: the number of documents inserted
        """
        result = items.insert_many(item_documents)
        return len(result.inserted_ids)