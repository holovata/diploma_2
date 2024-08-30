# database/db_vectorize.py

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import chromadb
import uuid
from sentence_transformers import SentenceTransformer
from .db_select import get_all_papers


def create_chroma_index():
    # Инициализация ChromaDB клиента
    client = chromadb.Client()
    collection_name = 'papers_collection'

    '''# Проверка существования коллекции
    if collection_name in client.list_collections():
        collection = client.get_collection(collection_name)
    else:
        collection = client.create_collection(collection_name)'''

    collection = client.get_or_create_collection(collection_name)
    # Загрузка предобученной модели для преобразования текстов в векторы
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Извлечение данных из базы данных
    papers = get_all_papers()

    # Преобразование аннотаций в векторы
    texts = [paper[4] for paper in papers]  # Аннотации статей
    vectors = model.encode(texts)

    # Создание списков для ID, векторов и метаданных
    ids = [str(uuid.uuid4()) for _ in papers]
    embeddings = vectors.tolist()
    metadatas = [{
        'name': paper[1],
        'authors': paper[2],
        'url': paper[3],
        'abstract': paper[4],  # Сохранение аннотации в метаданных
        'keyword': paper[5],
        'categories': paper[6],
        'year': paper[7],
        'eprint': paper[8]
    } for paper in papers]

    # Добавление данных в коллекцию
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

    print("Vector index has been created and stored in ChromaDB.")

    return client, collection, papers


def search_chroma_index(query, top_k=5):
    # Инициализация ChromaDB клиента
    client = chromadb.Client()
    collection = client.get_collection('papers_collection')

    # Загрузка предобученной модели для преобразования текстов в векторы
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Преобразование запроса в вектор
    query_vector = model.encode([query])

    # Поиск ближайших соседей
    response = collection.query(query_embeddings=query_vector, n_results=top_k)

    # Возвращение результатов поиска
    if 'metadatas' in response and 'distances' in response:
        metadatas = response['metadatas'][0]
        distances = response['distances'][0]
        return metadatas, distances
    else:
        return [], []
