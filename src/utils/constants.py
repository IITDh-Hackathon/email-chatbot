COLLECTION_NAME = "mail_embeddings"
SIMILARITY_SEARCH_TYPE = "l2"

RAG_PROMPT = """
You are personal assistant that helps with email data. You are given context email data and asked to answer a question about the email.
Context:
{context}
Question: {question}
"""