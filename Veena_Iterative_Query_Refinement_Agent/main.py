import json
import requests
from datetime import datetime
from collections import defaultdict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from urllib.parse import quote

console = Console()

class IterativeQueryAgent:
    def __init__(self):
        self.memory_file = 'query_memory.json'
        self.memory = self._load_memory()
        self.query_history = defaultdict(list)

    def _load_memory(self):
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def _query_ollama(self, prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {"model": "llama3", "prompt": prompt, "stream": True}
        
        try:
            response = requests.post(url, json=payload, headers=headers, stream=True)
            response.raise_for_status()
            result = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    data = json.loads(decoded_line)
                    result += data.get("response", "")
                    if data.get("done"):
                        break
            return result.strip()
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return ""

    def generate_variations(self, initial_query: str) -> list:
        prompt = f"""Generate exactly 3 distinct search queries about: {initial_query}
        Return ONLY a JSON array of questions formatted exactly like:
        ["First question?", "Second question?", "Third question?"]
        Include nothing else in your response."""
        
        response = self._query_ollama(prompt)
        try:
            variations = json.loads(response)
            if isinstance(variations, list) and len(variations) >= 3:
                return [q.strip() for q in variations[:3] if isinstance(q, str)]
            return []
        except json.JSONDecodeError:
            console.print("[yellow]Failed to parse JSON response[/yellow]")
            return []

    def retrieve_wikipedia_knowledge(self, query: str) -> str:
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={quote(query)}&limit=1&format=json"
            search_response = requests.get(search_url).json()
            
            if not search_response[1]:
                return ""
            
            page_title = search_response[1][0]
            summary_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles={quote(page_title)}&format=json"
            summary_response = requests.get(summary_url).json()
            page = next(iter(summary_response['query']['pages'].values()))
            return page.get('extract', '')[:3000]
        except Exception as e:
            console.print(f"[yellow]Wikipedia error: {e}[/yellow]")
            return ""

    def refine_query(self, initial_query: str) -> str:
        console.print(Panel(f"[bold cyan]Initial Query:[/bold cyan] {initial_query}"))

        # Step 1: Generate validated variations
        variations = []
        attempts = 0
        while len(variations) < 3 and attempts < 3:
            new_vars = self.generate_variations(initial_query)
            variations = [v for v in new_vars if v.endswith('?') and 10 < len(v) < 100]
            attempts += 1
        
        if len(variations) < 3:
            variations = [
                f"What is the primary mechanism behind {initial_query}?",
                f"How does environment affect {initial_query}?",
                f"What recent discoveries relate to {initial_query}?"
            ]

        # Display variations
        table = Table(title="Step 1: Generated Query Variations", show_lines=True)
        table.add_column("#", style="cyan")
        table.add_column("Query")
        for idx, var in enumerate(variations, 1):
            table.add_row(str(idx), var)
        console.print(table)

        # Step 2: Process variations
        console.print(Panel("[bold green]Step 2: Processing Variations[/bold green]"))
        insights = []
        for idx, query in enumerate(variations, 1):
            context = self.retrieve_wikipedia_knowledge(query)
            prompt = f"Answer concisely: {query}\nContext: {context}"
            response = self._query_ollama(prompt)
            
            console.print(f"\n[bold]Variation {idx}:[/bold] [italic]{query}[/italic]")
            console.print(f"[bright_blue]Response:[/bright_blue] {response}")
            
            insights.append({"query": query, "response": response})
            self.memory.append({
                "initial_query": initial_query,
                "query": query,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })

        # Step 3: Extract insights
        console.print(Panel("[bold yellow]Step 3: Key Insights[/bold yellow]"))
        extracted = []
        for idx, insight in enumerate(insights, 1):
            prompt = f"""Extract the core factual insight from:
            {insight['response']}
            
            Return ONLY the key finding as one short sentence."""
            result = self._query_ollama(prompt)
            if result and result[-1] not in {'.', '?', '!'}:
                result += '.'
            extracted.append(result)
            console.print(f"[bold]{idx}.[/bold] {result}")

        # Step 4: Final synthesis
        console.print(Panel("[bold magenta]Step 4: Final Answer[/bold magenta]"))
        synthesis_prompt = f"""Combine these insights about {initial_query}:
        {chr(10).join(extracted)}
        
        Structure as:
        - Overview paragraph
        - 3 key bullet points
        - Conclusion summary"""
        
        final = self._query_ollama(synthesis_prompt)
        console.print(Panel(final, title="Final Answer", style="green"))
        
        self._save_memory()
        return final

if __name__ == "__main__":
    agent = IterativeQueryAgent()
    query = input("Enter your query: ")
    agent.refine_query(query)