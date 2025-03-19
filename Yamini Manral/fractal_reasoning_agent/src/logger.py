# logger.py
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

console = Console()

def log(message, style="bold blue"):
    """Log messages with Rich formatting."""
    console.print(Panel(Text(message, style=style)))
    
    with open("logfile.txt", "a") as log_file:
        log_file.write(f"{message}\n")

def log_markdown(markdown_text):
    """Render Markdown content in the console."""
    console.print(Markdown(markdown_text))
