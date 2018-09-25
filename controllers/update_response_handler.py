import tornado.web
import tornado.escape
import psycopg2
import json

from config.database import database

class UpdateResponseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
        self.set_header("X-XSS-Protection", "1; mode=block")

    def options(self):
        pass

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))

    def patch(self):
        conn = None
        try:
            params = database()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            data = tornado.escape.json_decode(self.request.body)

            id = data.get('id', '')
            response = data.get('response', '')

            if not response:
                return self.send_response({'error': True, 'msg': 'Por favor informe a RESPONSE.'}, 400)

            query = "UPDATE tb_tj_sp SET response = %s WHERE id = %s"
            cur.execute(query, (response, id))
            conn.commit()
            cur.close()

            self.set_status(200)
            self.finish({"message": 'Dado atualizado com sucesso!'})

        except (Exception, psycopg2.DatabaseError) as error:
            self.write({'Error': error})
        finally:
            if conn is not None:
                conn.close()