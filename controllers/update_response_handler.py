import tornado.web
import psycopg2
import datetime

from config.database import database

class UpdateResponseHandler(tornado.web.RequestHandler):

    def post(self):
        conn = None
        resources = {}
        try:
            params = database()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            response = self.get_argument('response')
            id = self.get_argument('id')

            query = "UPDATE tb_tj_sp SET response = %s WHERE id = %s"
            cur.execute(query, (response, id))
            conn.commit()
            cur.close()

            self.set_status(200)
            self.finish({"message": 'Dado atualizado com sucesso!'})

        except (Exception, psycopg2.DatabaseError) as error:
            self.write('Error')
            print(error)
        finally:
            if conn is not None:
                conn.close()