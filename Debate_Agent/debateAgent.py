import json
import os
import time
import requests
from dotenv import load_dotenv
from rich.console import Console


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

console = Console()

DEBATE_STEPS = {
    "generate_perspectives": "Generate perspectives on this issue based on type of perspective.",
    "evaluate_evidence": "Assess the reliability of the supporting evidence on a scale of 0 to 10.",
    "check_logical_consistency": "Analyze logical consistency on a scale of 0 to 10.",
    "check_ethical_consistency": "Analyze ethical consistency on a scale of 0 to 10."
}

JUDGE_STEPS = {
    "understand_all_perspectives": "Understand key arguments of each perspective on this issue based on type of perspective.",
    "evaluate_ratings": "Assess the reliability of the supporting evidence, logical consistency, and ethical consistency of each perspective, which are rated on a scale of 0 to 10.",
    "compare_arguments": "Compare arguments based on all the above ratings and arguments.",
    "synthesize_conclusion": "Provide a balanced and well-reasoned conclusion with a clear winner."
}

class DebateAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self.load_data()
        self.perspectives = []
        self.evidence_scores = {}
        self.consistency_scores = {}
        self.ethical_scores = {}

    def load_data(self):
        try:
            with open(self.data_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self):
        with open(self.data_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_debate_prompt(self, topic, perspective_type):
        return f"""
        You are an expert debate assistant trained to analyze complex issues from multiple perspectives.
        Your role is to provide well-reasoned arguments, identify logical inconsistencies, and highlight the strongest and weakest points in each stance.
        
        Debate Topic: {topic}
        Perspective Type: {perspective_type}
        
        Steps:
        - {DEBATE_STEPS['generate_perspectives']}
        - {DEBATE_STEPS['evaluate_evidence']}
        - {DEBATE_STEPS['check_logical_consistency']}
        - {DEBATE_STEPS['check_ethical_consistency']}
        
        Be thorough, and generate a detailed response including all steps in the process.
        """

    def get_judge_prompt(self, topic, responses):
        return f"""
        You are an expert debate judge tasked with evaluating a set of perspectives on a specific issue. 
        The perspectives have already been rated on a scale from 0 to 10 based on their supporting evidence, logical consistency, and ethical consistency.
        Your task is to assess these ratings and provide a final, well-reasoned conclusion.

        **Debate Topic:** {topic}

        **Generated Perspectives:**
        {responses}

        Steps:
        - {JUDGE_STEPS['understand_all_perspectives']}
        - {JUDGE_STEPS['evaluate_ratings']}
        - {JUDGE_STEPS['compare_arguments']}
        - {JUDGE_STEPS['synthesize_conclusion']}

        Please provide a detailed and balanced evaluation, followed by a clear final answer highlighting one of the perspectives as the winner to the debate topic in one sentence. 
        Explicitly refer to each perspective by name ("Supportive Perspective," "Contrarian Perspective," and "Legal and Ethical Perspective") instead of labeling them as "Perspective 1," "Perspective 2," and "Perspective 3."
        """

    def call_llm(self, prompt, max_tokens=1000):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }

        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(url, json=data, headers=headers)
                
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 10))
                    console.print(f"[bold red]Rate limit reached. Retrying after {retry_after} seconds...[/bold red]")
                    time.sleep(retry_after)
                    continue  

                response.raise_for_status()
                response_json = response.json()
                
                choices = response_json.get("choices", [])
                if choices and "message" in choices[0]:
                    return choices[0]["message"].get("content", "No content found.")
                return "No valid response received."

            except requests.exceptions.RequestException as e:
                console.print(f"[bold red]API Request Failed: {str(e)}[/bold red]")
                time.sleep(5)  # Wait before retrying

    def get_perspectives(self, topic):
        console.print("\n[bold cyan]Generating Perspectives:[/bold cyan]")

        prompts = [
            self.get_debate_prompt(topic, "Supportive Perspective"),
            self.get_debate_prompt(topic, "Contrarian Perspective"),
            # self.get_debate_prompt(topic, "Legal and Ethical Perspective")
        ]

        responses = []
        for prompt in prompts:
            response = self.call_llm(prompt)
            if response:
                responses.append(response.strip())

        self.perspectives = list(set(responses))
        for idx, p in enumerate(self.perspectives, start=1):
            console.print(f"{idx}. {p}")

    def evaluate_judge(self, topic):
        console.print("\n[bold cyan]Evaluating Debate Outcome:[/bold cyan]")

        if not self.perspectives:
            console.print("[red]No perspectives available for evaluation.[/red]")
            return

        formatted_responses = "\n\n".join(
            [f"Perspective {idx}:\n{p}" for idx, p in enumerate(self.perspectives, start=1)]
        )

        prompt = self.get_judge_prompt(topic, formatted_responses)
        response = self.call_llm(prompt)
        if response:
            console.print(f"\n[bold green]Judge's Evaluation:[/bold green]\n{response}")
            self.save_perspectives_and_evaluation(response)

    def save_perspectives_and_evaluation(self, evaluation):
        # Save perspectives and judge evaluation to the JSON file
        debate_data = {
            "perspectives": self.perspectives,
            "evaluation": evaluation
        }
        self.data.append(debate_data)
        self.save_data()

    def run_debate(self, topic):
        self.get_perspectives(topic)
        if self.perspectives:
            self.evaluate_judge(topic)

if __name__ == "__main__":
    agent = DebateAgent("procon_debates.json")

    while True:
        topic = input("\nEnter a debate question (or type 'exit' to quit): ").strip()
        if topic.lower() == "exit":
            console.print("\n[bold cyan]Exiting Debate Agent. Have a great day![/bold cyan]")
            break
        if not topic:
            console.print("[red]Please enter a valid question.[/red]")
            continue
        agent.run_debate(topic)
