# main.py
from rich.console import Console
from src.conversation import ChatSession

console = Console()

def main():
    """Entry point for the Fractal Reasoning Agent application."""
    # console.print("\n[bold green]Welcome to the Fractal Reasoning Agent![/bold green]")
    # console.print("This tool helps you explore complex problems by breaking them down into smaller, manageable parts.\n")

    # Initialize the chat session
    chat_session = ChatSession()
    
    # Start the chat session
    chat_session.start()

if __name__ == "__main__":
    main()