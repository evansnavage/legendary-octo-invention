from typing import Collection
import pymongo
import sys

try:
  client = pymongo.MongoClient("mongodb+srv://admin:1234@imscluster.vv08q.mongodb.net/")
  
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)
  
db = client.inventory

test_products = db["products"]

product_documents = [{ "name": "Green Paint", "price": 3.99, "quantity": 10 },
                     { "name": "Blue Paint", "price": 3.99, "quantity": 10 },
                     { "name": "Red Paint", "price": 3.99, "quantity": 10 },
                     { "name": "Yellow Paint", "price": 3.99, "quantity": 10 }]

try:
    test_products.drop()
except pymongo.errors.OperationFailure:
    print("An authentication error was received. Are your username and password correct in your connection string?")
    sys.exit(1)

try:
    result = test_products.insert_many(product_documents)
except pymongo.errors.OperationFailure:
    print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
    sys.exit(1)
else:
    inserted_count = len(result.inserted_ids)
    print("Inserted %x documents for test setup." %(inserted_count))
    print ("\n")
    
def get_all_products() -> Collection:
    """Returns all products

    Returns:
        Collection: A collection of all products
    """
    return test_products.find()

def get_products_by_name(name: str) -> Collection:
    """Returns all products with the given name

    Args:
        name (str): The name of the products to find

    Returns:
        Collection: documents with the given name
    """
    return test_products.find_many({"name": name})

def get_product_by_id(id) -> any | None:
    """Returns the product with the id

    Args:
        id (string): The id of the product to find

    Returns:
        any | None: The bson object of the product or None if not found
    """
    return test_products.find_one({"id": id})

def get_first_product_by_name(name:str ) -> any | None:
    """Returns the first product with the given name

    Args:
        name (str): Name of the product to find

    Returns:
        any | None: the bson object of the product or None if not found
    """
    return test_products.find_one({"name": name})

def update_product_quantity(name, quantity) -> any | None: 
    """Updates the quantity of the product with the given name
    Will update all products with the given name

    Args:
        name (str): the name of the product to update
        quantity (int): the new quantity of the product

    Returns:
        any | None: the first updated product or None if not found
    """
    test_products.update_one({"name": name}, {"$set": {"quantity": quantity}})
    return test_products.find_one({"name": name})