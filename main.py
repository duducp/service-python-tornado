import json
import time

import pika

from app import config
from app.create_table import createTables

from tornado.web import Application
from tornado.ioloop import IOLoop

from controllers.post_public_sources_query import PostPublicSourcesQuery
from controllers.update_public_sources_query import UpdatePublicSourcesQuery
from controllers.update_response import update
from handler.error404 import Error404
from handler.ws import WebSocket


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
        self._channel.queue_declare(queue=self._queue, durable=False, callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        print(" [*] RabbitMQ conectado a fila", self._queue)
        self._channel.basic_consume(self.handle_delivery, queue=self._queue)

    def handle_delivery(self, channel, method, header, body):
        try:
            message = json.loads(body)
            update(body)
        except Exception as e:
            error = json.dumps({
                "ErrorMessage": str(e),
                "Source": self._queue,
                "Timestamp": int(time.time()),
                "Type": "alert",
                "Request": str(body)
            })
            print(error)
        finally:
            channel.basic_ack(delivery_tag=method.delivery_tag)


class App(Application):
    def __init__(self):
        handlers = [
            (r'/ws', WebSocket),
            (r'/save', PostPublicSourcesQuery),
            (r'/update/([0-9]+)', UpdatePublicSourcesQuery),
            (r'/.*', Error404),
        ]

        Application.__init__(self, handlers)


def main():
    try:
        # Start Tornado
        application = App()
        application.pika = PikaClient()
        application.listen(config.TORNADO_PORT, config.TORNADO_HOST)
        print(' [*] Serviço rodando no domínio http://{}:{}'.format(config.TORNADO_HOST, config.TORNADO_PORT))

        # Start IO/Event loop
        ioloop = IOLoop.instance()
        ioloop.add_timeout(config.IOLOOP_TIMEOUT, application.pika.connect)
        ioloop.start()
    except KeyboardInterrupt:
        print('stop')


if __name__ == '__main__':
    createTables()
    main()
