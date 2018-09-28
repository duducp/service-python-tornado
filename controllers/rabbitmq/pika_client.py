import pika

from app import config
from controllers.update_response import update


class PikaClient(object):
    def __init__(self):
        self._connection = None
        self._channel = None
        self._queue = 'response'

    # https://gist.github.com/vgoklani/5951694
    # https://pika.readthedocs.io/en/0.9.8/connecting.html
    def connect(self):
        try:
            credentials = pika.PlainCredentials(config.RMQ_USER, config.RMQ_PASSWORD)
            param = pika.ConnectionParameters(host=config.RMQ_HOST, credentials=credentials)

            self._connection = pika.TornadoConnection(param, on_open_callback=self.on_connected)
        except Exception as e:
            print('Something went wrong... %s', e)

    def on_connected(self, connection):
        print(' [*] Serviço estabaleceu conexão com RabbitMQ')

        # open a channel
        self._connection.channel(self.on_channel_open)

    def on_channel_open(self, new_channel):
        print(' [*] Abrindo canal para o rabbitmq')

        self._channel = new_channel
        self.receiver()

    def receiver(self):
        print(' [*] Consumnindo a fila', self._queue)
        self._channel.queue_declare(queue=self._queue, durable=False, callback=self.cb_receiver)

    def cb_receiver(self, frame):
        print(" [*] RabbitMQ conectado a fila", self._queue)
        self._channel.basic_consume(self.hd_receiver, queue=self._queue)

    def hd_receiver(self, channel, method, header, body):
        try:
            update(body)
        except Exception as e:
            print(str(e))
        finally:
            self._channel.basic_ack(delivery_tag=method.delivery_tag)
