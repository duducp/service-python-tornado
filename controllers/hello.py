import tornado.web

class HelloHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_status(200)
        self.finish({"message": "Olá mundo!"})