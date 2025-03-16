# conversation.py
import time
import sys
from rich.console import Console
from src.agent import FractalReasoningAgent
from src.logger import log_markdown

console = Console()

class ChatSession:
    def __init__(self):
        self.active_question = None  # Stores the user's complex question
        self.fractal_agent = None    # Instance of the FractalReasoningAgent
        self.sub_problems = []       # Stores decomposed sub-problems
        self.solutions = []          # Stores solutions for each sub-problem
        self.evaluations = []        # Stores evaluations of solutions
        self.optimizations = []      # Stores optimized solutions

    def start(self):
        """Start the chat session and handle user input."""
        console.print("\n[bold green]Welcome to the Fractal Reasoning Agent![/bold green]")
        console.print("You can ask a complex question, and the system will break it down into smaller components for analysis.\n")
        console.print("You can also ask to exit the session by typing 'bye'.\n")

        # Step 1: Get the user's complex question
        self.active_question = self.get_user_question()
        if not self.active_question:
            self.exit_session()

        # Step 2: Initialize the FractalReasoningAgent with the user's question
        start_time = time.time()
        self.fractal_agent = FractalReasoningAgent(self.active_question)

        # Step 3: Decompose the question into sub-problems
        console.print("\n[bold cyan]Step 1: Decomposing the Problem...[/bold cyan]\n")
        self.sub_problems = self.fractal_agent.decomposer(self.active_question)
        
        if not self.sub_problems:
            console.print("[bold red]⚠ Failed to decompose the problem. Exiting...[/bold red]")
            self.exit_session()

        # Step 4: Solve sub-problems
        console.print("\n[bold cyan]Step 2: Solving Sub-problems...[/bold cyan]\n")
        self.solutions = self.fractal_agent.solver(self.sub_problems)

        # Step 5: Evaluate solutions
        console.print("\n[bold cyan]Step 3: Evaluating Solutions...[/bold cyan]\n")
        self.evaluations = self.fractal_agent.evaluator(self.sub_problems, self.solutions)

        # Step 6: Optimize solutions
        console.print("\n[bold cyan]Step 4: Optimizing Solutions...[/bold cyan]\n")
        self.optimizations = self.fractal_agent.optimizer(self.sub_problems, self.solutions, self.evaluations)

        # Step 7: Integrate solutions
        console.print("\n[bold cyan]Step 5: Integrating Solutions...[/bold cyan]\n")
        final_solution = self.fractal_agent.integrator(self.sub_problems, self.solutions, self.evaluations, self.optimizations)

        # Step 8: Communicate results
        console.print("\n[bold cyan]Step 6: Communicating Results...[/bold cyan]\n")
        self.fractal_agent.communicator(final_solution)

        # Step 9: Display the time taken for the process
        elapsed_time = time.time() - start_time
        console.print("\n")
        log_markdown(f"Time taken: {elapsed_time:.2f} seconds")
        console.print("\n")

        # Step 10: Exit the session
        self.exit_session()

    def get_user_question(self):
        """Prompt the user for a complex question and validate input."""
        while True:
            user_input = input("🔍 Enter a complex question: ").strip()
            if user_input.lower() == "bye":
                self.exit_session()
            elif not user_input:
                console.print("[bold red]⚠ Please enter a valid question.[/bold red]")
            else:
                return user_input

    def exit_session(self):
        """Exit the session and clean up."""
        console.print("\n🔴 [bold red]Exiting the session...[/bold red]\n")
        self.active_question = None
        self.sub_problems = []
        sys.exit()  # Exit the program immediately