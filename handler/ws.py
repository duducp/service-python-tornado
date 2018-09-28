from tornado.websocket import WebSocketHandler


class WebSocket(WebSocketHandler):
    connections = set()

    def data_received(self, chunk):
        pass

    def open(self):
        self.connections.add(self)
        print('new connection')

    def on_message(self, message):
        print('message received:  %s' % message)
        self.write_message(message)
        [client.write_message(message) for client in self.connections]

    def on_close(self):
        self.connections.remove(self)
        print('connection closed')

    def check_origin(self, origin):
        return True
