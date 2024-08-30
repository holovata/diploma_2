# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings)
# from langchain.embeddings.openai import OpenAIEmbeddings
# from chromadb.db.base import UniqueConstraintError
# from chromadb.utils import embedding_functions
# from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

class Config:
    # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # embedding_function = OpenAIEmbeddings()
    # embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="Huffon/sentence-klue-roberta-base")
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    # chroma_store_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chroma_store'))

config = Config()