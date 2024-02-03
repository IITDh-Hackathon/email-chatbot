COLLECTION_NAME = "mail_embeddings"
SIMILARITY_SEARCH_TYPE = "l2"

IS_VALUABLE_PROMPT = """
You are classifying a chunk/part of mail as a usable part. Carefully check the text and make sure it is not completely useless. like
"you are receiving this email because you are subscribed to our newsletter" or "unsubscribe" or "click here to unsubscribe" etc.
or lines having more > or < characters or having sentences like "On <date> <time>, <name> wrote:".
also make sure it is not a signature or a disclaimer.
Even if you are not sure, it is better to mark it as valuable.

Mail chunk: 
{mail_chunk}

Give output as "true" or "false" without quotes.

"""