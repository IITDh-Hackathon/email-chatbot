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
You are a event classifying system and you have this information: 
{mail_chunk}

Give the academic event details in given format (strictly given json) and if there is a gmeet link in the information keep the event_venue as online, if any one of the details are missing fill it as not available
event_date format is yyyy-mm-dd strictly. event_time should follow 24hour format. example 13:16. 
	{{
	   "event_name":"",
	   "event_date":"",
	   "event_time":"",
	   "event_venue":
	}} 
"""

EVENT_CLASSIFIER_PROMPT = """You are a event classfier. You should only answer yes/no strictly.
 You should classfify the received email :
 {mail_chunk} 
 
 as yes, if the above email contains any talk/workshop/online meets/meetup or any upcoming fest related information. 
 Specifically lookout for online trainings, Annual progress seminar(APS), Seminars, Pre-synopsis, research related and personal meetings. 
"""

CHUNK_SIZE = 2500
CHUNK_OVERLAP = 100