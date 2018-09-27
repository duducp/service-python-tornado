import config
import pika
import time
from random import randrange

from controllers.update_response import update


def receiver():
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.HOST))

    channel = connection.channel()
    print(' [*] Serviço estabaleceu conexão com RabbitMQ')

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


def run():
    receiver()


if __name__ == '__main__':
    try:
        receiver()
    except KeyboardInterrupt:
        connection.close()
