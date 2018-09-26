from http import HTTPStatus

from handler.cors import CorsHandler

class NotFoundHandler(CorsHandler):
    def get(self):
        self.set_status(HTTPStatus.NOT_FOUND)
        self.write({'error: ': True, 'msg: ': 'Rota não encontrada'})

if __name__ == "__main__":
    pass
