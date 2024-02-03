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


gmail = Gmail()

def sync_emails():
    # messages = gmail.get_unread_messages(query=construct_query(query_params))
    query_params = {
        "newer_than": (2, "day"),
    }
    emails = gmail.get_messages(query=construct_query(query_params))

    for message in emails:
        mail = Mail(
            message_id=str(message.id),
            thread_id=str(message.thread_id),
            sender=message.sender,
            recipient=message.recipient,
            subject=message.subject,
            date=message.date,
            message=message.plain,
            # labels=str(message.labels)
        )
        session.add(mail)
        session.commit()    


def get_emails():
    return session.query(Mail).all()

if __name__ == "__main__":
    load_env()
    make_db_session()
    print(get_emails())

