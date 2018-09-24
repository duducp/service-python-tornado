import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

from controllers.hello_handler import HelloHandler
from config.create_table import createTables

def main():

    settings = dict(
        xsrf_cookies=True,
        autoreload=True,
        gzip=True,
        debug=True
    )

    application = tornado.web.Application([
        (r"/", HelloHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 8000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    createTables()
    main()
