from textual.app import App, ComposeResult
from textual.widgets import Static,Collapsible, Footer, Label, Markdown, DataTable, TextArea
from textual.containers import ScrollableContainer, Vertical

LETO = """\
# Duke Leto I Atreides

Head of House Atreides."""

JESSICA = """
# Lady Jessica

Bene Gesserit and concubine of Leto, and mother of Paul and Alia.
"""

PAUL = """
# Paul Atreides

Son of Leto and Jessica.
"""

Rows=[
    ("Event" , "Time"),
    ("Event 1", "10:00 Feb 20 2021"),
    ("Event 2", "11:00 Feb 20 2021"),
    ("Event 3", "12:00 Feb 20 2021")
]

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
        with Collapsible(collapsed=False, title="Leto"):
            yield Label(LETO)
        yield Collapsible(Markdown(JESSICA), collapsed=False, title="Jessica")
        with Collapsible(collapsed=True, title="Paul"):
            yield Markdown(PAUL)

    def action_collapse_or_expand(self, collapse: bool) -> None:
        for child in self.walk_children(Collapsible):
            child.collapsed = collapse

class ChatResponse(Static):
    def compose(self) -> ComposeResult:
        with Vertical():
            with ScrollableContainer():
                yield Static("Ask Bot", id="chat-bot-response-button")
                yield Static("Loading...", id="chat-bot-response")

    def on_mount(self) -> None:
        pass

class ChatInput(Static):
    BINDINGS = [
        ("Enter", "send_message", "Send Message"),
    ]
    def compose(self) -> ComposeResult:
        with Vertical():
            yield TextArea(id="chat-input")

    def on_mount(self) -> None:
        pass

    def action_send_message(self) -> None:
        pass

class ChatComponent(Static):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield TextArea(id="chat-input")
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