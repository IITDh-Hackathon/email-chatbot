from textual.app import App, ComposeResult
from textual.widgets import Static,Collapsible, Footer, Label, Markdown, DataTable
from textual.containers import ScrollableContainer

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


class MainApp(App):
    CSS_PATH = "grid.tcss"
    def compose(self) -> ComposeResult:
        yield Footer()
        yield ScrollableContainer(Static("All Emails"),CollapsibleApp())
        yield Static("Two", classes="box")
        yield ScrollableContainer(Static("All Events"),TableApp())
        

if __name__ == "__main__":
    app = MainApp()
    app.run()