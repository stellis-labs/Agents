import os
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import spacy
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# The rest of the imports and classes remain the same until the SummarizationProcessor
# Only showing the modified parts for clarity
# === NLP-Based Query Parser === #
class QueryParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")  # Use SpaCy's local model

    def parse(self, query):
        doc = self.nlp(query)
        tasks = [f"Analyze {token.text.lower()}" for token in doc if token.dep_ in ("nsubj", "dobj")]
        return tasks

# === Extended Data Retrieval === #
class SQLDataSource:
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
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


class APIDataSource:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        # Mock API responses
        if "competitors" in self.api_url:
            return {"competitors": "Competitors in Region A offer durable products at competitive prices."}
        elif "market-trends" in self.api_url:
            return {"market_trends": "Growing demand for sustainable and durable products in Region A."}
        else:
            raise ValueError("Invalid API URL")


# === Parallel Execution === #
class ParallelReasoningPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, description, data_source, processor):
        self.steps.append({"description": description, "data_source": data_source, "processor": processor})

    def run(self):
        results = []

        def process_step(step):
            print(f"\n{step['description']}")
            data = step["data_source"].fetch_data()
            insights = step["processor"].process(data)
            print(f"Insights: {insights}")
            return insights

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_step, step) for step in self.steps]
            for future in futures:
                results.append(future.result())

        return results


# === Enhanced Reasoning Logic === #
class SalesProcessor:
    def process(self, data):
        return f"Sales data: {data['sql_data']}"


class FeedbackProcessor:
    def process(self, data):
        return f"Customer feedback: {data['document_text'][:200]}..."  # Truncate for readability


class CompetitorProcessor:
    def process(self, data):
        return f"Competitor insights: {data['competitors']}"


class MarketTrendsProcessor:
    def process(self, data):
        return f"Market trends: {data['market_trends']}"

class SummarizationProcessor:
    """
    Summarizes insights using the Ollama API.
    """

    def __init__(self, model_name="tinyllama"):
        """
        Initialize the Ollama summarizer.
        :param model_name: Name of the Ollama model to use (default: tinyllama).
        """
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def process(self, insights):
        """
        Summarizes the combined insights using the Ollama API.
        :param insights: List of insights to summarize.
        :return: Summarized text.
        """
        combined_text = " ".join(insights)
        
        # Prepare the prompt
        prompt = f"""Please summarize the following insights concisely:

{combined_text}

Summary:"""

        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            # Make request to Ollama API
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            # Extract the response
            result = response.json()
            return result.get('response', "Unable to generate summary.")
            
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"

def main():
    """
    Entry point for the program. Orchestrates query processing, reasoning steps, and summarization.
    """
    print(" Enhanced Multi-Hop Reasoning Agent \n")

    # Initialize components
    query = "What are the key factors driving the decline in sales for Product X in the last quarter?"
    query_parser = QueryParser()
    tasks = query_parser.parse(query)
    print(f"Parsed Tasks: {tasks}")

    # Initialize the pipeline
    pipeline = ParallelReasoningPipeline()

    # Add reasoning steps
    pipeline.add_step(
        "Analyze sales data",
        SQLDataSource("sales.db", "SELECT * FROM sales WHERE product='Product X'"),
        SalesProcessor(),
    )
    pipeline.add_step(
        "Analyze customer feedback",
        DocumentParser("feedback.pdf"),
        FeedbackProcessor(),
    )
    pipeline.add_step(
        "Analyze competitor data",
        APIDataSource("mock://competitors"),
        CompetitorProcessor(),
    )
    pipeline.add_step(
        "Analyze market trends",
        APIDataSource("mock://market-trends"),
        MarketTrendsProcessor(),
    )

    # Run the pipeline
    insights = pipeline.run()

    # Summarize results using Ollama
    summarizer = SummarizationProcessor(model_name="tinyllama")  # You can change the model as needed
    final_summary = summarizer.process(insights)

    print("\nFinal Summary")
    print(final_summary)

if __name__ == "__main__":
    main()