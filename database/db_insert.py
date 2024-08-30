# database/db_insert.py

import psycopg2
from .db_config import get_db_connection

def insert_paper(name, authors, url, abstract, keyword, subjects, year, eprint):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Проверка наличия записи с таким же URL
                cursor.execute('SELECT COUNT(*) FROM keyword_papers_list WHERE url = %s', (url,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO keyword_papers_list (name, authors, url, abstract, keyword, subjects, year, eprint) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (name, authors, url, abstract, keyword, subjects, year, eprint))

                    connection.commit()
                else:
                    print(f"Статья с URL {url} уже существует в базе данных.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data:", error)
