
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
import logging


#DATABASE_NAME = 'warndatesdb'
#WARNDATES_COLLECTION_NAME = 'warndates'
#SUBSCRIPTIONS_COLLECTION_NAME = 'subscriptions'
#MONGO_URL = "mongodb://root:example@localhost:27018/"
#MONGO_URL_CONTAINER = "mongodb://root:example@host.docker.internal:27018"



# Konfiguriere den Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)




class MongoRepository:
    def __init__(self, connection_string, database_name):
        """Initialisiert die Verbindung zur MongoDB."""
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.warndates_collection = self.db['warndates']
        self.subscriptions_collection = self.db['subscriptions']

    # Insert subscription
    def insert_subscription(self, subscription):
        """Fügt ein Subscription-Dokument in die subscriptions-Sammlung ein."""
        self.subscriptions_collection.insert_one(subscription)

    # Insert product
    def insert_product(self, warndate, product):
        """Fügt ein Produkt zu einer bestimmten warndate hinzu."""
        converted_warndate = datetime.strptime(warndate, "%d-%m-%Y").strftime("%Y-%m-%d")
        self.warndates_collection.update_one(
            {'warndate': converted_warndate},
            {'$push': {'items': product}},
            upsert=True
        )

    # Select all warnDates < actualDate
    def select_all_warn_dates_before(self, actual_date):
        """Wählt alle warndates, die vor einem bestimmten Datum liegen."""
        converted_actualdate = datetime.strptime(actual_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        # print("Vergleiche mit folgendem Datum: ", converted_actualdate)
        return list(self.warndates_collection.find({'warndate': {'$lte': converted_actualdate}}))

    # Select all subscriptions
    def select_all_subscriptions(self):
        """Gibt alle Subscriptions zurück."""
        return list(self.subscriptions_collection.find())

    # Delete product
    def delete_product(self, product_id):
        """Löscht ein Produkt anhand der ID aus den items aller warndates."""
        self.warndates_collection.update_many(
            {},
            #{'$pull': {'items': {'_id': ObjectId(product_id)}}}
            {'$pull': {'items': {'_id': product_id}}}
        )


# insert subscription
# 
# insert Product
# 
# select all warnDate < actualDate
#
# select all subscriptions 
# for all subscription
#     for every warnDate
#         send PushNotifications 
#
# delete Product




# Beispielverwendung
if __name__ == "__main__":
    # Verbindung zur MongoDB
    connection_string = "mongodb://root:example@localhost:27018"
    database_name = "warndatesdb"

    repo = MongoRepository(connection_string, database_name)

    # Beispiel-Subscription einfügen
    subscription = {
        'endpoint': 'https://example.com',
        'expirationTime': None,
        'keys': {
            'p256dh': 'example_key',
            'auth': 'example_auth'
        }
    }
    repo.insert_subscription(subscription)  # works


    product_obj_id = ObjectId()
    product_id = str(product_obj_id)

    # Beispiel-Produkt einfügen
    product = {
        "_id": product_id,
        "ort": "Dachboden",
        "name": "Apfel",
        "amount": "1kg",
        "bestBefore": "01-05-2025"
    }
    repo.insert_product("01-10-2026", product)  # works

    # WarnDates vor einem bestimmten Datum abrufen   #works
    warn_dates = repo.select_all_warn_dates_before("02-10-2026")
    print("WarnDates vor 08-12-2025:", warn_dates)

    # Alle Subscriptions abrufen
    subscriptions = repo.select_all_subscriptions()
    print("Subscriptions:", subscriptions)

    # Produkt löschen   #works
    #product_id = "677cf5159821cc2e0efeb9ea"
    product_id = product["_id"]  # ID des eingefügten Produkts
    repo.delete_product(product_id)
    print(f"Produkt mit ID {product_id} wurde gelöscht.")



