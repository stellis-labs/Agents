# console interface for the patient triage application - majorly for testing purposes
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from patient_triage.app import generate_structured_triage_report

console = Console()

def display_triage_report(report):
    table = Table(title="Triage Report", show_header=True, header_style="bold magenta")
    table.add_column("Step", style="dim", width=20)
    table.add_column("Details", style="green")

    for step in report["steps"]:
        table.add_row(step["description"], str(step["details"]))

    final_output = report["final_output"]
    table.add_row("Final Output", f"Triage Level: {final_output['triage_level']}\nExplanation: {final_output['explanation']}")

    console.print(table)

def main():
    console.print("[bold magenta]Patient Triage Application[/bold magenta]")
    symptoms = Prompt.ask("Enter symptoms")
    history = Prompt.ask("Enter medical history")
    diagnosis = Prompt.ask("Enter preliminary diagnosis")

    report = generate_structured_triage_report(symptoms, history, diagnosis)
    display_triage_report(report)

if __name__ == "__main__":
    main()
    # done