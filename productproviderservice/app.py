import logging
import pika
from flask import Flask, request, json, jsonify
from flask_cors import CORS
from bson.objectid import ObjectId
#from .product.service import Service as Service
# TODO: for docker container relative imports are not working
from product.service import Service as Service


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


@app.route('/')
def hello():
    app.logger.info('hello from console')
    # print("hello from normal stdout")
    return '<h1>Hello from Flask</h2>'


@app.route('/products', methods=["GET"])
def get_products():
    app.logger.info('Get to products')

   # Get all products from db
    service = Service()
    jsonProducts = service.find_all_products()

    # Convert JSON string to Python object
    products = json.loads(jsonProducts)

    convertedProducts = [
        {
            "id": item["_id"]["$oid"],
            #**{key: value for key, value in item.items() if key != "_id"}
            **{key: value for key, value in item.items()}
        }
        for item in products
    ]

    return convertedProducts, 200, {'Content-Type': 'application/json'}


@app.route('/product', methods=["POST"])
def create_product():
    app.logger.info(f'Create product with data: {request.get_json()}')
    
    data = request.get_json()
    app.logger.info(f'The typ of data is: {type(data)}')
    app.logger.info(f'The data is: {data}')
    # insert a new product into the db
    service = Service()
    product_id = service.create_product(data)

    if product_id is not None:
        # publish the event of successful updating a product
        
        message = create_json("Product","CREATE",data)
        publish_event(message)
        return jsonify({
            "created": str(product_id),
            "message": "JSON received successfully!"
        }), 200
    else:
        return jsonify({"message": "Product could not be created!"}), 404


@app.route('/product/<product_id>', methods=["DELETE"])
def delete_product(product_id):
    app.logger.info(f'Delete product with id: {product_id}')

    # Delete the product from the db
    service = Service()
    result = service.delete_product_by_id(product_id)

    if result:

        # publish the event of successful updating a product
        data = {"id": product_id}
        message = create_json("Product","DELETE",data)
        publish_event(message)
        return jsonify({"message": "Product with deleted successfully!"}), 200
    else:
        return jsonify({"message": "Product not found!"}), 404


@app.route('/product/<product_id>', methods=["PUT"])
def update_product(product_id):
    # Diese ProductId ist neu generiert.
    app.logger.info(f'Update product with id: {product_id} and data: {request.get_json()}')
    data = request.get_json()
    # Update the product in the db
    service = Service()
    result = service.update_product_with(product_id, data)

    if result:
        # publish the event of successful updating a product
        data["id"] = product_id
        message = create_json("Product","UPDATE",data)
        publish_event(message)
        return jsonify({"message": "Product updated successfully!"}), 200
    else:
        return jsonify({"message": "Product not found or update failed!"}), 404


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

# 
def publish_event(json_str):
    app.logger.info(f'publish_event called.')
    # Verbindung zu RabbitMQ herstellen
    #connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq','5672'))
    channel = connection.channel()

    # Nachricht senden
    channel.basic_publish(exchange='product_exchange',
                          routing_key='',
                          body=json_str)
    #print(f"Sent: {json_str}")
    app.logger.info(f'Sent: {json_str}')
    connection.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
