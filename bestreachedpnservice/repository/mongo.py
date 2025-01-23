from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
import logging

DATABASE_NAME = 'warndatesdb'
WARNDATES_COLLECTION_NAME = 'warndates'
SUBSCRIPTIONS_COLLECTION_NAME = 'subscriptions'
# MONGO_URL = "mongodb://root:example@localhost:27018/"
MONGO_URL_CONTAINER = "mongodb://root:example@host.docker.internal:27018"


# Konfiguriere den Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class MongoRepository:
    def __init__(self):
        """Initialisiert die Verbindung zur MongoDB."""
        self.client = MongoClient(MONGO_URL_CONTAINER)
        self.db = self.client[DATABASE_NAME]
        # self.warndates_collection = self.db['warndates']
        self.warndates_collection = self.db[WARNDATES_COLLECTION_NAME]
        # self.subscriptions_collection = self.db['subscriptions']
        self.subscriptions_collection = self.db[SUBSCRIPTIONS_COLLECTION_NAME]

    # Insert subscription
    def insert_subscription(self, subscription):
        """Fügt ein Subscription-Dokument in die subscriptions-Sammlung ein."""
        try:
            insertedSubscriptionId = self.subscriptions_collection.insert_one(subscription)
            return insertedSubscriptionId
        except Exception as e:
            raise Exception("Unable to insert due to the following error: ", e)

    # Insert product
    def insert_product(self, warndate, product):
        """Fügt ein Produkt zu einer bestimmten warndate hinzu."""
        converted_warndate = datetime.strptime(warndate, "%d-%m-%Y").strftime("%Y-%m-%d")
        
        try:
            modifiedCount = self.warndates_collection.update_one(
                {'warndate': converted_warndate},
                {'$push': {'items': product}},
                upsert=True
            )
            return modifiedCount
        except Exception as e:
            raise Exception("Unable to update the document due to the following error: ", e)
    

    # Select all warnDates < actualDate
    def select_all_warn_dates_before(self, actual_date):
        """Wählt alle warndates, die vor einem bestimmten Datum liegen."""
        try:
            converted_actualdate = datetime.strptime(actual_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            # print("Vergleiche mit folgendem Datum: ", converted_actualdate)
            jsonList_result = list(self.warndates_collection.find({'warndate': {'$lte': converted_actualdate}}))
            return jsonList_result
        except Exception as e:
            raise Exception("Unable to find all warndates entries due to the following error: ", e)        

    # Select all subscriptions
    def select_all_subscriptions(self):
        """Gibt alle Subscriptions zurück."""
        try:
            jsonList_result = list(self.subscriptions_collection.find())
            return jsonList_result
        except Exception as e:
            raise Exception("Unable to find all subscription entries due to the following error: ", e)        

    # Delete product
    def delete_product(self, product_id):
        """Löscht ein Produkt anhand der ID aus den items aller warndates."""
        try:
            modifiedCount = self.warndates_collection.update_many(
                {},
                #{'$pull': {'items': {'_id': ObjectId(product_id)}}}
                {'$pull': {'items': {'_id': product_id}}}
            )
            return modifiedCount
        except Exception as e:
            raise Exception("Unable to delete the product due to the following error: ", e)

    # Delete subscription
    def delete_subscription(self, subscription_id):
        """Löscht eine Subscription anhand der ID aus den subscriptions."""
        try:
            # modifiedCount = self.subscriptions_collection.delete_one({"_id": ObjectId(subscription_id)})
            modifiedCount = self.subscriptions_collection.delete_one({"_id": subscription_id})
            return modifiedCount
        except Exception as e:
            raise Exception("Unable to delete the subscription due to the following error: ", e)        