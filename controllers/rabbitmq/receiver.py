#!/usr/bin/env python
import json
import pika
import time
from random import randrange

from controllers.update import update


def connect():
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    global channel
    channel = connection.channel()
    print(' [*] Serviço estabaleceu conexão com RabbitMQ')


def receiver():
    # define o nome da fila
    channel.queue_declare(queue='response')

    # número de mensagens a ser envia por vez
    channel.basic_qos(prefetch_count=1)

    # consome a fila (recebe os dados da fila)
    channel.basic_consume(callback_receiver, queue='response')

    print(' [*] Serviço inicializado. Para parar precione CTRL+C')
    channel.start_consuming()


def callback_receiver(ch, method, properties, body):
    time.sleep(randrange(0, 5))
    ch.basic_ack(delivery_tag=method.delivery_tag)

    update(body)


if __name__ == '__main__':
    try:
        connect()
        receiver()
    except KeyboardInterrupt:
        connection.close()
