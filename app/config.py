import os

APP_HOST = str(os.environ.get("HOST", 'localhost'))
APP_PORT = int(os.environ.get("PORT", 8000))

DB_DATABASE = str(os.environ.get("DB_DATABASE", 'pg_cedro'))
DB_USER = str(os.environ.get("DB_DATABASE", 'postgres'))
DB_PASSWORD = str(os.environ.get("DB_DATABASE", 'edinei6'))
DB_HOST = str(os.environ.get("DB_DATABASE", 'localhost'))
DB_PORT = int(os.environ.get("PORT", 5432))
