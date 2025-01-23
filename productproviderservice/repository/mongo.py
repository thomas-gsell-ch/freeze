from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging

DATABASE_NAME = 'productsdb'
COLLECTION_NAME = 'products'
# MONGO_URL = "mongodb://root:example@localhost:27017/"
MONGO_URL_CONTAINER = "mongodb://root:example@host.docker.internal:27017"




# Konfiguriere den Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)



class MongoRepository(object):
    def __init__(self):
        mongoclient = MongoClient(MONGO_URL_CONTAINER)
        database = mongoclient.get_database(DATABASE_NAME)
        self.products = database.get_collection(COLLECTION_NAME)

    def find_all(self):
        try:
            allProducts = self.products.find()

            # Convert the cursor to JSON
            json_result = dumps(allProducts, indent=2)

            return json_result
        except Exception as e:
            raise Exception(
                "Unable to find the document due to the following error: ", e)

    def create(self, product):
        try:
            insertedProductId = self.products.insert_one(product).inserted_id

            return insertedProductId
        except Exception as e:
            raise Exception(
                "Unable to insert due to the following error: ", e)

        return self.db.productsdb.insert_one(product)

    def update(self, id, product):
        logging.info("MongoRepository.update(): called.")
        try:
            id = id['product_id']
            # id = str(id)
            if isinstance(id, str):
                logging.info("id ist ein String.")
            else:
                logging.info(f"id ist ein: {type(id)}")

            # product['_id'] = id
            modifiedCount = self.products.replace_one({'_id': ObjectId(id)}, product).modified_count
            logging.info(f"affected documents: {modifiedCount}")

            return modifiedCount
        except Exception as e:
            raise Exception("Unable to update the document due to the following error: ", e)

    def delete(self, id):
        try:
            deletedCount = self.products.delete_one(
                {'_id': ObjectId(id)}).deleted_count

            return deletedCount
        except Exception as e:
            raise Exception(
                "Unable to delete the document due to the following error: ", e)
