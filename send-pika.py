import pika
import sys

channelname = sys.argv[1]
msg = sys.argv[2]

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue=channelname)

channel.basic_publish(exchange="", routing_key=channelname, body=msg)

print(f" [x] Sent '{msg}'")
