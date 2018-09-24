import tornado.web
import psycopg2
import datetime
import json

from config.database import database

class SaveResponseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
        self.set_header("X-XSS-Protection", "1; mode=block")

    def OPTIONS(self):
        pass

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))

    def post(self):
        conn = None
        try:
            params = database()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            name = self.get_argument('name')
            response = self.get_argument('response')
            date = datetime.datetime.now()

            query = "INSERT INTO tb_tj_sp (name, response, date) VALUES (%s, %s, %s)"
            cur.execute(query, (name, response, date))
            conn.commit()
            cur.close()

            self.send_response({"message": 'Dado inserido com sucesso!'})

        except (Exception, psycopg2.DatabaseError) as error:
            self.write('Error')
            print(error)
        finally:
            if conn is not None:
                conn.close()
