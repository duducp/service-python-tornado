import os

TORNADO_HOST = str(os.environ.get("HOST", 'localhost'))
TORNADO_PORT = int(os.environ.get("PORT", 8000))

RMQ_USER = str(os.environ.get("RMQ_USER", 'guest'))
RMQ_PASSWORD = str(os.environ.get("RMQ_PASSWORD", 'guest'))
RMQ_HOST = str(os.environ.get("RMQ_HOST", 'localhost'))
RMQ_PORT = int(os.environ.get("RMQ_PORT", 5762))

IOLOOP_TIMEOUT = int(os.environ.get("IOLOOP_TIMEOUT", 500))

DB_DATABASE = str(os.environ.get("DB_DATABASE", 'pg_cedro'))
DB_USER = str(os.environ.get("DB_DATABASE", 'postgres'))
DB_PASSWORD = str(os.environ.get("DB_DATABASE", 'edinei6'))
DB_HOST = str(os.environ.get("DB_DATABASE", 'localhost'))
DB_PORT = int(os.environ.get("PORT", 5432))
