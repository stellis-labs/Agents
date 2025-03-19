# logger.py
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

console = Console()

def log(message, style="bold blue", log_to_file=True, print_to_console=False):
    """Log messages to a logfile and optionally print them to the console."""
    
    if print_to_console:
        console.print(Panel(Text(message, style=style)))

    # Always log to a file
    if log_to_file:
        with open("logfile.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{message}\n")


def log_markdown(markdown_text):
    """Render Markdown content in the console."""
    console.print(Markdown(markdown_text))
