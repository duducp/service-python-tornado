import pika
import psycopg2
import datetime
import json

from app import config

from json import JSONDecodeError
from http import HTTPStatus
from handler.cors import CorsHandler
from app.database import database


class PostPublicSourcesQuery(CorsHandler):
    def send_response(self, message, error=False, status=200):
        self.set_status(status)
        self.write({'status: ': status, 'error: ': error, 'msg: ': message})

    def send_to_rabbitmq(self, obj):
        try:
            _queue = 'request-tj-sp'

            # conecta ao rabbitmq
            credentials = pika.PlainCredentials(config.RMQ_USER, config.RMQ_PASSWORD)
            param = pika.ConnectionParameters(host=config.RMQ_HOST, credentials=credentials)

            connection = pika.BlockingConnection(param)
            channel = connection.channel()

            # cria a fila
            channel.queue_declare(queue=_queue)

            # tratamento da mensagem
            message_rabbit_mq = json.dumps(obj)

            # envia a mensagem para a fila
            channel.basic_publish(exchange='', routing_key=_queue, body=message_rabbit_mq)

            connection.close()
        except Exception as error:
            return self.send_response('Erro ao adicionar objeto a fila', False, HTTPStatus.INTERNAL_SERVER_ERROR)

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
                    self.send_to_rabbitmq(obj)

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
