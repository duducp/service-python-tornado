import pika
import psycopg2
import datetime
import json

from json import JSONDecodeError
from http import HTTPStatus
from handler.cors import CorsHandler
from config.database import database

from controllers.rabbitmq import addRabbitmq


class PostPublicSourcesQuery(CorsHandler):
    def send_response(self, message, error=False, status=200):
        self.set_status(status)
        self.write({'status: ': status, 'error: ': error, 'msg: ': message})

    def addRabbitmq(self, obj):
        try:
            # Conecta
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            # Cria a fila
            channel.queue_declare(queue='request-tj-sp')

            message_rabbit_mq = json.dumps(obj)

            # envia a mensagem para a fila
            channel.basic_publish(exchange='', routing_key='request-tj-sp', body=message_rabbit_mq)

            connection.close()
        except Exception as error:
            return self.send_response('Erro ao adicionar objeto a lista', False, HTTPStatus.INTERNAL_SERVER_ERROR)

    def post(self):
        try:
            # body = tornado.escape.json_decode(self.request.body)
            body = json.loads(self.request.body.decode("utf-8"))
            if body:
                name = body.get('name', '')
                response = body.get('response', '')
                date = datetime.datetime.now()

                if not name:
                    return self.send_response('Por favor informe o NOME', False, HTTPStatus.BAD_REQUEST)

                conn = None
                try:
                    params = database()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()

                    query = "INSERT INTO tb_tj_sp (name, response, date) VALUES (%s, %s, %s) RETURNING id"
                    cur.execute(query, (name, response, date))
                    conn.commit()

                    obj = {
                        'name': body.get('name'),
                        'id': int(cur.fetchone()[0])
                    }
                    self.addRabbitmq(obj)

                    cur.close()

                    return self.send_response('Dado inserido na fila com sucesso!', False, 200)

                except (Exception, psycopg2.DatabaseError) as error:
                    return self.send_response(error, True, HTTPStatus.INTERNAL_SERVER_ERROR)
                finally:
                    if conn is not None:
                        conn.close()
            else:
                return self.send_response('Nenhum dado foi fornecido', True, HTTPStatus.BAD_REQUEST)

        except JSONDecodeError as error:
            return self.send_response('Os dados informados não é do tipo JSON válido', True, HTTPStatus.BAD_REQUEST)
