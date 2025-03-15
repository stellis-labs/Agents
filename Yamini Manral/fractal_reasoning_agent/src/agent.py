#agent.py
# import time
from rich.console import Console
# from rich.live import Live
# from rich.spinner import Spinner
from src.logger import log
from src.config import MAX_SCENARIOS
from src.utils import stream_response
from src.llm_api import call_llm
from rich.markdown import Markdown

console = Console()

class FractalReasoningAgent:
    def __init__(self, question):
        self.question = question
        self.sub_problems = []  # Stores decomposed sub-problems
        self.solutions = []     # Stores solutions for each sub-problem
        self.evaluations = []   # Stores evaluations of solutions
        self.optimizations = [] # Stores optimized solutions
        self.final_solution = None  # Stores the integrated final solution

    def decomposer(self, problem):
        """Decomposer: Break down the problem into smaller sub-problems."""
        prompt = f"""
        You are a reasoning agent. Follow the instructions very carefully and strictly.The problem is:
        {problem}
        Break down the problem into {MAX_SCENARIOS} sub-problems. Provide a concise list of sub-problems, without bullets or numbers.
        Do not include any introductory text or explanations. directly start with the sub-problems. Do not include any other text or explanations. Just start writing sub-problems.
        Ensure the response is precise and well-formatted, with proper spacing and new lines.
        Each sub-problem should be a single, clear, and actionable statement.
        
        """
        try:
            response = call_llm(prompt)
            full_response = ""
            for chunk in stream_response(response):
                full_response += chunk

            full_response = full_response.strip()
            sub_problems = [s.strip() for s in full_response.split("\n") if s.strip()]
            
            if not sub_problems:
                console.print("[bold red]⚠ No sub-problems generated![/bold red]")
                return []

            for i, sub_problem in enumerate(sub_problems[:MAX_SCENARIOS], start=1):
                console.print(f"- Sub-problem {i}: {sub_problem}")
            return sub_problems
        except Exception as e:
            log(f"Error decomposing problem: {e}", style="bold red")
            return []

    def solver(self, sub_problems):
        """Solver: Solve each sub-problem with a single, concise solution."""
        solutions = []
        for sub_problem in sub_problems:
            prompt = f"""
            You are a reasoning agent. The sub-problem is:
            {sub_problem}
            Provide a single, concise solution to this sub-problem.
            Ensure the response is precise and well-formatted, with proper spacing and new lines.
            Do NOT provide multiple solutions or introduce new sub-problems.
            Do not include any introductory text or explanations.
            """
            try:
                response = call_llm(prompt)
                solution = stream_response(response).strip()
                
                # Validate the solution
                if "\n" in solution:  # If the solution contains multiple lines, take only the first one
                    solution = solution.split("\n")[0].strip()
                    console.print(f"[bold yellow]⚠ Warning: Multiple solutions detected for sub-problem. Using the first solution.[/bold yellow]")
                
                console.print(f"- Solver: {solution}")
                solutions.append(solution)
            except Exception as e:
                log(f"Error solving sub-problem: {e}", style="bold red")
                solutions.append("No solution available.")
        return solutions

    def evaluator(self, sub_problems, solutions):
        """Evaluator: Evaluate the solutions to sub-problems."""
        evaluations = []
        for i, (sub_problem, solution) in enumerate(zip(sub_problems, solutions)):
            prompt = f"""
            You are a reasoning agent. The sub-problem is:
            {sub_problem}
            The proposed solution is:
            {solution}

            Evaluate the solution critically. Identify strengths, weaknesses, and potential improvements.
            Ensure the response is precise and well-formatted, with proper spacing and new lines.
            Each sub-problem should be a single, clear, and actionable statement.
            Do not include any introductory text or explanations.
            """
            try:
                response = call_llm(prompt)
                evaluation = stream_response(response).strip()
                console.print(f"- Evaluator: {evaluation}")
                evaluations.append(evaluation)
            except Exception as e:
                log(f"Error evaluating solution: {e}", style="bold red")
                evaluations.append("No evaluation available.")
        return evaluations

    def optimizer(self, sub_problems, solutions, evaluations):
        """Optimizer: Optimize the solutions to sub-problems."""
        optimizations = []
        for i, (sub_problem, solution, evaluation) in enumerate(zip(sub_problems, solutions, evaluations)):
            prompt = f"""
            You are a reasoning agent. The sub-problem is:
            {sub_problem}
            The proposed solution is:
            {solution}
            The evaluation of the solution is:
            {evaluation}

            Suggest optimizations to improve the solution.
            Ensure the response is precise and well-formatted, with proper spacing and new lines.
            Each sub-problem should be a single, clear, and actionable statement.
            Do not include any introductory text or explanations.
            """
            try:
                response = call_llm(prompt)
                optimization = stream_response(response).strip()
                console.print(f"- Optimizer: {optimization}")
                optimizations.append(optimization)
            except Exception as e:
                log(f"Error optimizing solution: {e}", style="bold red")
                optimizations.append("No optimization available.")
        return optimizations

    def integrator(self, sub_problems, solutions, evaluations, optimizations):
        """Integrator: Combine all solutions into a cohesive final solution."""
        final_solution = ""
        
        for i, (sub_problem, solution, evaluation, optimization) in enumerate(zip(sub_problems, solutions, evaluations, optimizations)):
            prompt = f"""
            You are a reasoning agent. Below is a sub-problem, its solution, evaluation, and optimization:
            
            Sub-problem {i + 1}: {sub_problem}
            Solution: {solution}
            Evaluation: {evaluation}
            Optimization: {optimization}

            Provide a concise summary of this sub-problem, its solution, evaluation, and optimization.
            Ensure the response is precise and well-formatted, with proper spacing and new lines.
            Do not include any introductory text or explanations.
            """
            try:
                response = call_llm(prompt)
                summary = stream_response(response).strip()
                final_solution += f"\n### Sub-problem {i + 1} Summary:\n{summary}\n"
            except Exception as e:
                log(f"Error summarizing sub-problem {i + 1}: {e}", style="bold red")
                final_solution += f"\n### Sub-problem {i + 1} Summary:\nNo summary available.\n"
        
        return final_solution

    def communicator(self, final_solution):
        """Communicator: Display the final solution to the user."""
        console.print("\n[bold cyan]Final Recommendation:[/bold cyan]")
        console.print(Markdown(final_solution))