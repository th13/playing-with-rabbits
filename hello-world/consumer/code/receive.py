import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

channel.queue_declare(queue="hello")

def callback(ch, method, properties, body):
    print("[x] Received {}".format(body))

channel.basic_consume(callback, queue="hello", no_ack=True)

print("[*] Waiting for messages...")

channel.start_consuming()
