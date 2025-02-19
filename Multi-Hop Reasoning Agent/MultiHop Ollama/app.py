from config import Config
from query_parser import QueryParser
from parallel_pipeline import ParallelReasoningPipeline
from data_sources import SQLDataSource, DocumentParser, APIDataSource
from processing import SalesProcessor, FeedbackProcessor, CompetitorProcessor, MarketTrendsProcessor
from summarization import SummarizationProcessor
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print("[bold cyan]\nEnhanced Multi-Hop Reasoning Agent[/bold cyan]\n")

    # Load configuration
    config = Config()

    # Parse the query using Ollama API
    query = "What are the key factors driving the decline in sales for Product X in the last quarter?"
    query_parser = QueryParser(config)
    tasks = query_parser.parse(query)
    console.print(Panel(f"Parsed Tasks: {tasks}", title="Query Parsing", border_style="cyan"))

    # Initialize the pipeline
    pipeline = ParallelReasoningPipeline()

    # Add reasoning steps
    pipeline.add_step(
        "Retrieve and analyze sales data for Product X",
        SQLDataSource("sales.db", "SELECT * FROM sales WHERE product='Product X'"),
        SalesProcessor(config),
        "SQL Database", "blue"
    )
    pipeline.add_step(
        "Retrieve and analyze customer feedback for Product X",
        DocumentParser("feedback.pdf"),
        FeedbackProcessor(config),
        "Document", "green"
    )
    pipeline.add_step(
        "Retrieve and analyze competitor data",
        APIDataSource("mock://competitors"),
        CompetitorProcessor(config),
        "API", "yellow"
    )
    pipeline.add_step(
        "Retrieve and analyze market trends",
        APIDataSource("mock://market-trends"),
        MarketTrendsProcessor(config),
        "API", "red"
    )

    # Run the pipeline
    insights = pipeline.run()

    # Summarize results using Ollama
    summarizer = SummarizationProcessor(config)
    final_summary = summarizer.process(insights)

    console.print(Panel(final_summary, title="[bold]Final Summary[/bold]", border_style="magenta"))

if __name__ == "__main__":
    main()