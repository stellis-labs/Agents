from rich.console import Console
from rich.panel import Panel

class DisplayManager:
    def __init__(self):
        self.console = Console()

    def display_problem(self, problem: str):
        """ Display the problem statement in a clear and styled format. """
        self.console.print(f"\n[bold blue]Problem Statement:[/bold blue] [bold red]{problem}[/bold red]\n")

    def display_step(self, step_title: str, content: list):
        """ Display each reasoning step in a structured panel format. """
        if not content:
            content = ["No response available."]
        panel_content = "\n".join(content)
        self.console.print(Panel(panel_content, title=f"[bold green]{step_title}[/bold green]", style="bold yellow"))