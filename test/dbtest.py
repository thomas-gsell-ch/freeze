#! /usr/bin/python

# for testing purposes
from pymongo import MongoClient

# uri = "mongodb://root:example@localhost:27017"
uriDevContainer = "mongodb://root:example@host.docker.internal:27017"
client = MongoClient(uriDevContainer)

print("Setting up mongo client")

try:
    database = client.get_database("freezedb")
    products = database.get_collection("products")

    # Get all products
    allProducts = products.find()

    for product in allProducts:
        print(product)

    # Insert a product
    products.insert_one({
        "name": "Vanilla Ice Cream",
        "category": "Eis",
        "amount": "3",
        "location": "Küche",
        "freezingDate": "2024-10-10",
        "bestBefore": "2025-10-10"
    })

    # Query for a product that has the category 'Eis'
    query = {"category": "Eis"}
    product = products.find_one(query)
    print("Query result: ")
    print(product)
    client.close()
except Exception as e:
    raise Exception(
        "Unable to find the document due to the following error: ", e)
