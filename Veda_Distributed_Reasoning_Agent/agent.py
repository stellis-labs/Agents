import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from rich.console import Console

load_dotenv()
console = Console()

# Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class DistributedReasoningAgent:
    def __init__(self, model="mixtral-8x7b-32768", max_sub_agents=5):
        self.llm = ChatGroq(model_name=model, groq_api_key=GROQ_API_KEY)
        self.max_sub_agents = max_sub_agents
        self.sub_agents = []

    def generate_sub_tasks(self, user_input):
        """Generate sub-tasks dynamically based on the user input."""
        console.print(f"[bold cyan]Step 1: Problem Decomposition[/bold cyan]")
        response = self.llm.invoke([
            SystemMessage(content="You are an expert task decomposer."),
            HumanMessage(content=f"Break down this problem into {self.max_sub_agents} clear sub-tasks. Only provide the sub-task titles, without any descriptions: {user_input}")
        ])
        
        sub_tasks = response.content.strip().split("\n")
        sub_tasks = [task.strip() for task in sub_tasks if task.strip()]
        
        console.print(f"[bold cyan]Generated Sub-Tasks:[/bold cyan]")
        for i, task in enumerate(sub_tasks[:self.max_sub_agents], 1):
            console.print(f"- {task}")  
        
        return sub_tasks[:self.max_sub_agents]

    def create_sub_agents(self, sub_tasks):
        """Create sub-agents based on the generated sub-tasks."""
        console.print(f"[bold cyan]Step 2: Sub-Agent Creation and Task Assignment[/bold cyan]")
        for task in sub_tasks:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert in naming agents based on their tasks."),
                HumanMessage(content=f"Generate a meaningful and concise name for an agent responsible for this task. "
                                 f"Only provide the name, without any description: {task}")
        ])
            agent_name = response.content.strip()

            sub_agent = SubAgent(agent_name, task, self.llm)
            self.sub_agents.append(sub_agent)
            
            console.print(f"- {agent_name}")

    def execute(self):
        """Execute the problem-solving process."""
        console.print("[bold cyan]Step 3: Task Execution[/bold cyan]")
        for agent in self.sub_agents:
            agent.execute_task()

        console.print("[bold cyan]Step 4: Result Synthesis and Summarization[/bold cyan]")
        results = {agent.name: agent.result for agent in self.sub_agents}
        
        summarized_solution = self.summarize_results(results)
        console.print(f"[bold cyan]Summarized Solution:[/bold cyan]")
        #console.print(json.dumps(summarized_solution, indent=4))
        console.print(summarized_solution)



    def summarize_results(self, results):
        """Summarize the findings into a cohesive, high-level summary."""
        findings_summary = "\n".join([f"{agent_name}: {result}" for agent_name, result in results.items()])

        response = self.llm.invoke([
            SystemMessage(content="You are an expert in synthesizing multiple findings into a clear, high-level summary."),
            HumanMessage(content=f"""
            Given the following findings from different agents, provide a structured, concise, and actionable summary. 
            Ensure the summary:
            - Captures key insights from each finding.
            - Eliminates redundancy.
            - Presents a logical, cohesive solution.
            - Includes actionable recommendations if applicable.

            Findings:
            {findings_summary}

            Provide the summary in a structured format with key points highlighted.
            """)
        ])
        
        return {"🌟 Final Solution 🌟": response.content}
    
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
        console.print(f"[bold green]✔ Findings from {self.name}:[/bold green] {self.result}")
