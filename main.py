from app import config
from app.create_table import createTables

from tornado.web import Application
from tornado.ioloop import IOLoop

from controllers.post_public_sources_query import PostPublicSourcesQuery
from controllers.rabbitmq.pika_client import PikaClient
from controllers.update_public_sources_query import UpdatePublicSourcesQuery
from handler.error404 import Error404
from handler.ws import WebSocket


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
