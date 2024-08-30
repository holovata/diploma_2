# database/db_vectorize.py
import ollama
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_community.llms import Ollama
import chromadb
import os
import uuid
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings)
from database.db_select import get_all_papers
from langchain_community.embeddings import HuggingFaceEmbeddings
from CONFIG import config
import shutil


def create_chroma_index():
    collection_name = 'papers_collection'

    # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # embedding_function = HuggingFaceEmbeddings(
    #    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        # model_name="bert-base-multilingual-cased")

    print("Fetching papers from database...")
    papers = get_all_papers()
    print(f"Number of papers fetched: {len(papers)}")

    # if len(papers) > 0:
    #    print("Sample paper:", papers[0])

    texts = [paper[4] for paper in papers]
    # print(f"Sample text: {texts[0] if texts else 'No texts available'}")
    print(f"Total texts: {len(texts)}")

    ids = [str(uuid.uuid4()) for _ in papers]
    # print(f"Sample ID: {ids[0] if ids else 'No IDs available'}")
    print(f"Total IDs: {len(ids)}")

    metadatas = [{
        'name': paper[1],
        'source': paper[1],
        'authors': paper[2],
        'url': paper[3],
        'abstract': paper[4],
        'keyword': paper[5],
        'categories': paper[6],
        'year': paper[7],
        'eprint': paper[8]
    } for paper in papers]
    # print(f"Sample metadata: {metadatas[0] if metadatas else 'No metadata available'}")
    print(f"Total metadata items: {len(metadatas)}")

    print("Initializing vector store...")
    # Определяем путь к директории chroma_store относительно текущего файла
    chroma_store_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chroma_store'))
    vectorstore = Chroma.from_texts(texts=texts, embedding=config.embedding_function,
                                    collection_name=collection_name, metadatas=metadatas,
                                    ids=ids, persist_directory=chroma_store_path)

    print("Vector store initialized.", chroma_store_path)
    documents = vectorstore.get()['documents']
    print(f"Number of documents in vector store: {len(documents)}")
    # if len(documents) > 0:
    #     print("Sample document:", documents[0])

    '''vectordb = Chroma(persist_directory=chroma_store_path, embedding_function=config.embedding_function, collection_name=collection_name)

    print("Vector store initialized AGAIN.",chroma_store_path)

    documents = vectordb.get()['documents']
    print(f"Number of documents in vector store: {len(documents)}")'''

    # return vectorstore, embedding_function


# create_chroma_index()

def clear_chroma_store(chroma_store_path):
    if os.path.exists(chroma_store_path):
        shutil.rmtree(chroma_store_path)
        print(f"Directory {chroma_store_path} has been cleared.")
    else:
        print(f"Directory {chroma_store_path} does not exist.")
    os.makedirs(chroma_store_path)
    print(f"Directory {chroma_store_path} has been created.")


# clear_chroma_store(chroma_store_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chroma_store')))

# Additional example usage
def search_chroma_index(query, vectorstore, top_k):
    # vectorstore = create_chroma_index()
    response = vectorstore.similarity_search(query=query, k=top_k)
    metadatas = [doc.metadata for doc in response]
    # distances = [doc.distance for doc in response]
    return metadatas
