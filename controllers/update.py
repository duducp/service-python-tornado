import json
import psycopg2
from json import JSONDecodeError

from config.database import database


def update(data):
    try:
        body = json.loads(data)

        if body:
            response = body.get('response')
            _id = body.get('id')

            if not response:
                print('A RESPONSE não foi informada')

            conn = None
            try:
                params = database()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()

                query = "UPDATE tb_tj_sp SET response = %s WHERE id = %s"
                cur.execute(query, (response, _id))
                conn.commit()
                cur.close()

                print('O id {} foi atualizado com sucesso'.format(_id))

            except (Exception, psycopg2.DatabaseError) as error:
                print('Erro ao conectar com o banco de dados')
            finally:
                if conn is not None:
                    conn.close()
        else:
            print('Nenhum dado foi fornecido')

    except JSONDecodeError as error:
        print('Os dados informados não é do tipo JSON válido')