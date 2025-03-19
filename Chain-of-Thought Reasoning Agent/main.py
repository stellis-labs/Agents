from rich.console import Console
from reasoning_agent import ReasoningAgent
from llm_interfaces.llm_factory import get_llm

def main():
    console = Console()

    # Ask user for LLM selection
    console.print("[bold blue]Choose LLM provider: [/bold blue] 1) Ollama (Local)  2) Groq (Cloud)")
    choice = input("> ").strip()

    if choice == "1":
        llm_provider = "ollama"
        llm = get_llm("ollama", model_name="llama3.2")
    elif choice == "2":
        llm_provider = "groq"
        api_key = input("Enter your Groq API Key: ").strip()
        llm = get_llm("groq", model_name="llama3.2", api_key=api_key)
    else:
        console.print("[bold red]Invalid choice. Defaulting to Ollama.[/bold red]")
        llm_provider = "ollama"
        llm = get_llm("ollama", model_name="llama3.2")

    # Initialize the reasoning agent
    agent = ReasoningAgent(llm)

    # Take user input
    console.print("\n[bold blue]Enter the problem statement:[/bold blue]")
    problem_statement = input("> ").strip()

    while not problem_statement:
        console.print("[bold red]Error: Problem statement cannot be empty. Please try again.[/bold red]")
        problem_statement = input("> ").strip()

    # Solve problem
    agent.solve_problem(problem_statement)

if __name__ == "__main__":
    main()