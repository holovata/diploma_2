from langchain_community.llms import Ollama
from langchain_community.vectorstores.chroma import Chroma
import os
from CONFIG import config
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langsmith import Client
from uuid import uuid4

unique_id = uuid4().hex[0:8]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough - {unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"

client = Client()


def debug_log(message):
    print(f"[DEBUG] {message}")


def check_chroma_connection(persist_dir, collection_name='papers_collection'):
    try:
        debug_log("Checking Chroma connection")
        vectordb = Chroma(persist_directory=persist_dir, embedding_function=config.embedding_function,
                          collection_name=collection_name)

        # Attempt to count the number of documents in the collection
        documents = vectordb.get()['documents']
        debug_log(f"Number of documents in the collection '{collection_name}': {len(documents)}")
        return f"Connection successful. Number of documents: {len(documents)}"

    except Exception as e:
        debug_log(f"Failed to connect to Chroma vector store: {e}")
        return "Failed to connect to Chroma vector store."


def process_query(query, persist_dir=r"C:\Work\mi41\DIPLOM_99\diplom_fix\chroma_store"):
    try:
        debug_log(f"Persist directory: {persist_dir}")
        collection_name = 'papers_collection'

        debug_log("Initializing Chroma vector store")
        vectordb = Chroma(persist_directory=persist_dir, embedding_function=config.embedding_function,
                          collection_name=collection_name)

        # documents = vectordb.get()['documents']
        # if len(documents) > 0:
        #     print("Sample document:", documents[0])

        # debug_log("Similarity search")
        # result = vectordb.similarity_search(query, k=2)

        # debug_log("Creating retriever")
        retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        # debug_log(f"Retrieving documents for query: {query}")
        retrieved_docs = retriever.invoke(query)
        # debug_log(f"Retrieved documents: {retrieved_docs}")

        debug_log("Initializing LLM")
        llm = Ollama(model="qwen:4b")

        prompt = """
            You are an AI helper-assistant that guides scientists through an existing database with arxiv.org articles.
            1. Use ONLY the following pieces of context to answer the question at the end.
            2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.
            3. Keep the answer crisp and limited to 2 or 3 sentences for each article.
            4. When mentioning articles, try to provide more information about the articles. Author(s) and the link are a bare minimum.
            5. If you are asked to provide a certain number of articles, provide a list of that exact number of articles from the provided context.

            Context: {context}

            Question: {question}

            Helpful Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)

        llm_chain = LLMChain(
            llm=llm,
            prompt=QA_CHAIN_PROMPT,
            callbacks=None,
            verbose=True)

        document_prompt = PromptTemplate(
            input_variables=["page_content", "source"],
            template="Context:\ncontent:{page_content}\nsource:{source}",
        )

        combine_documents_chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_variable_name="context",
            document_prompt=document_prompt,
            callbacks=None,
        )

        qa = RetrievalQA(
            combine_documents_chain=combine_documents_chain,
            verbose=True,
            retriever=retriever,
            return_source_documents=True,
        )

        result = qa(query)

        return result["result"]

    except RuntimeError as e:
        debug_log(f"RuntimeError: {e}")
        debug_log("There was an issue with the vector store. Please check the persist directory and files.")
        return "An error occurred while processing the query."


def main():
    persist_dir = r"C:\Work\mi41\DIPLOM_99\diplom_fix\chroma_store"
    connection_status = check_chroma_connection(persist_dir)
    print(connection_status)

    if "Failed" in connection_status:
        return

    query = input("\nQuery: ")
    debug_log(f"Processing new query: {query}")
    answer = process_query(query, persist_dir)
    print(answer)

'''    while True:
        query = input("\nQuery: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue
        debug_log(f"Processing new query: {query}")
        answer = process_query(query, persist_dir)
        print(answer)'''


if __name__ == "__main__":
    main()
