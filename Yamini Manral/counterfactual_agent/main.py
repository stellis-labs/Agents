# main.py
from rich.console import Console
from src.conversation import ChatSession

console = Console()


def main():
    chat = ChatSession()
    chat.start()

if __name__ == "__main__":
    main()
