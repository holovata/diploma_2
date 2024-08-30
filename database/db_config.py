# database/db_config.py

import psycopg2


def get_db_connection():
    connection = psycopg2.connect(
        database="newpapersdb",
        user="myuser",
        password="mypassword",
        host="127.0.0.1",
        port="5432",
        client_encoding='UTF8'
    )
    return connection
