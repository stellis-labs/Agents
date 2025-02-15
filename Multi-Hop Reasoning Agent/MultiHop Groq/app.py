from rich.console import Console
from rich.panel import Panel
from groq import Groq
from config import API_KEY
from query_parser import QueryParser
from parallel_pipeline import ParallelReasoningPipeline
from data_sources import SQLDataSource, DocumentParser, APIDataSource
from processing import CompetitorProcessor, MarketTrendsProcessor, SalesProcessor, FeedbackProcessor, SummarizationProcessor

console = Console()

def main():
    console.print("[bold cyan]\nEnhanced Multi-Hop Reasoning Agent[/bold cyan]\n")

    # Initialize Groq Client
    groq_client = Groq(api_key=API_KEY)

    # Parse the query using LLM
    query = "What are the key factors driving the decline in sales for Product X in the last quarter?"
    query_parser = QueryParser(groq_client)
    tasks = query_parser.parse(query)
    console.print(Panel(f"Parsed Tasks: {tasks}", title="Query Parsing", border_style="cyan"))

    # Initialize the pipeline
    pipeline = ParallelReasoningPipeline()

    # ✅ Remove hardcoded step numbers & let dynamic numbering handle it
    pipeline.add_step(
        "Retrieve and analyze sales data for Product X",
        SQLDataSource("sales.db", "SELECT * FROM sales WHERE product='Product X'"),
        SalesProcessor(groq_client),
        "SQL Database", "blue"
    )
    pipeline.add_step(
        "Retrieve and analyze customer feedback for Product X",
        DocumentParser("feedback.pdf"),
        FeedbackProcessor(groq_client),
        "Document", "green"
    )
    pipeline.add_step(
        "Retrieve and analyze competitor data",
        APIDataSource("mock://competitors"),
        CompetitorProcessor(groq_client),
        "API", "yellow"
    )
    pipeline.add_step(
        "Retrieve and analyze market trends",
        APIDataSource("mock://market-trends"),
        MarketTrendsProcessor(groq_client),
        "API", "red"
    )

    # Run the pipeline
    insights = pipeline.run()

    # Summarize results using LLM
    summarizer = SummarizationProcessor(groq_client)
    final_summary = summarizer.process(insights)

    console.print(Panel(final_summary, title="[bold]Final Summary[/bold]", border_style="magenta"))


if __name__ == "__main__":
    main()