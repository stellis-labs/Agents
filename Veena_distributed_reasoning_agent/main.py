import re
import requests
import json
import os
import glob
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from sub_agent import SubAgent, query_ollama

console = Console()

# ---------------------------
# Helper Functions for Run Instance Management (Scenario 1)
# ---------------------------
def get_run_instance():
    """
    Reads the current run instance from "run_instance.txt". If the file does not exist, returns 1.
    """
    if os.path.exists("run_instance.txt"):
        with open("run_instance.txt", "r") as f:
            try:
                return int(f.read().strip())
            except:
                return 1
    else:
        return 1

def update_run_instance(new_value: int):
    """
    Writes the new run instance value to "run_instance.txt".
    """
    with open("run_instance.txt", "w") as f:
        f.write(str(new_value))

# ---------------------------
# Helper Functions for Scenario 2 (Config Management)
# ---------------------------
def list_config_files():
    """
    Returns a list of available configuration files matching 'config_agents_*.json'.
    """
    return glob.glob("config_agents_*.json")

def load_config(filename):
    """
    Loads and returns the JSON configuration from the given file.
    """
    with open(filename, "r") as f:
        return json.load(f)

# ---------------------------
# Scenario 1: Generate New Configuration
# ---------------------------
class MainAgent:
    def __init__(self, problem: str, num_agents: int):
        """
        Initializes the MainAgent with the problem statement and desired number of sub-agents.
        """
        self.problem = problem
        self.num_agents = num_agents
        self.tasks = []       # Will hold decomposed tasks (list of dictionaries)
        self.sub_agents = []  # Will hold the created SubAgent instances
        self.results = []     # Will store output from each sub-agent

    def decompose_problem(self):
        """
        Uses the LLM to decompose the problem into exactly num_agents tasks.
        Each task is a JSON object with keys: 'agent_name', 'task_summary', and 'task_prompt'.
        """
        prompt = f"""Decompose the following complex problem into exactly {self.num_agents} tasks.
Each task must be a JSON object with the following keys:
  - "agent_name": A descriptive name for the sub-agent (e.g., "LogisticsNetworkAnalyzer").
  - "task_summary": A brief summary of the task.
  - "task_prompt": Detailed instructions for executing the task.

Problem:
{self.problem}

Respond with a JSON array containing exactly {self.num_agents} objects.
"""
        response = query_ollama(prompt)
        try:
            # Extract the JSON array from the response.
            json_str = re.search(r'\[.*\]', response, re.DOTALL).group()
            # Remove unwanted control characters.
            json_str = re.sub(r'[\x00-\x1f]+', ' ', json_str)
            tasks = json.loads(json_str)
            self.tasks = tasks[:self.num_agents]
            console.print("[green]Decomposition successful:[/green]")
            console.print_json(json.dumps(self.tasks, indent=2))
        except Exception as e:
            console.print(f"[red]Error during problem decomposition: {e}[/red]")

    def create_sub_agents(self):
        """
        Creates sub-agent objects from the decomposed tasks.
        (In Scenario 1, we always generate new agents.)
        """
        for task in self.tasks:
            agent = SubAgent(
                name=task.get("agent_name"),
                task_type=task.get("task_summary"),
                task_prompt=task.get("task_prompt")
            )
            self.sub_agents.append(agent)
        # Display the sub-agents in a formatted table.
        table = Table(title="Created Sub-Agents", show_header=True, header_style="bold magenta")
        table.add_column("Agent Name", style="cyan")
        table.add_column("Task Summary", style="green", max_width=30)
        table.add_column("Task Prompt", style="yellow", max_width=50)
        for agent in self.sub_agents:
            table.add_row(agent.name, agent.task_type, agent.task_prompt)
        console.print(table)

    def execute_sub_agents(self):
        """
        Executes the task for each sub-agent and collects their output.
        """
        for agent in self.sub_agents:
            console.print(f"[blue]Executing {agent.name}...[/blue]")
            result = agent.execute(self.problem)
            self.results.append({"agent_name": agent.name, "result": result})
            panel = Panel(
                f"[bold]{agent.name} Output:[/bold]\n{result}",
                title=agent.name,
                border_style="dim"
            )
            console.print(panel)

    def synthesize_results(self):
        """
        Synthesizes all sub-agent outputs into a final integrated plan.
        """
        synthesis_prompt = f"""Using the following findings from expert agents, synthesize a cohesive plan to solve the problem.
Problem:
{self.problem}

Agent Findings:
{json.dumps(self.results, indent=2)}

Your synthesis should include:
1. A Problem Overview
2. Key Findings from each agent
3. Proposed Solutions
4. Recommended Action Items

Provide your answer in clear, concise bullet points.
"""
        synthesis = query_ollama(synthesis_prompt)
        console.print(Markdown(f"# Final Integrated Plan\n{synthesis}"))

    def save_config(self, run_instance: int):
        """
        Saves the sub-agent configuration for this run into a JSON file.
        The file is named "config_agents_<run_instance>.json".
        """
        config = [agent.to_dict() for agent in self.sub_agents]
        filename = f"config_agents_{run_instance}.json"
        with open(filename, "w") as f:
            json.dump(config, f, indent=2)
        console.print(f"[green]Saved configuration to {filename}[/green]")

    def run(self):
        """
        Executes the complete workflow for Scenario 1:
          1. Decomposes the problem,
          2. Creates sub-agents,
          3. Executes each sub-agent,
          4. Synthesizes the results,
          5. Saves the configuration,
          6. Updates the run instance counter.
        """
        console.rule(f"[bold]Problem:[/bold] {self.problem}")
        self.decompose_problem()
        self.create_sub_agents()
        self.execute_sub_agents()
        self.synthesize_results()
        run_instance = get_run_instance()
        self.save_config(run_instance)
        update_run_instance(run_instance + 1)

# ---------------------------
# Scenario 2: Use Existing Configuration
# ---------------------------
class MainAgentScenario2:
    def __init__(self, problem: str, config):
        """
        Initializes the MainAgent for Scenario 2 with a new problem statement and a loaded configuration.
        'config' is expected to be a list of sub-agent definitions.
        """
        self.problem = problem
        self.config = config
        self.sub_agents = []  # Will store SubAgent objects.
        self.results = []     # Will collect outputs from each sub-agent.

    def create_sub_agents_from_config(self):
        """
        Creates sub-agent objects from the loaded configuration.
        """
        for agent_def in self.config:
            agent = SubAgent(
                name=agent_def.get("name"),
                task_type=agent_def.get("task_type"),
                task_prompt=agent_def.get("task_prompt")
            )
            self.sub_agents.append(agent)
        # Display the loaded sub-agents in a formatted table.
        table = Table(title="Loaded Sub-Agents", show_header=True, header_style="bold magenta")
        table.add_column("Agent Name", style="cyan")
        table.add_column("Task Summary", style="green", max_width=30)
        table.add_column("Task Prompt", style="yellow", max_width=50)
        for agent in self.sub_agents:
            table.add_row(agent.name, agent.task_type, agent.task_prompt)
        console.print(table)

    def execute_sub_agents(self):
        """
        Executes each sub-agent's task and collects their outputs.
        """
        for agent in self.sub_agents:
            console.print(f"[blue]Executing {agent.name}...[/blue]")
            result = agent.execute(self.problem)
            self.results.append({"agent_name": agent.name, "result": result})
            panel = Panel(
                f"[bold]{agent.name} Output:[/bold]\n{result}",
                title=agent.name,
                border_style="dim"
            )
            console.print(panel)

    def synthesize_results(self):
        """
        Synthesizes the outputs from all sub-agents into a final integrated plan.
        """
        synthesis_prompt = f"""Using the following findings from expert agents, synthesize a cohesive plan to solve the problem.
Problem:
{self.problem}

Agent Findings:
{json.dumps(self.results, indent=2)}

Your synthesis should include:
1. A Problem Overview
2. Key Findings from each agent
3. Proposed Solutions
4. Recommended Action Items

Provide your answer in clear, concise bullet points.
"""
        synthesis = query_ollama(synthesis_prompt)
        console.print(Markdown(f"# Final Integrated Plan\n{synthesis}"))

    def run(self):
        """
        Executes the workflow for Scenario 2:
          1. Creates sub-agents from the loaded configuration,
          2. Executes each sub-agent,
          3. Synthesizes the outputs into a final plan.
        """
        console.rule(f"[bold]Problem:[/bold] {self.problem}")
        self.create_sub_agents_from_config()
        self.execute_sub_agents()
        self.synthesize_results()

# ---------------------------
# Main Program: Choose Scenario
# ---------------------------
if __name__ == "__main__":
    console.rule("[bold green]DISTRIBUTED REASONING AGENT[/bold green]")
    # First, ask for the complex problem statement.
    problem = input("Enter complex problem statement:\n> ").strip()
    
    # Then ask if user wants to generate a new config or use an existing one.
    mode = input("Choose an option:\n1. Generate new configuration\n2. Use existing configuration\nEnter 1 or 2: ").strip()
    
    if mode == "1":
        # Scenario 1: Generate new configuration.
        num_input = input("How many sub-agents do you want? (Max 5): ").strip()
        try:
            num_agents = int(num_input)
            num_agents = max(1, min(num_agents, 5))
        except:
            num_agents = 3
        main_agent = MainAgent(problem, num_agents)
        main_agent.run()
    elif mode == "2":
        # Scenario 2: Use existing configuration.
        config_files = glob.glob("config_agents_*.json")
        if not config_files:
            console.print("[red]No configuration files found. Please run Scenario 1 first to generate a configuration file.[/red]")
            exit(1)
        console.print("[blue]Available configuration files:[/blue]")
        for idx, file in enumerate(config_files, 1):
            console.print(f"{idx}. {file}")
        selection = input("Select a configuration file by number: ").strip()
        try:
            sel_index = int(selection) - 1
            chosen_config_file = config_files[sel_index]
        except Exception as e:
            console.print(f"[red]Invalid selection: {e}[/red]")
            exit(1)
        config = load_config(chosen_config_file)
        main_agent = MainAgentScenario2(problem, config)
        main_agent.run()
    else:
        console.print("[red]Invalid option. Please run the program again and choose either 1 or 2.[/red]")
