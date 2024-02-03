import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI, ChatOpenAI
from langchain.schema import HumanMessage
import chromadb


def load_env():
    load_dotenv("../.env")

load_env()


from langchain_core.prompts import PromptTemplate

COLLECTION_NAME = "mail_embeddings"
SIMILARITY_SEARCH_TYPE = "l2"

RAG_PROMPT = """
You are personal assistant that helps with email data. You are given context email data and asked to answer a question about the email.
Context:
{context}
Question: {question}
"""

chromadb_instance = chromadb.PersistentClient(path="../chroma.db")
embeddings = OpenAIEmbeddings()
openai = OpenAI()
chat_openai = ChatOpenAI(model_name="gpt-4")
query_prompt = PromptTemplate(template=RAG_PROMPT, input_variables=["context", "question"])


def get_embedding(text: str):
    return embeddings.embed_query(text)


def similarity_search(query: str):
    query_embedding = get_embedding(query)
    collection = chromadb_instance.get_collection(COLLECTION_NAME)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=4,
    )
    return results

def query_response(query: str):
    context = similarity_search(query)
    llm = ChatOpenAI(model_name="gpt-4")
    output = query_prompt | llm
    response = output.invoke({"context": context, "question": query})
    return response.content

if __name__ == "__main__":
    query = "Is there any talk on Knowledge production or creation of new knowledge scheduled?"
    print(query_response(query))


