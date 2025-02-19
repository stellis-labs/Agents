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