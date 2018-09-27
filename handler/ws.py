from tornado import websocket


class WebSocket(websocket.WebSocketHandler):
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
