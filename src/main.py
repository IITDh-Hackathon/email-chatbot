from textual.app import App, ComposeResult
from textual.events import Mount
from textual.widgets import Static,Collapsible, Footer, Label, Markdown, DataTable, TextArea, Button
from textual.containers import ScrollableContainer, Vertical
from textual.widgets import Static,Collapsible, Footer, Label, Markdown, DataTable
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from utils.events import *
from utils.llm_query import *



Rows=[("Event" , "Time")]

all_events = get_events()

all_mails = get_mails()
all_mails.sort(key=lambda x: x["time"], reverse=True)

for event in all_events:
    Rows.append((event["Event"],event["Time"]))

def shorten_text(text: str, max_length: int = 19) -> str:
    """Shorten text to max_length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + ".."

shortened_rows = [(shorten_text(row[0]),row[1]) for row in Rows]

Rows = shortened_rows

class TableApp(Static):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*Rows[0])
        table.add_rows(Rows[1:])

class CollapsibleApp(Static):
    """An example of collapsible container."""

    BINDINGS = [
        ("c", "collapse_or_expand(True)", "Collapse All"),
        ("e", "collapse_or_expand(False)", "Expand All"),
    ]

    def compose(self) -> ComposeResult:
        """Compose app with collapsible containers."""
        for mail in all_mails:
            with Collapsible(collapsed=True, title=mail["subject"]):
                yield Label(f"From: {mail['from']}      Time: {mail['time']}\n{mail['subject']}\n{mail['message']}\n")
                            

    def action_collapse_or_expand(self, collapse: bool) -> None:
        for child in self.walk_children(Collapsible):
            child.collapsed = collapse

class ResponseBox(Static):
    query = reactive("")
    
    def on_mount(self, event: Mount) -> None:
        self.update("Please enter a query above and click submit")

class ChatResponse(Static):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        text_display = self.query_one(ResponseBox)
        text_area = self.query_one(TextArea)
        input_text = text_area.text
        text_area.text = ""
        text_display.update(query_response(input_text))
    def compose(self) -> ComposeResult:
        with Vertical():
            with ScrollableContainer():
                yield TextArea(id="chat-input")
                yield Button("Submit Query", id="chat-bot-response-button")
                yield ResponseBox(id="chat-bot-response")

    def on_mount(self) -> None:
        pass

class ChatComponent(Static):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield ChatResponse()

    def on_mount(self) -> None:
        pass

class MainApp(App):
    CSS_PATH = "grid.tcss"
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Static("All Emails"),CollapsibleApp())
        yield Vertical(Static("Chat Bot"), ChatComponent(classes="box"))
        yield ScrollableContainer(Static("All Events"),TableApp())
        yield Footer()


if __name__ == "__main__":
    app = MainApp()
    app.run()