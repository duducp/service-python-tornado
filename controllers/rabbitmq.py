import json
import pika


def addRabbitmq(obj: dict):
    try:
        # Conecta
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Cria a fila
        channel.queue_declare(queue='request-tj-sp')

        # trata a mensagem recebida
        message_rabbit_mq = json.dumps(obj)

        # envia a mensagem para a fila
        channel.basic_publish(exchange='', routing_key='request-tj-sp', body=message_rabbit_mq)

        connection.close()
        return True
    except Exception as error:
        return error
