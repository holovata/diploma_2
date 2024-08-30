# database/db_fetch_and_store.py

import arxiv
from database.db_insert import insert_paper

def fetch_and_store_papers(keyword, max_results=5):
    client = arxiv.Client()
    search = arxiv.Search(
        query=keyword,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    try:
        results = list(client.results(search))
        actual_results = min(max_results, len(results))

        for result in results[:actual_results]:
            name = result.title
            authors = ', '.join([author.name for author in result.authors])
            url = result.entry_id
            abstract = result.summary
            categories = ', '.join(result.categories)
            year = result.updated.year
            eprint = result.entry_id

            insert_paper(name, authors, url, abstract, keyword, categories, year, eprint)

    except Exception as e:
        print(f"Error during fetching and storing papers: {e}")


'''keyword = "machine learning"  # Измените на нужное ключевое слово
fetch_and_store_papers(keyword, max_results=20)'''