import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received {0!r}".format(body))
    time.sleep(body.count(b"."))
    print(" [x] Done.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue="task_queue")

print("[*] Waiting for messages...")

channel.start_consuming()
