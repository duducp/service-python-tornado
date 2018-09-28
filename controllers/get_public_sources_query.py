import psycopg2
import json

from http import HTTPStatus
from app.database import database
from handler.cors import CorsHandler


class GetPublicSourcesQuery(CorsHandler):
    def send_response(self, message, data=None, error=False, status=200):
        self.set_status(status)
        self.write({'status: ': status, 'error: ': error, 'msg: ': message, 'data': data})

    def get(self, _id):
        conn = None
        try:
            params = database()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            query = "SELECT id, name, response, date FROM tb_tj_sp WHERE id = %s"
            cur.execute(query, (int(_id),))
            data = cur.fetchone()

            obj = {
                'id': data[0],
                'name': data[1],
                'response': json.loads(data[2]),
                'datetime': data[3].isoformat()
            }

            cur.close()

            return self.send_response('', obj, False, 200)

        except (Exception, psycopg2.DatabaseError) as error:
            return self.send_response('', str(error), True, HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            if conn is not None:
                conn.close()
