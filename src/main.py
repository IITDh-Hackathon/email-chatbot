from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich import print
from rich.layout import Layout
from rich.console import Group
from typing import List
from utils.events import *
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.padding import Padding
import time

import os
print(os.getcwd())
from utils.llm_query import *

query = "Is there any talk on Knowledge production or creation of new knowledge scheduled?"
print(query_response(query))

console = Console()
# console.clear()

layout = Layout()

# Left Pane
left_pane = Layout(name="left", ratio=25)



# code for rich layout
layout = Layout()
# event_table = Table()
# event_table.add_column("ID")
# event_table.add_column("Description")
layout.split_row(
    Layout(name="left", ratio=27),
    Layout(name="middle", ratio=46),
    Layout(name="right", ratio=27),
)

def display_emails(emails: List[dict]):
    all_emails = []
    for email in emails:
        top = Text.assemble(f"{email['from']}       {email['time']}")
        middle = Text.assemble( f"{email['subject']}")
        bottom = Text.assemble( f"{email['preview']}")
        all_emails.append(Group(top, middle, bottom))
    layout["left"].update(Group(*all_emails))

def display_events(events: dict):
    event_table = Table(box=box.ROUNDED)
    event_table.title = "Upcoming Events"
    event_table.add_column("Event", width=20,style="cyan")
    event_table.min_width = 33
    event_table.add_column("Time", width=13,style="magenta")
    # for event, time in events.items():
    #     event_table.add_row(event, time)
    # with Live(event_table, refresh_per_second=4):
    #     for event, times in events.items():
    #         event_table.add_row(event, times)
    #         time.sleep(0.5)
    for event, time in events.items():
        event_table.add_row(event, time)
    layout["right"].update(event_table)


# def print_text(text):
#     for char in text:
#         # Print the character without buffering
#         print(char, end='', flush=True)
#         time.sleep(0.1)  # Adjust the sleep duration as needed


def start_console():
    # console.print(f'*** Email ChatBot ***',
    #               style="bold red ", justify="center")
    # # console.print('>' ,style = "italic underline blue on #ffffff")
    # console.print(
    #     '[italic][bold][#FF00FF]Bot :[/#FF00FF][/bold][/italic] Hey Welcome to Email Chatbot. How may I help you', )

    # print the above text with in the layout="middle"
    layout["middle"].update(
        console.print(
            "[bold]Center Text[/bold]", justify="center"
        )
    )

    # layout["middle"].update(
    #     console.print(
    #         '[italic][bold][#FF00FF]Bot :[/#FF00FF][/bold][/italic] Hey Welcome to Email Chatbot. How may I help you', )
    # )

dict = {
    "Event 1": "10:00 Feb 20 2021",
    "Event 2": "11:00 Feb 20 2021",
    "Event 3": "12:00 Feb 20 2021"
}
# print date and time in the right pane
# display_events(dict)

mails=[
    {
        "from": "email1",
        "subject": "subject1",
        "preview": "preview1",
        "time": "time1"
    },
    {
        "from": "email2",
        "subject": "subject2",
        "preview": "preview2",
        "time": "time2"
    },
    {
        "from": "email3",
        "subject": "subject3",
        "preview": "preview3",
        "time": "time3"
    }
]

events = get_events()
print(events)
# display_events(events)

# print_text("Hello World")
# print(layout)
