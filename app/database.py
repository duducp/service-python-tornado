from app import config


def database():
    return {
        "database": config.DB_DATABASE,
        "user": config.DB_USER,
        "password": config.DB_PASSWORD,
        "host": config.DB_HOST,
        "port": config.DB_PORT
    }