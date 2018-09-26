#!/usr/bin/env python
import pika
import time
from random import randrange

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# nome da fila
channel.queue_declare(queue='request-tj-sp')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(randrange(0, 5))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# número de mensagens a ser envia por vez
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback, queue='request-tj-sp')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()