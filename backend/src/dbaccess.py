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

test_products = db["products"]

product_test_documents = [{ "name": "Green Paint", "price": 3.99, "quantity": 10, "description": "Paint that is green", "category": "Paint", "distributor": "Sherwin Williams" },
                    { "name": "Blue Paint", "price": 3.99, "quantity": 10 },
                    { "name": "Red Paint", "price": 3.99, "quantity": 10 },
                    { "name": "Yellow Paint", "price": 3.99, "quantity": 10 }]

try:
        test_products.drop()
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are your username and password correct in your connection string?")
        sys.exit(1)

try:
        result = test_products.insert_many(product_test_documents)
except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
else:
        inserted_count = len(result.inserted_ids)
        print("Inserted %x documents for test setup." %(inserted_count))
        print ("\n")

### END OF TEST OPERATIONS ###

### Basic Operation Setup ###
products = db["products"]
product_documents_default = [{ "name": "Green Paint", "price": 3.99, "quantity": 10, "description": "Paint that is green", "category": "Paint", "distributor": "Sherwin Williams" }]
try:
        products.insert_many(product_documents_default)
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
    global products
    if testing:
        products = db["test_products"]
    else:
        products = db["products"]

# Set the default active database to production
set_active_database(testing=False)
def drop_all_products():
        """Drops all products from the database
        """
        products.drop()

def get_all_products() -> Collection:
        """Returns all products

        Returns:
                Collection: A collection of all products
        """
        curser = products.find({}, {"_id": 0})
        return [doc for doc in curser]
def get_products_by_name(name: str) -> Collection:
        """Returns all products with the given name

        Args:
                name (str): The name of the products to find

        Returns:
                Collection: documents with the given name
        """
        data = products.find({"name": name}, {"_id": 0})
        return [doc for doc in data]

def get_product_by_id(id: str) -> Optional[any]:
        """Returns the product with the id

        Args:
                id (string): The id of the product to find

        Returns:
                Optional[any]: The bson object of the product or None if not found
        """
        return products.find_one({"_id": bson.ObjectId(id)})

def get_first_product_by_name(name:str ) -> Optional[any]:
        """Returns the first product with the given name

        Args:
                name (str): Name of the product to find

        Returns:
                Optional[any]: the bson object of the product or None if not found
        """
        return products.find_one({"name": name})

def update_product_quantity(name: str, quantity: float) -> Optional[any]: 
        """Updates the quantity of the product with the given name
        Will update all products with the given name

        Args:
                name (str): the name of the product to update
                quantity (int): the new quantity of the product

        Returns:
                Optional[any]: the first updated product or None if not found
        """
        products.update_one({"name": name}, {"$set": {"quantity": quantity}})
        return products.find_one({"name": name})

def update_product_price(name: str, price: float) -> Optional[any]:
        """Updates the price of the product with the given name
        Will update all products with the given name

        Args:
                name (str): the name of the product to update
                price (float): the new price of the product

        Returns:
                Optional[any]: the first updated product or None if not found
        """
        products.update_one({"name": name}, {"$set": {"price": price}})
        return products.find_one({"name": name})

def update_product_description(name: str, description: str) -> Optional[any]:
        """Updates the description of the product with the given name
        Will update all products with the given name

        Args:
                name (str): the name of the product to update
                description (str): the new description of the product

        Returns:
                Optional[any]: the first updated product or None if not found
        """
        products.update_one({"name": name}, {"$set": {"description": description}})
        return products.find_one({"name": name})

def update_product_category(name: str, category: str) -> Optional[any]:
        """Updates the category of the product with the given name
        Will update all products with the given name

        Args:
                name (str): the name of the product to update
                category (str): the new category of the product

        Returns:
                Optional[any]: the first updated product or None if not found
        """
        products.update_one({"name": name}, {"$set": {"category": category}})
        return products.find_one({"name": name})

def create_product(name: str, quantity: float, price: float = 0.0, description: str = "", category: str = "") -> Optional[any]:
        """Creates a new product

        Args:
                name (str): the name of the product
                quantity (float): the quantity of the product
                price (float, optional): the price of the product. Defaults to 0.0.
                description (str, optional): the description of the product. Defaults to "".
                category (str, optional): the category of the product. Defaults to "".

        Returns:
                Optional[any]: the created product or None if failed
        """
        products.insert_one({"name": name, "price": price, "quantity": quantity, "description": description, "category": category})
        return products.find_one({"name": name})
    
def get_id_from_name(name: str) -> str:
        """Returns the id of the product with the given name

        Args:
                name (str): the name of the product to find

        Returns:
                str: the id of the product
        """
        return products.find_one({"name": name}, {"_id": 1})["_id"]
    
def delete_product_by_name(name: str) -> None:
        """Deletes the product with the given name

        Args:
                name (str): the name of the product to delete
        """
        products.delete_one({"name": name})

def delete_product_by_id(id: str) -> None:
        """Deletes the product with the given id
        
        Args:
                id (str): the id of the product to delete
        """
        products.delete_one({"_id": bson.ObjectId(id)})

def insert_many_products(product_documents: Collection) -> int:
        """Inserts many products into the database

        Args:
                product_documents (Collection): the documents to insert

        Returns:
                int: the number of documents inserted
        """
        result = products.insert_many(product_documents)
        return len(result.inserted_ids)