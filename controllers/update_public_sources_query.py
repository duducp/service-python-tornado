import psycopg2
import json

from http import HTTPStatus
from json import JSONDecodeError
from config.database import database
from handler.cors import CorsHandler


class UpdatePublicSourcesQuery(CorsHandler):
    def send_response(self, message, error=False, status=200):
        self.set_status(status)
        self.write({'status: ': status, 'error: ': error, 'msg: ': message})

    def patch(self, _id):
        try:
            body = json.loads(self.request.body.decode("utf-8"))
            if body:
                response = body.get('response', '')

                if not response:
                    return self.send_response('Por favor informe a RESPONSE', False, HTTPStatus.BAD_REQUEST)

                conn = None
                try:
                    params = database()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()

                    query = "UPDATE tb_tj_sp SET response = %s WHERE id = %s"
                    cur.execute(query, (response, _id))
                    conn.commit()
                    cur.close()

                    return self.send_response('Dado atualizado com sucesso', False, 200)

                except (Exception, psycopg2.DatabaseError) as error:
                    return self.send_response(error, True, HTTPStatus.INTERNAL_SERVER_ERROR)
                finally:
                    if conn is not None:
                        conn.close()
            else:
                return self.send_response('Nenhum dado foi fornecido', True, HTTPStatus.BAD_REQUEST)

        except JSONDecodeError as error:
            return self.send_response('Os dados informados não é do tipo JSON válido', True, HTTPStatus.BAD_REQUEST)
