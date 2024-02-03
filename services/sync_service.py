import os

from simplegmail import Gmail
import sqlalchemy
from simplegmail.query import construct_query
from simplegmail import label
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from langchain.embeddings import Embeddings

from dotenv import load_dotenv

Base = sqlalchemy.orm.declarative_base()

# global variables
session = None

def load_env():
    load_dotenv("../.env")

def make_db_session():
    global session
    try:
        engine = create_engine(os.getenv("DB_URI"))
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
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
    print("Latest email id: ", latest_email_id)
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
        



def get_db_emails():
    all_emails = session.query(Mail).all()
    print_only(all_emails)
    return all_emails

if __name__ == "__main__":
    load_env()
    make_db_session()
    gmail = Gmail()
    sync_emails(gmail)
    get_db_emails()