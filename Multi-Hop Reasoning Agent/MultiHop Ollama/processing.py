import requests

class BaseProcessor:
    """Base processor for interacting with Ollama API."""
    
    def __init__(self, config):
        self.api_url = config.get_api_url()

    def process(self, data, prompt, system_message):
        response = requests.post(
            self.api_url,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "system": system_message,
                "stream": False
            }
        )
        return response.json()["response"]


class SalesProcessor(BaseProcessor):
    def process(self, data):
        if not data["sql_data"]:
            return "No sales data available."
        sales_records = "\n".join([str(record) for record in data["sql_data"]])
        return super().process(data, f"Analyze the following sales data:\n\n{sales_records}", "You are an expert business analyst.")


class FeedbackProcessor(BaseProcessor):
    def process(self, data):
        return super().process(data, f"Analyze customer feedback:\n\n{data['document_text']}", "You are an expert in sentiment analysis.")


class CompetitorProcessor(BaseProcessor):
    def process(self, data):
        return super().process(data, f"Analyze competitor data:\n\n{data['competitors']}", "You are an expert in competitor analysis.")


class MarketTrendsProcessor(BaseProcessor):
    def process(self, data):
        return super().process(data, f"Analyze market trends:\n\n{data['market_trends']}", "You are an expert market analyst.")