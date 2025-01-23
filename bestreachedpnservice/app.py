import logging
import pika
from flask import Flask, request, json, jsonify
from flask_cors import CORS
from bson.objectid import ObjectId
from pywebpush import webpush, WebPushException   # requirement pywebpush==2.0.3 failed
#from .product.service import Service as Service
# TODO: for docker container relative imports are not working
#from product.service import Service as Service
from repository.mongo import MongoRepository as Service
import time
import threading
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)


# Flask-Logger konfigurieren
if not app.debug:
    # Setze den Log-Level
    app.logger.setLevel(logging.INFO)
    
    # Erstelle einen Stream-Handler für stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Ändere dies zu DEBUG, WARNING, etc. falls benötigt
    
    # Format für die Log-Ausgabe
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    stream_handler.setFormatter(formatter)
    
    # Füge den Handler zum Flask-Logger hinzu
    if not app.logger.handlers:
        app.logger.addHandler(stream_handler)


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


#-----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# Push-Notification
#----------------------------------------------------------------------------------------


VAPID_PUBLIC_KEY = "BCcugnAXkyYu6Ci9G0FbmeYD3EzvUoNTCxqpFo1TCHSB9-iErdH2v3FYYWHNngZKXVRVFP-D00m5li1g_DAmCe4"
VAPID_PRIVATE_KEY = "DHn5rO6TzClhtOisl1LTOTiiZ2uSkB_GYFVKOGRjH0w"
VAPID_CLAIMS = {
    "sub": "mailto:example@example.com"
}



# Die Subscription infos sind: 
# {
#     'endpoint': 'https://fcm.googleapis.com/fcm/send/e8KaETkV-GA:APA91bHzu4z6BoQIiaenAVTSL-NNAyU-9OclB5o81pPx54MmhDmHKgk-F0Cr37evPTgg-xYJomduoH9npii8_WBZHI7KssbAmJWz8Se14ZWl5DQ4VsYTeOa6_FnFyN6uQjg1XtI7TAdf', 
#     'expirationTime': None, 
#     'keys': {
#         'p256dh': 'BI1RCOjvqfRQzbRJNzMPcX5oALXg4kN_bqxceIydAqgzi92KHA79JcYBzhJHcIM3srInmFTM7D_LzlnaI-vWC9Q', 
#         'auth': 'oDcDHYsaBebQIP2RXAOgGQ'
#     }
# }

@app.route('/')
def hello():
    app.logger.info('hello from console')
    # print("hello from normal stdout")
    return '<h1>Hello from Flask of the bestreachedpnservice</h2>'

#subscriptions = []

@app.route('/subscribe', methods=['POST'])
def subscribe():
    '''Erlaubt Subscriptions für Push-Notifications zu registrieren'''

    subscription_info = request.get_json()
    app.logger.info(f"Die Subscription infos sind: {subscription_info}")
    app.logger.info(f"Der Type der Subscription ist: {type(subscription_info)}")
    service = Service()
    subscriptionId = service.insert_subscription(subscription_info)
    #subscriptions.append(subscription_info)

    if subscriptionId is not None:
        return jsonify({"message": "Subscription successful.", "registrated": str(subscriptionId)}), 200
    else:
        return jsonify({"message": "Subscription could not be registrated!"}), 404


def send_push_notification():
    app.logger.info("Startet den push notification Service.")
    while True:
        time.sleep(60)
        #time.sleep(86400)  # Wait 1 Stunde = 86400 Sekunden
        service = Service()
        subscriptions = service.select_all_subscriptions()
        date_format = "%d-%m-%Y"
        current_date_obj = datetime.now()
        current_date_str = current_date_obj.strftime(date_format)
        warndates = service.select_all_warn_dates_before(current_date_str)
        app.logger.info(f"Found the followed warndates: {warndates}")
        for subscription in subscriptions:
            app.logger.info(f"Found the followed subscription: {subscription}")
            for warndate in warndates:
                app.logger.info(f"A webpush shall be send for: {warndate}")
                # Nur senden wenn warndate mehr als ein Item enthält
                if len(warndate['items']) > 0:
                    try:
                        webpush(
                            subscription_info=subscription,
                            data=create_pn_Banner(warndate),
                            vapid_private_key=VAPID_PRIVATE_KEY,
                            vapid_claims=VAPID_CLAIMS
                        )
                    except WebPushException as ex:
                        app.logger.info(f"Delete subscription: {subscription}")
                        service.delete_subscription(subscription['_id'])
                        app.logger.error(f"Push notification failed: {ex}")


def create_pn_Banner(warning):
    '''Erzeugt den konkreten Banner für die Push Nachricht.'''
    result = []
    warndate = warning["warndate"]
    result.append(f"Das Ablauf-Warndatum vom {warndate} ist überschritten für:")
    for item in warning["items"]:
        result.append(f"{item['name']}, {item['location']}, {item['amount']}, {item['bestBefore']}")
    result.append("")  # Leere Zeile für bessere Lesbarkeit
    return "\n".join(result)


#-----------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
# RabbitMQ-Client
#-------------------------------------------------------------------------------------

# insert subscription
# 
# insert Product
#
# delete Product

# wartet auf Events 

def callback(ch, method, properties, body):
    #print(f"Received: {body.decode()}")

    json_string = body.decode()
    app.logger.info(f"Received: {json_string}")
    parsed_json = json.loads(json_string)
    topic, command = extract_topic_and_command(parsed_json)
    data = extract_data(parsed_json)

    app.logger.info(f"bestreachedpnservice: Command '{command}' ausführen.")
    if topic == "Product":
        if command == "CREATE":
            # Berechnen des Warndatums
            # Einfügen des Products in die Liste des entsprechenden Warndatums.
            warndate = createWarndate(data)
            service = Service()
            service.insert_product(warndate, data)

        elif command == "UPDATE":
            # Ändern des Products
            # Bestehender Eintrag löschen, Warndate neu berechnen, Eintrag neu einfügen.
            app.logger.info(f"bestreachedpnservice: Command '{command}' ausführen.") 
            product_id = data['id']
            service = Service()
            modifiedCount = service.delete_product(product_id)
            app.logger.info(f"bestreachedpnservice: Anzahl der gelöschten Einträge: {modifiedCount}")
            warndate = createWarndate(data)
            service.insert_product(warndate, data)
            app.logger.info(f"bestreachedpnservice: Anzahl eingefügten Einträge: {modifiedCount}")

        elif command == "DELETE":
            # Product suchen und aus der entsprechenden Warndatumsliste entfernen
            app.logger.info(f"bestreachedpnservice: Command '{command}' ausführen.")
            product_id = data['id']
            service = Service()
            modifiedCount = service.delete_product(product_id)
            app.logger.info(f"bestreachedpnservice: Anzahl der gelöschten Einträge: {modifiedCount}")
        else:
            app.logger.error(f"bestreachedpnservice: Event hat kein gültiges Command: '{command}'")    
    else:
        app.logger.error(f"bestreachedpnservice: Event mit Topic '{topic}'ist im falschen Kanal")


def createWarndate(data):
    bestBefore_str = data['bestBefore']
    date_format = "%d-%m-%Y"
    date_obj = datetime.strptime(bestBefore_str, date_format)
    warning_date_obj = date_obj - timedelta(weeks=1)
    return warning_date_obj.strftime(date_format)


def extract_data(json_obj):
    """Extrahiert die 'data'-Datenstruktur aus dem JSON."""
    data = json_obj.get("data", {})
    return data

def extract_topic_and_command(json_obj):
    """Extrahiert das Topic und das Command aus dem JSON."""
    topic = json_obj.get("topic", None)
    command = json_obj.get("command", None)
    return topic, command

def start_message_Receiver():
    # Verbindung zu RabbitMQ
    app.logger.info('Der Message Receiver wurde gestartet.')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))
    channel = connection.channel()
    # Setze den Callback, der ausgeführt wird, wenn eine Nachricht ankommt
    channel.basic_consume(queue='brpnservice_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# Utilities
#-----------------------------------------------------------------------------------------------

def create_json(topic, command, data):
    
    data = convert_objectid_to_string(data)
    
    app.logger.info(f'The data is: {data}')
    # JSON-Daten aus den übergebenen Parametern zusammensetzen
    json_data = {
        "topic": topic,
        "command": command,
        "data": data
    }
    # JSON-String aus Python-Datenstruktur erstellen
    json_string = json.dumps(json_data, indent=4)
    app.logger.info(f'Create json string : {json_string}')
    return json_string


def convert_objectid_to_string(data):
    """
    Konvertiert ObjectId-Werte in einem Dictionary in Strings und setzt sie zurück ins Dictionary.
    """
    for key, value in data.items():
        if isinstance(value, ObjectId):
            # Konvertiere ObjectId zu String
            data[key] = str(value)
    return data


# For analysing only:
# import os
# LOCK_FILE = "thread_running.lock"

if __name__ == "__main__":
#    if not os.path.exists(LOCK_FILE):  # Überprüfen, ob die Lock-Datei existiert
#        open(LOCK_FILE, 'w').close()  # Lock-Datei erstellen
    threading.Thread(target=send_push_notification, daemon=True).start()   # Funktioniert
    threading.Thread(target=start_message_Receiver, daemon=True).start()
    app.logger.info("Hier startet es.")    # Funktioniert
    app.run(host='0.0.0.0', debug=False)   # Damit funktionierts unter http://localhost:5001/
#    else:
#        print("Tatsächlich, dieses Script wird zweimal ausgeführt.")