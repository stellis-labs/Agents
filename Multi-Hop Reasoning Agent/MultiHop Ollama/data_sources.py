import sqlite3
from PyPDF2 import PdfReader

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
        reader = PdfReader(self.file_path)
        text = "".join([page.extract_text() for page in reader.pages])
        return {"document_text": text}


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