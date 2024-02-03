from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich import print
from rich.layout import Layout
import time

console = Console()
console.clear()

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


def show_events(events: dict):
    event_table = Table()
    event_table.title = "Upcoming Events"
    event_table.add_column("Event", width=20,style="cyan")
    event_table.min_width = 33
    event_table.add_column("Time", width=13,style="magenta")
    # for event, time in events.items():
    #     event_table.add_row(event, time)
    with Live(event_table, refresh_per_second=4):
        for event, times in events.items():
            event_table.add_row(event, times)
            time.sleep(0.5)
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


# start_console()
# # print(layout)
# # create a object with __rich__ console__meth
# create a dict with key as eenvent and value as time
dict = {
    "Event 1": "10:00 Feb 20 2021",
    "Event 2": "11:00 Feb 20 2021",
    "Event 3": "12:00 Feb 20 2021"
}
# print date and time in the right pane
show_events(dict)


# print_text("Hello World")
print(layout)
