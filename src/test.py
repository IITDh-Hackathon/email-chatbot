from textual.app import App, ComposeResult
from textual.widgets import Static,Collapsible, Footer, Label, Markdown


class HorizontalLayoutExample(App):
    CSS_PATH = "grid.tcss"
    def compose(self) -> ComposeResult:
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")
        
class MainApp(App):
    
    def compose(self)->ComposeResult:
        yield HorizontalLayoutExample()
    


if __name__ == "__main__":
    app = MainApp()
    app.run()