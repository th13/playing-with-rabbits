import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

channel.exchange_declare(exchange="logs", type="direct")

# Get messages from stdin.
while True:
    log = input("❭❭❭ ")
    
    severity = log.split(" ")[0]
    message = " ".join(log.split(" ")[1:])
    
    channel.basic_publish(exchange="logs",
                          routing_key=severity,
                          body=message)

    print(" [x] Sent {0!r}: {1!r}".format(severity, message))

connection.close()

