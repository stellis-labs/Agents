from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.panel import Panel
from rich.console import Console

console = Console()

class ParallelReasoningPipeline:
    """Manages parallel execution of reasoning tasks with dynamic step numbering."""
    def __init__(self):
        self.steps = []

    def add_step(self, description, data_source, processor, data_type, color):
        """Adds an analysis step to the pipeline without predefined numbering."""
        self.steps.append({
            "description": description,
            "data_source": data_source,
            "processor": processor,
            "data_type": data_type,
            "color": color
        })

    def run(self):
        """Executes all pipeline steps in parallel and numbers them dynamically."""
        results = []
        step_number = 1  # Start numbering dynamically

        with ThreadPoolExecutor() as executor:
            future_to_step = {executor.submit(self.process_step, step): step for step in self.steps}

            for future in as_completed(future_to_step):
                step = future_to_step[future]
                insights = future.result()
                
                # Dynamically number the step
                step_content = (
                    f"[bold]Data Source:[/bold] {step['data_type']}\n"
                    f"[bold]Insights:[/bold] {insights}"
                )
                console.print(Panel(step_content, title=f"[bold]Step {step_number}: {step['description']}[/bold]", border_style=step["color"]))
                
                results.append(insights)
                step_number += 1  # Increment step number for next completed step

        return results

    def process_step(self, step):
        """Fetches data, processes it, and returns insights."""
        data = step["data_source"].fetch_data()
        return step["processor"].process(data)