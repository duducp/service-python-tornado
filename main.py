from app import config
from app.create_table import createTables

from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from controllers.post_public_sources_query import PostPublicSourcesQuery
from controllers.update_public_sources_query import UpdatePublicSourcesQuery
from handler.error404 import NotFoundHandler
from handler.ws import WebSocket


def main():
    # Create tornado application and supply URL routes
    app = Application([
        (r'/ws', WebSocket),
        (r'/save', PostPublicSourcesQuery),
        (r'/update/([0-9]+)', UpdatePublicSourcesQuery),
        (r'/.*', NotFoundHandler),
    ])

    # Setup HTTP Server
    http_server = HTTPServer(app)
    http_server.listen(config.APP_PORT, config.APP_HOST)

    print('Servidor rodando no domínio http://{}:{}'.format(config.APP_HOST, config.APP_PORT))

    # Start IO/Event loop
    IOLoop.instance().start()


if __name__ == '__main__':
    createTables()
    main()
