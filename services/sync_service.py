import os
import uuid

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
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
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

def add_to_db(emails):
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
        session.add(mail)
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
        "newer_than": (1, "day"),
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
    add_to_db(latest_emails)
    
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

def store_embeddings(chunks, embeddings):
    new_chunks = []
    for chunk in chunks:
        if is_valuable(chunk):
            new_chunks.append(chunk)
    print("this ",len(new_chunks))
    collection = chromadb_instance.get_or_create_collection(COLLECTION_NAME,
                                                        metadata={"hnsw:space": SIMILARITY_SEARCH_TYPE})
    ids = [str(uuid.uuid1()) for _ in range(len(new_chunks))]
    for i, chunk in enumerate(new_chunks):
        collection.add(documents=chunk, embeddings=embeddings[i], ids=[ids[i]])
    return ids



def get_db_emails():
    all_emails = session.query(Mail).all()
    print_only(all_emails)
    return all_emails

def get_latest_email():
    return session.query(Mail).order_by(Mail.date.desc()).first()

if __name__ == "__main__":
    make_db_session()
    make_chroma_session()
    gmail = Gmail()
    chunks = split_mail(get_latest_email().message)
    print(chunks)
    mail_embeddings = embed_mail(chunks)
    ids = store_embeddings(chunks, mail_embeddings)
    # print(mail_embeddings)
    # collection = chromadb_instance.get_or_create_collection(COLLECTION_NAME)
    # qe = embeddings.embed_query("when is the yoga session")

