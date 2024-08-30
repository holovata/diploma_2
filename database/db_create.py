# database/db_create.py

import psycopg2
from .db_config import get_db_connection

def create_tables():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Создание новой таблицы keyword_papers_list
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS keyword_papers_list (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        authors TEXT NOT NULL,
                        url TEXT NOT NULL,
                        abstract TEXT NOT NULL,
                        keyword TEXT NOT NULL,
                        categories TEXT NOT NULL,
                        year INTEGER NOT NULL,
                        eprint TEXT NOT NULL
                    )
                ''')

                connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating tables:", error)
