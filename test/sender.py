import pika

def send_message():
    # Verbindung zu RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Sicherstellen, dass die Queue existiert
    # channel.queue_declare(queue='brpnservice_queue')

    # Nachricht senden
    message = "Helloau RabbitMQ!"
    channel.basic_publish(exchange='product_exchange',
                          routing_key='',
                          body=message)
    print(f"Sent: {message}")

    connection.close()

if __name__ == '__main__':
    send_message()