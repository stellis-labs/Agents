import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv()
my_api_key = os.getenv("API_KEY")

# Import Groq API Client
from groq import Groq

# Initialize console for Rich output
console = Console()

class QueryParser:
    """Parses user queries using LLM to extract actionable tasks"""
    
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def parse(self, query):
        """Extracts key analysis targets from user query"""
        prompt = f"""Analyze the following user query and identify the key factors or entities that need to be analyzed. 
        Return your response as a comma-separated list of terms, each term being a noun or noun phrase. 
        Do not include any additional text.

        Query: {query}
        Response:"""
        
        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key analysis targets from user queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        
        response_text = response.choices[0].message.content
        tasks = [f"Analyze {term.strip()}" for term in response_text.split(",") if term.strip()]
        return tasks


# Data Sources #
class SQLDataSource:
    """Handles retrieving data from an SQLite database."""
    def __init__(self, db_path, query):
        self.db_path = db_path
        self.query = query

    def fetch_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(self.query)
        data = cursor.fetchall()
        conn.close()
        return {"sql_data": data}


class DocumentParser:
    """Handles extracting text data from PDF documents."""
    def __init__(self, file_path):
        self.file_path = file_path

    def fetch_data(self):
        if self.file_path.endswith(".pdf"):
            text = self._parse_pdf()
        else:
            raise ValueError("Unsupported file format.")
        return {"document_text": text}

    def _parse_pdf(self):
        reader = PdfReader(self.file_path)
        text = "".join([page.extract_text() for page in reader.pages])
        return text


class APIDataSource:
    """Handles API data retrieval for competitor and market data."""
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        if "competitors" in self.api_url:
            return {"competitors": "Competitors in Region A offer durable products at competitive prices."}
        elif "market-trends" in self.api_url:
            return {"market_trends": "Growing demand for sustainable and durable products in Region A."}
        else:
            raise ValueError("Invalid API URL")


# Parallel Processing #
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


# Data Processors #
class SalesProcessor:
    """Processes sales data using LLM for real insights."""
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def process(self, data):
        if not data["sql_data"]:
            return "No sales data available."

        # Format data for LLM analysis
        sales_records = "\n".join([str(record) for record in data["sql_data"]])

        # Prompt LLM to analyze sales trends
        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert business analyst."},
                {"role": "user", "content": f"Analyze the following sales data and provide insights:\n\n{sales_records}"}
            ],
            temperature=0,
        )
        return response.choices[0].message.content


class FeedbackProcessor:
    """Processes customer feedback using LLM for real insights."""
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def process(self, data):
        feedback_text = data["document_text"]

        if not feedback_text.strip():
            return "No feedback data available."

        # Prompt LLM to analyze customer sentiment
        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert in customer sentiment analysis."},
                {"role": "user", "content": f"Analyze the following customer feedback and provide insights:\n\n{feedback_text}"}
            ],
            temperature=0,
        )
        return response.choices[0].message.content


class CompetitorProcessor:
    """Processes competitor data using LLM for real insights."""
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def process(self, data):
        competitor_info = data.get("competitors", "")

        if not competitor_info.strip():
            return "No competitor data available."

        # Prompt LLM to analyze competitor strategy
        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert in competitor analysis."},
                {"role": "user", "content": f"Analyze the following competitor data and provide insights:\n\n{competitor_info}"}
            ],
            temperature=0,
        )
        return response.choices[0].message.content


class MarketTrendsProcessor:
    """Processes market trends using LLM for real insights."""
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def process(self, data):
        market_trends_info = data.get("market_trends", "")

        if not market_trends_info.strip():
            return "No market trend data available."

        # Prompt LLM to analyze market trends
        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert market analyst."},
                {"role": "user", "content": f"Analyze the following market trend data and provide insights:\n\n{market_trends_info}"}
            ],
            temperature=0,
        )
        return response.choices[0].message.content


class SummarizationProcessor:
    """Summarizes insights using LLM."""
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def process(self, insights):
        """Generates final summary using LLM."""
        combined_text = " ".join(insights)
        
        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Create a concise, actionable summary of the following business insights."},
                {"role": "user", "content": combined_text}
            ]
        )

        return response.choices[0].message.content


def main():
    console.print("[bold cyan]\nEnhanced Multi-Hop Reasoning Agent[/bold cyan]\n")

    # Initialize Groq Client
    groq_client = Groq(api_key=my_api_key)

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