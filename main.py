import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

from config.create_table import createTables
from controllers.hello import HelloHandler
from controllers.publicSourcesQuery import PublicSourcesQuery
from controllers.update_response_handler import UpdateResponseHandler
from handler.notfound import NotFoundHandler


def main():
    settings = dict(
        xsrf_cookies=False,
        autoreload=True,
        gzip=True,
        debug=True
    )

    application = tornado.web.Application([
        (r'/', HelloHandler),
        (r'/save', PublicSourcesQuery),
        (r'/update', UpdateResponseHandler),
        (r'/.*', NotFoundHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 8000))
    http_server.listen(port)
    print('Listening on http://localhost:%i' % port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    createTables()
    main()
