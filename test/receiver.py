import pika

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

def receive_message():
    # Verbindung zu RabbitMQ
    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost','5672'))
    channel = connection.channel()

    # Sicherstellen, dass die Queue existiert
    # channel.queue_declare(queue='pplservice_queue')
    # channel.queue_declare(queue='brpnservice_queue')

    # Setze den Callback, der ausgeführt wird, wenn eine Nachricht ankommt
    #channel.basic_consume(queue='pplservice_queue', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='brpnservice_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    receive_message()