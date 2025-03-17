import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
import google.generativeai as genai

# Load environment variables
load_dotenv()
console = Console()

# Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

class DistributedReasoningAgent:
    def __init__(self, model="mixtral-8x7b-32768"):
        self.llm = ChatGroq(model_name=model, groq_api_key=GROQ_API_KEY)
        self.sub_agents = []
        self.output_data = {}

    def generate_sub_tasks(self, user_input):
        """Dynamically generate sub-tasks based on the problem statement."""
        console.print(Panel("Step 1: Problem Decomposition", title="[bold cyan]Process[/bold cyan]", border_style="cyan"))
        
        response = self.llm.invoke([
            SystemMessage(content="You are an expert task decomposer."),
            HumanMessage(content=f"Break down this problem into clear sub-tasks based on complexity. Only provide the sub-task titles, without any descriptions: {user_input}")
        ])
        
        sub_tasks = response.content.strip().split("\n")
        sub_tasks = [task.strip() for task in sub_tasks if task.strip()]

        table = Table(title="Generated Sub-Tasks", show_header=True, header_style="bold magenta")
        table.add_column("Task Number", justify="center", style="bold yellow")
        table.add_column("Task Description", style="bold green")

        for i, task in enumerate(sub_tasks, 1):
            table.add_row(str(i), task)
        
        console.print(table)
        self.output_data["sub_tasks"] = sub_tasks
        return sub_tasks

    def create_sub_agents(self, sub_tasks):
        """Create sub-agents dynamically based on the generated sub-tasks."""
        console.print(Panel("Step 2: Sub-Agent Creation and Task Assignment", title="[bold cyan]Process[/bold cyan]", border_style="cyan"))
        
        for task in sub_tasks:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert in naming agents based on their tasks."),
                HumanMessage(content=f"Generate a meaningful and concise name for an agent responsible for this task. Only provide the name, without any description: {task}")
            ])
            agent_name = response.content.strip()
            
            sub_agent = SubAgent(agent_name, task, self.llm)
            self.sub_agents.append(sub_agent)
            console.print(f"[bold green]✔ Created Sub-Agent:[/bold green] {agent_name}")

    def execute(self):
        """Execute the problem-solving process."""
        console.print(Panel("Step 3: Task Execution", title="[bold cyan]Process[/bold cyan]", border_style="cyan"))
        results = {}
        
        for agent in self.sub_agents:
            agent.execute_task()
            results[agent.name] = agent.result
        
        console.print(Panel("Step 4: Result Synthesis and Summarization", title="[bold cyan]Process[/bold cyan]", border_style="cyan"))
        summarized_solution = self.summarize_results(results)
        
        console.print(Panel(summarized_solution, title="[bold cyan]🌟 Final Solution 🌟[/bold cyan]", border_style="green"))
        
        self.output_data["sub_agent_results"] = results
        self.output_data["summarized_solution"] = summarized_solution
        self.save_output()

    def summarize_results(self, results):
        """Summarize the findings using Google's Gemini model."""
        findings_summary = "\n".join([f"[bold yellow]{agent_name}:[/bold yellow] {result}" for agent_name, result in results.items()])
        
        prompt = f"""
        Given the following findings from different agents, provide a structured, concise, and actionable summary. 
        Ensure the summary:
        - Captures key insights from each finding.
        - Eliminates redundancy.
        - Presents a logical, cohesive solution.
        - Includes actionable recommendations if applicable.

        Findings:
        {findings_summary}

        Provide the summary in a structured format with key points highlighted.
        """

        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-pro")
    
        # Generate the response
        response = model.generate_content(prompt)
        return response.text

    def save_output(self):
        """Save the output data to a JSON file."""
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(self.output_data, f, indent=4, ensure_ascii=False)
        console.print("[bold cyan]✔ Output saved to output.json[/bold cyan]")

class SubAgent:
    def __init__(self, name, task, llm):
        self.name = name
        self.task = task
        self.llm = llm
        self.result = None

    def execute_task(self):
        """Execute the task assigned to this sub-agent."""
        console.print(f"[yellow]🔄 Executing {self.name}...[/yellow]")
        response = self.llm.invoke([
            SystemMessage(content=f"Role: {self.name}"),
            HumanMessage(content=f"Perform this task: {self.task}")
        ])
        self.result = response.content
        console.print(Panel(f"{self.result}", title=f"[bold green]✔ Findings from {self.name}[/bold green]", border_style="green"))


# Example Usage
if __name__ == "__main__":
    agent = DistributedReasoningAgent()
    user_problem = "Develop a strategy to optimize cloud computing costs for a growing SaaS company."
    
    sub_tasks = agent.generate_sub_tasks(user_problem)
    agent.create_sub_agents(sub_tasks)
    agent.execute()
