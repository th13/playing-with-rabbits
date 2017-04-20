import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

channel.exchange_declare(exchange="logs", type="direct")

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: {} [info] [warning] [error]\n".format(sys.argv[0]))
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange="logs",
                       queue=queue_name,
                       routing_key=severity)

print("[*] Waiting for logs.")

def callback(ch, method, properties, body):
    print("[x] {0!r}: {1!r}".format(method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
