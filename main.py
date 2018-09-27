import os

import tornado.websocket
from tornado import web, ioloop, httpserver

from config.create_table import createTables
from controllers.hello import HelloHandler
from controllers.post_public_sources_query import PostPublicSourcesQuery
from controllers.update_public_sources_query import UpdatePublicSourcesQuery
from handler.notfound import NotFoundHandler

LISTEN_PORT = int(os.environ.get("PORT", 8000))


class WSHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self):
        print('new connection')

    def on_message(self, message):
        print('message received:  %s' % message)
        # Reverse Message and send it back
        print('sending back message: %s' % message[::-1])
        self.write_message('uau ' + message[::-1])

    def on_close(self):
        print('connection closed')

    def check_origin(self, origin):
        return True


def main():
    settings = dict(
        xsrf_cookies=False,
        autoreload=True,
        gzip=True,
        debug=True
    )

    # Create tornado application and supply URL routes
    application = web.Application([
        (r'/ws', WSHandler),
        (r'/', HelloHandler),
        (r'/save', PostPublicSourcesQuery),
        (r'/update/([0-9]+)', UpdatePublicSourcesQuery),
        (r'/.*', NotFoundHandler),
    ], **settings)

    # Setup HTTP Server
    http_server = httpserver.HTTPServer(application)
    http_server.listen(LISTEN_PORT)

    print('Servidor rodando no domínio http://localhost:{}'.format(LISTEN_PORT))

    # Start IO/Event loop
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    createTables()
    main()
