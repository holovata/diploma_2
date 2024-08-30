# database/db_clear.py

import psycopg2
from database.db_config import get_db_connection


def clear_table(table_name):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')
                connection.commit()
                print(f"Table {table_name} has been cleared.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while clearing table {table_name}:", error)

# clear_table('keyword_papers_list')
