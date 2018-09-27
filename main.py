import config

from tornado import web, ioloop, httpserver

from app.create_table import createTables
from controllers.post_public_sources_query import PostPublicSourcesQuery
from controllers.update_public_sources_query import UpdatePublicSourcesQuery
from handler.error404 import NotFoundHandler
from handler.ws import WebSocket


def main():
    # Create tornado application and supply URL routes
    app = web.Application([
        (r'/ws', WebSocket),
        (r'/save', PostPublicSourcesQuery),
        (r'/update/([0-9]+)', UpdatePublicSourcesQuery),
        (r'/.*', NotFoundHandler),
    ])

    # Setup HTTP Server
    http_server = httpserver.HTTPServer(app)
    http_server.listen(config.LISTEN_PORT, config.HOST)

    print('Servidor rodando no domínio http://{}:{}'.format(config.HOST, config.LISTEN_PORT))

    # Start IO/Event loop
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    createTables()
    main()
