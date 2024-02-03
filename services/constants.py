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

IS_EVENT_PROMPT = """
You are a event classifying system and you have this information - {}. if the given information is not an event then reply 'no', else give the available event details in given format and if there is a gmeet link in the information keep the event_venue as online, if any one of the details are missing fill it as not available
	{{
	   event_name:
	   event_date:
	   event_time:
	   event_venue:
	}} 
"""