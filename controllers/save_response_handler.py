import tornado.web
import psycopg2
import datetime

from config.database import database

class SaveResponseHandler(tornado.web.RequestHandler):

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

            self.set_status(200)
            self.finish({"message": 'Dado inserido com sucesso!'})

        except (Exception, psycopg2.DatabaseError) as error:
            self.write('Error')
            print(error)
        finally:
            if conn is not None:
                conn.close()