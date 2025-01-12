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
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

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
        retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})

        # debug_log(f"Retrieving documents for query: {query}")
        # retrieved_docs = retriever.invoke(query)
        # debug_log(f"Retrieved documents: {retrieved_docs}")

        debug_log("Initializing LLM")
        llm = Ollama(model="qwen:4b")

        # Define the custom prompt template suitable for the Phi-3 model
        qna_prompt_template = """<|system|>
        You have been provided with the context and a question, try to find out the answer to the question only using the context information. If the answer to the question is not found within the context, return "I dont know" as the response.<|end|>
        <|user|>
        Context:
        {context}

        Question: {query}<|end|>
        <|assistant|>"""
        PROMPT = PromptTemplate(
            template=qna_prompt_template, input_variables=["context", "question"]
        )

        # Define the QNA chain
        chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT)

        context = retriever.get_relevant_documents(query)
        print(context)

        answer = (chain({"input_documents": context, "query": query}, return_only_outputs=True))['output_text']
        answer = (answer.split("<|assistant|>")[-1]).strip()
        return answer

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

if __name__ == "__main__":
    main()
