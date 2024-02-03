from simplegmail import Gmail
import sqlalchemy
from simplegmail.query import construct_query
from simplegmail import label
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 10.200.242.211:5432
Base = sqlalchemy.orm.declarative_base()


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
    engine = create_engine('postgresql://postgres:karthik@localhost:5432/mail')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(e)

# import sql aclchemy
# from sqlalchemy import create_engine

gmail = Gmail()

query_params = {
    "newer_than": (6, "day"),
    # "older_than": (1, "day"),
}

# messages = gmail.get_unread_messages(query=construct_query(query_params))


# retrieve latest emails from inbox
# def get_latest_emails(num_emails=10):
#     # get last `num_emails` emails from inbox
#     emails = gmail.get_messages(query='in:inbox')
#     # get the latest emails, up to the specified number
#     latest_emails = emails[:num_emails]
#     return latest_emails

# emails = gmail.get_messages(query=construct_query(query_params))

# for message in emails[0:2]:
#     print("To: " + message.recipient)
#     print("From: " + message.sender)
#     print("Subject: " + message.subject)
#     print("Date: " + message.date)
#     print("Thread ID: " + message.thread_id)
#     print("Message ID: " + message.id)
#     print("Message: " + message.plain)
#     # print("Labels: " + str(message.labels))

# for message in emails:
#     mail = Mail(
#         message_id=str(message.id),
#         thread_id=str(message.thread_id),
#         sender=message.sender,
#         recipient=message.recipient,
#         subject=message.subject,
#         date=message.date,
#         message=message.plain,
#         # labels=str(message.labels)
#     )
#     session.add(mail)
#     session.commit()

# for message in emails:
#     print("Type of message ID: ", type(message.id))
#     print("Type of thread ID: ", type(message.thread_id))
#     print("Type of sender: ", type(message.sender))
#     print("Type of recipient: ", type(message.recipient))
#     print("Type of subject: ", type(message.subject))
#     print("Type of date: ", type(message.date))
#     print("Type of message: ", type(message.plain))

# query from db

result = session.query(Mail).all()

for row in result:
    print("To: " + row.recipient)
    print("From: " + row.sender)
    print("Subject: " + row.subject)
    print("Date: " + row.date)
    print("Thread ID: " + row.thread_id)
    print("Message ID: " + row.message_id)
    
    # print("Message: " + row.message)
    # print("Labels: " + row.labels)
