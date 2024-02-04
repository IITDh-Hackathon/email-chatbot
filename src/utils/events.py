import psycopg2
from psycopg2 import sql
import json

# Replace these values with your PostgreSQL connection details
dbname = "mail"
user = "postgres"
password = "karthik"
host = "localhost"
port = "5432"

# Specify the table name you want to read from
def get_events():
    table_name = "event"

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

    # Create a cursor
    cursor = conn.cursor()

    # Construct and execute a SQL query to select data from the table
    query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the fetched data
    events = []
    count = 0
    for my_tuple in rows:
        if count == 10:
            break
        result_dict = {
        "Event": my_tuple[1],
        "Time": my_tuple[3] +"-"+ my_tuple[2]
        }
        events.append(result_dict)
        count += 1
    cursor.close()
    conn.close()
    return events

# Close the cursor and connection
# print(json.dumps(events))

def get_mails():
    table_name = "mail"

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

    # Create a cursor
    cursor = conn.cursor()

    # Construct and execute a SQL query to select data from the table
    query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the fetched data
    emails = []
    count = 0
    for my_tuple in rows:
        if count == 15:
            break
        result_dict = {
        "from": my_tuple[2],
        "time": my_tuple[5],
        "subject": my_tuple[4],
        "message": my_tuple[6]
        }
        emails.append(result_dict)
        count += 1
    cursor.close()
    conn.close()
    print(emails)
    return emails

get_mails()