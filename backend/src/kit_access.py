from typing import Collection, Optional
import pymongo
import sys
import bson
import os
import backend.src.item_access as item_access
from .dbEnvironmentVariable import setEnvironmentVariables

### CONNECT AND TEST CONNECTION ###

setEnvironmentVariables()

try:
    client = pymongo.MongoClient(os.getenv("MONGODB_URI", ""))
    
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)
    
db = client.inventory

test_kits = db["test_kits"]

# kit_documents_default = [{ "name": "Dog painting kit", "quantity": 10, "items": [],"cost": 0.0,"description": "kit for painting dogs", "tags": ["Paint"]}]

kit_test_documents = [{ "name": "Dog painting kit", "quantity": 10, "items": [],"cost": 0.0,"description": "kit for painting dogs", "tags": ["Paint"]},
                      { "name": "Turtle painting kit", "quantity": 8, "items": [],"description": "kit for painting turtles", "tags": ["Paint"]},
                      { "name": "Sculpting Kit", "quantity": 4, "items": [],"cost": 0.0,"description": "kit for sculpting with clay", "tags": ["Clay"]},
                      { "name": "Oil painting kit", "quantity": 6, "items": [],"cost": 0.0,"description": "kit for painting dogs", "tags": ["Paint","Oil"]}]


try:
        test_kits.drop()
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are your username and password correct in your connection string?")
        sys.exit(1)

try:
        result = test_kits.insert_many(kit_test_documents)
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
else:
        inserted_count = len(result.inserted_ids)
        print("Inserted %x documents for test setup." %(inserted_count))
        print ("\n")

### END OF TEST OPERATIONS ###

### Basic Operation Setup ###
kits = db["kits"]
kit_documents_default = [{ "name": "Dog painting kit", "quantity": 10, "items": [],"cost": 0.0,"description": "kit for painting dogs", "tags": ["Paint"]}]
try:
        kits.insert_many(kit_documents_default)
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
        items = db["test_kits"]
    else:
        items = db["kits"]


# Set the default active database to production
set_active_database(testing=False)
def drop_all_kits():
        """Drops all kits from the database
        """
        kits.drop()


def get_all_kits() -> Collection:
        """Returns all kits

        Returns:
                Collection: A collection of all kits
        """
        cursor = kits.find({}, {"_id": 0})
        return [doc for doc in cursor]

def get_kit_by_id(id: str) -> Optional[any]:
        """Returns the kit with the id

        Args:
                id (string): The id of the kit to find

        Returns:
                Optional[any]: The bson object of the kit or None if not found
        """
        return kits.find_one({"_id": bson.ObjectId(id)})


def get_kit_by_name(name:str ) -> Optional[any]:
        """Returns the first kit with the given name

        Args:
                name (str): Name of the Kit to find

        Returns:
                Optional[any]: the bson object of the kit or None if not found
        """
        return kits.find_one({"name": name})

def update_kit_quantity(name: str, quantity: float) -> Optional[any]: 
        """Updates the quantity of the kit with the given name
        Will update all kits with the given name

        Args:
                name (str): the name of the kit to update
                quantity (int): the new quantity of the kit

        Returns:
                Optional[any]: the first updated kit or None if not found
        """
        kits.update_one({"name": name}, {"$set": {"quantity": quantity}})
        return kits.find_one({"name": name})


def calculate_kit_total_price(name: str) -> Optional[any]:
    """Calculates the total price of the kit by totaling the price of
       each item in the kit and returning the value 

    Args:
        name (str): name of the kit to calculate the price for

    Returns:
        Optional[any]: _description_
    """

    kit = get_kit_by_name(name)
    
    items = kit['items']

    cost = 0

    for item in items:
           cost += item_access.get_item_price(item["name"])

    return cost

def update_item_description(name: str, description: str) -> Optional[any]:
        """Updates the description of the kit with the given name
        Will update all kits with the given name

        Args:
                name (str): the name of the kit to update
                description (str): the new description of the kit

        Returns:
                Optional[any]: the first updated kit or None if not found
        """
        kits.update_one({"name": name}, {"$set": {"description": description}})
        return kits.find_one({"name": name})


def add_tags(name: str, tags: list[str]) -> Optional[any]: 
       """Adds the tags to the kit with the given name

        Args: 
                name(str): the name of the kit to update
                tags(list[str]): the list of tags to add to kit

        Return:
                Optional[any}: kit updated or none if not found
       
       """
       for tag in tags:
            kits.update_one({"name": name}, {"$push": {"tags": tag}})
       return kits.find_one({"name": name})

def remove_tags(name: str, tags: list[str]) -> None:
    """Removes the tags of the kit with the given name 

    Args:
        name (str): the name of the kit to update
        tags (list[str]): the list of tags to remove from kit
    """
    for tag in tags:
        kits.update_one({"name": name}, {"$pull": {"tags": tag}})


def create_kit(name:str, quantity: int, items: list[str] = [], cost: float = 0.0, description: str = "", tags: list[str] = []) -> Optional[any]:
    """Creates a new kit

    Args:
        name (str): The name of the kit
        quantity (int): The quantity of the kit
        items (list[any], optional): List of items within the kit Defaults to [].
        cost (float, optional): Total cost of the kit based on the items in the kit. Defaults to 0.0.
        description (str, optional): Description of what the kit is/is for. Defaults to "".
        tags (list[str], optional): List of tags on the kit. Defaults to [].

    Returns:
        Optional[any]: the created kit or None if failed
    """

    actual_items = []

    for item in items:
       actual_items.append(item_access.get_first_item_by_name(item))


    kits.insert_one({"name": name, "quantity": quantity, "items": actual_items, "cost": cost, "description": description, "tags": tags})
    return kits.find_one({"name": name})

def get_id_from_name(name: str) -> str:
        """Returns the id of the kit with the given name

        Args:
                name (str): the name of the kit to find

        Returns:
                str: the id of the kit
        """
        return kits.find_one({"name": name}, {"_id": 1})["_id"]

def delete_kit_by_name(name: str) -> None:
        """Deletes the kit with the given name

        Args:
                name (str): the name of the kit to delete
        """
        kits.delete_one({"name": name})

def delete_kit_by_id(id: str) -> None:
        """Deletes the kit with the given id
        
        Args:
                id (str): the id of the kit to delete
        """
        kits.delete_one({"_id": bson.ObjectId(id)})

def insert_many_kits(kit_documents: Collection) -> int:
        """Inserts many kits into the database

        Args:
                item_documents (Collection): the documents to insert

        Returns:
                int: the number of documents inserted
        """
        result = items.insert_many(kit_documents)
        return len(result.inserted_ids)


def get_kits_by_tag(tag: str) -> Collection:
        """Returns all kits with the given tag

        Args:
                tag (str): the tag to search for

        Returns:
                Collection: the kits with the given tag
        """
        data = kits.find({"tags": {"$in": [tag]}}, {"_id": 0})
        return [doc for doc in data]


def get_kit_quantity(name: str) -> int:
        """Returns the quantity of the kit with the given name

        Args:
                name (str): the name of the kit

        Returns:
                float: the quantity of the kit
        """
        return items.find_one({"name": name}, {"quantity": 1})["quantity"]



           




