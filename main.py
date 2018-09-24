import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

from config.create_table import createTables
from controllers.hello_handler import HelloHandler
from controllers.save_response_handler import SaveResponseHandler
from controllers.update_response_handler import UpdateResponseHandler

def main():

    settings = dict(
        xsrf_cookies=False,
        autoreload=True,
        gzip=True,
        debug=True
    )

    application = tornado.web.Application([
        (r"/", HelloHandler),
        (r"/save", SaveResponseHandler),
        (r"/update", UpdateResponseHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 8000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    createTables()
    main()
