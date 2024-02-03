import os

from simplegmail import Gmail
import sqlalchemy
from simplegmail.query import construct_query
from simplegmail import label
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

Base = sqlalchemy.orm.declarative_base()

load_dotenv("../.env")


class Mail(Base):
    __tablename__ = 'mail'

    message_id = Column(String, primary_key=True)
    thread_id = Column(String)
    sender = Column(String)
    recipient = Column(String)
    subject = Column(String)
    date = Column(String)
    message = Column(String)
    # labels = Column(String)


# host=localhost port=5432 dbname=cdc user=postgres password=xxxxxxx sslmode=prefer connect_timeout=10
# engine = create_engine('postgresql://postgres:karthik@localhost:5432/mail')
# Session = sessionmaker(bind=engine)
# session = Session()

try:
    engine = create_engine(os.getenv("DB_URI"))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(e)


gmail = Gmail()



# messages = gmail.get_unread_messages(query=construct_query(query_params))


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


result = session.query(Mail).all()
i = 0
for row in result:
    i+=1
    print("To: " + row.recipient)
    print("From: " + row.sender)
    print("Subject: " + row.subject)
    print("Date: " + row.date)
    print("Thread ID: " + row.thread_id)
    print("Message ID: " + row.message_id)
    # print("Message: " + row.message)
    # print("Labels: " + row.labels)
print(i)
