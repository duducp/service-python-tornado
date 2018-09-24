# https://blog.ateliedocodigo.com.br/primeiros-passos-com-rabbitmq-e-python-938fb0957019

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='request-tj-sp')

channel.basic_publish(exchange='',
                      routing_key='request-tj-sp',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()