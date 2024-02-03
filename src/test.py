from textual.app import App, ComposeResult
from textual.widgets import Static,Collapsible, Footer, Label, Markdown


class HorizontalLayoutExample(App):
    CSS_PATH = "grid.tcss"
    def compose(self) -> ComposeResult:
        yield Footer()
        yield ScrollableContainer(Static("All Emails"),CollapsibleApp())
        yield Static("Two", classes="box")
        yield ScrollableContainer(Static("All Events"),TableApp())
        

if __name__ == "__main__":
    app = MainApp()
    app.run()