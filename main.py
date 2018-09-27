import os

from tornado import web, ioloop, httpserver

from config.create_table import createTables
from controllers.hello import HelloHandler
from controllers.post_public_sources_query import PostPublicSourcesQuery
from controllers.update_public_sources_query import UpdatePublicSourcesQuery
from handler.notfound import NotFoundHandler

LISTEN_PORT = int(os.environ.get("PORT", 8000))
LISTEN_ADDRESS = '127.0.0.1'


def main():
    settings = dict(
        xsrf_cookies=False,
        autoreload=True,
        gzip=True,
        debug=True
    )

    # Create tornado application and supply URL routes
    application = web.Application([
        (r'/', HelloHandler),
        (r'/save', PostPublicSourcesQuery),
        (r'/update/([0-9]+)', UpdatePublicSourcesQuery),
        (r'/.*', NotFoundHandler),
    ], **settings)

    # Setup HTTP Server
    http_server = httpserver.HTTPServer(application)
    http_server.listen(LISTEN_PORT, LISTEN_ADDRESS)

    print('Servidor rodando no domínio {}:{}'.format(LISTEN_ADDRESS, LISTEN_PORT))

    # Start IO/Event loop
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    createTables()
    main()
