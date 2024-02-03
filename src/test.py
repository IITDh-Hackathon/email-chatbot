from rich import print
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.text import Text
from rich.table import Table, Column
from rich.live import Live
from time import sleep


console = Console()
console.set_alt_screen(True)
console.clear()

layout = Layout()

logs_table = Table(Column("Logs"), expand=True)

layout.split_column(
    Layout(name="header", ratio=4),
    Layout(logs_table, name="body", ratio=6)
)

header = layout.get('header')

header.split_row(
    Layout(Panel(''), name="account-info"),
    Layout(Panel(''), name="bot-status-info")
)

live = Live(layout, refresh_per_second=1)
live.start()

for i in range(30):
    logs_table.add_row(f'Test line {i}.')

sleep(5)