#!/usr/bin/python

import psycopg2
from config.database import database

def createTables():
    conn = None
    try:
        params = database()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tb_tj_sp (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                response TEXT,
                date DATE NOT NULL
            )
        """)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    createTables()
