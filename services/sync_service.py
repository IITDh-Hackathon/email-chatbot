import os
import uuid
import json
import time

from simplegmail import Gmail
import sqlalchemy
from simplegmail.query import construct_query
from simplegmail import label
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain_openai import OpenAI, ChatOpenAI
from langchain.schema import HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from  constants import *

from langchain_core.prompts import PromptTemplate

# from langchain.embeddings import Embeddings

from dotenv import load_dotenv

Base = sqlalchemy.orm.declarative_base()

def load_env():
    load_dotenv("../.env")

load_env()

# global variables
session = None
chromadb_instance = None
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
valueble_prompt = PromptTemplate(input_variables=["mail_chunk"],template=IS_VALUABLE_PROMPT)


def make_db_session():
    global session
    try:
        engine = create_engine(os.getenv("DB_URI"))
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        print(e)

def make_chroma_session():
    global chromadb_instance
    try:
        chromadb_instance = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH"))

    except Exception as e:
        print(e)



# table for mails in the database
class Mail(Base):
    __tablename__ = 'mail'

    message_id = Column(String, primary_key=True)
    thread_id = Column(String)
    sender = Column(String)
    recipient = Column(String)
    subject = Column(String)
    date = Column(String)
    message = Column(String)

    def __repr__(self):
        return f"<Mail(message_id={self.message_id}, sender={self.sender}, recipient={self.recipient}, subject={self.subject}, date={self.date}, message={self.message})>"

class Event(Base):
    __tablename__ = 'event'

    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(String)
    event_time = Column(String)
    event_venue = Column(String)
    sender = Column(String)
    
    def __repr__(self):
        return f"<Event(event_name={self.event_name}, event_date={self.event_date}, event_time={self.event_time}, event_venue={self.event_venue})>"
    
def add_to_db(emails):
    ret = []
    for email in emails:
        mail = Mail(
            message_id=email.id,
            thread_id=email.thread_id,
            sender=email.sender,
            recipient=email.recipient,
            subject=email.subject,
            date=email.date,
            message=email.plain,
            # labels=str(email.labels)
        )
        ret.append(mail)
        session.add(mail)
        session.commit()
    return ret

def add_event_to_db(event):
    print(event)
    event = Event(
        event_name=event["event_name"],
        event_date=event["event_date"],
        event_time=event["event_time"],
        event_venue=event["event_venue"],
        sender=event["sender"]
    )
    session.add(event)
    session.commit()
#get lastest added record to the database
def get_latest_email_id():
    try:
        return session.query(Mail).order_by(Mail.message_id.desc()).first().message_id
    except Exception as e:
        print(e)
        return None

def sync_emails(gmail_client : Gmail):
    query_params = {
        "newer_than": (4, "day"),
    }
    emails = gmail_client.get_messages(query=construct_query(query_params))
    latest_email_id = get_latest_email_id()
    # print("Latest email id: ", latest_email_id)
    #only add new emails to the database
    latest_emails=[]
    for email in emails:
        if email.id == latest_email_id:
            break
        latest_emails.append(email)
    return add_to_db(latest_emails)

    
def print_only(emails):
    for email in emails:
        print("Message ID: ", email.message_id)
        # print("Thread ID: ", email.thread_id)
        # print("Sender: ", email.sender)
        # print("Recipient: ", email.recipient)
        print("Subject: ", email.subject)
        print("Date: ", email.date)
        #get labels
        print("Labels: ", email.labels)
        



def split_mail(mail):
    return text_splitter.split_text(mail)

def embed_mail(chunks):
    return embeddings.embed_documents(chunks)

def is_valuable(chunk):
    try:
        prompt = valueble_prompt
        llm = OpenAI(temperature=0.0)
        output = prompt | llm
        response = output.invoke({"mail_chunk": chunk})
        response = response.strip().lower()
        print(response)
        if "true" in response:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def classify_event(mail_str):
    try:
        prompt = PromptTemplate(input_variables=["mail_chunk"],template=EVENT_CLASSIFIER_PROMPT)
        llm = ChatOpenAI(model_name="gpt-4")
        output = prompt | llm
        response = output.invoke({"mail_chunk": mail_str})
        response = response.content
        response = response.strip().lower()
        print(response)
        if "yes" in response:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def get_event_data(mail_str,sender):
    try:
        prompt = PromptTemplate(input_variables=["mail_chunk"],template=IS_EVENT_PROMPT)
        llm = ChatOpenAI(model_name="gpt-4")
        output = prompt | llm
        response = output.invoke({"mail_chunk": mail_str})
        # response = response.strip().lower()
        response=response.content
        response = response.strip().lower()
        print(response)
        json_response = json.loads(response)
        json_response["sender"] = sender
        add_event_to_db(json_response)
        return True
    except Exception as e:
        print(e)
        return False


def store_embeddings(chunks, embeddings):
    collection = chromadb_instance.get_or_create_collection(COLLECTION_NAME,
                                                        metadata={"hnsw:space": SIMILARITY_SEARCH_TYPE})
    ids = [str(uuid.uuid1()) for _ in range(len(chunks))]
    for i, chunk in enumerate(chunks):
        collection.add(documents=chunk, embeddings=embeddings[i], ids=[ids[i]])
    return ids



def get_db_emails():
    all_emails = session.query(Mail).all()
    # print_only(all_emails)
    return all_emails[10]

def get_latest_email():
    return session.query(Mail).order_by(Mail.date.desc()).first()

def refine_chunks(chunks, mail):
    mail_metadata = "From: " + mail.sender + "\n" + "To: " + mail.recipient + "\n" + "Subject: " + mail.subject + "\n" + "Date: " + mail.date + "\n\n Message: \n"
    new_chunks = []
    event_chunks = []
    for chunk in chunks:
        if is_valuable(chunk):
            event_chunks.append(chunk)
            chunk = mail_metadata + chunk
            new_chunks.append(chunk)
    return new_chunks,event_chunks

def main_loop():
    new_mails = sync_emails(gmail)
    for mail in new_mails:
        print(mail)
        chunks = split_mail(mail.message)
        chunks,event_chunks = refine_chunks(chunks, mail)
        mail_string = ' '.join(event_chunks)
        if classify_event(mail_string):
            get_event_data(mail_string,mail.sender)
        mail_embeddings = embed_mail(chunks)
        store_embeddings(chunks, mail_embeddings)

if __name__ == "__main__":
    make_db_session()
    make_chroma_session()
    gmail = Gmail(
        client_secret_file="../client_secret.json",
        creds_file="../gmail_token.json",
    )
    while True:
        main_loop()
        time.sleep(60)
