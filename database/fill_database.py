import datetime
from database.db_create import create_tables
from database.db_select import get_all_papers
from database.db_clear import clear_table
from database.db_fetch_and_store import fetch_and_store_papers


def main():
    create_tables()

    # Очистка таблицы перед вставкой новых данных
    clear_table("keyword_papers_list")
    print("begin fetching", datetime.datetime.now())
    # Получение и вставка данных из arXiv по ключевому слову
    keyword = "machine learning"  # Измените на нужное ключевое слово
    fetch_and_store_papers(keyword, max_results=200)

    keyword = "computation and language"  # Измените на нужное ключевое слово
    fetch_and_store_papers(keyword, max_results=200)

    keyword = "artificial intelligence"  # Измените на нужное ключевое слово
    fetch_and_store_papers(keyword, max_results=1000)

    keyword = "finance"  # Измените на нужное ключевое слово
    fetch_and_store_papers(keyword, max_results=200)

    keyword = "biology"  # Измените на нужное ключевое слово
    fetch_and_store_papers(keyword, max_results=200)
    print("end fetching", datetime.datetime.now())

# main()