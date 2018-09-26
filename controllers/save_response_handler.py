import tornado.web
import tornado.escape
import psycopg2
import datetime
import json
import pika
import _thread

import time
from random import randrange

from config.database import database

class SaveResponseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
        self.set_header("X-XSS-Protection", "1; mode=block")

    def options(self):
        pass

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))

    def addRow(self, obj):
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
        except (Exception, psycopg2.DatabaseError) as error:
            self.write({'error: ': True, 'msg: ': error})


    def callbackGetRow(self, channel, method, header, body):
        print(" [x] Received %r" % body)
        time.sleep(randrange(0, 5))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def getRow(self):
        try:
            # Conecta
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            # Cria a fila
            channel.queue_declare(queue='request-tj-sp')  # depois mudar para response

            # número de mensagens a ser envia por vez
            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(self.callbackGetRow, queue='request-tj-sp')  # depois mudar para response

            channel.start_consuming()
        except (Exception, psycopg2.DatabaseError) as error:
            self.write({'error: ': True, 'msg: ': error})

    def post(self):
        conn = None
        try:
            params = database()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            data = tornado.escape.json_decode(self.request.body)

            name = data.get('name', '')
            response = data.get('response', '')
            date = datetime.datetime.now()

            if not name:
                return self.send_response({'error': True, 'msg': 'Por favor informe o NOME.'}, 400)

            query = "INSERT INTO tb_tj_sp (name, response, date) VALUES (%s, %s, %s) RETURNING id"
            cur.execute(query, (name, response, date))
            conn.commit()

            obj = {
                'name': data.get('name'),
                'id': int(cur.fetchone()[0])
            }

            cur.close()

            try:
                self.addRow(obj)
                self.send_response({'error': False, 'msg': 'Dado inserido na fila com sucesso!'})

                # self.getRow()
            except (Exception) as error:
                self.write({'error: ': True, 'msg: ': error})

        except (Exception, psycopg2.DatabaseError) as error:
            self.write({'error: ': True, 'msg: ': error})
        finally:
            if conn is not None:
                conn.close()
