import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

channel.exchange_declare(exchange="logs", type="fanout")

message = " ".join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange="logs",
                      routing_key="",
                      body=message)

print(" [x] Sent {0!r}".format(message))

connection.close()
