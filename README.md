# **Enhanced Multi-Hop Reasoning Agent**

## **Overview**
This project implements an **Enhanced Multi-Hop Reasoning Agent**, designed to process complex queries, analyze multiple data sources in parallel, and summarize the insights using advanced natural language processing (NLP) techniques. The system integrates various components like SQL databases, PDF document parsing, API data retrieval, and summarization.

---

## **Key Features**
- **NLP Query Parsing**: Extracts actionable tasks from user queries using SpaCy.
- **Parallel Data Retrieval**: Fetches and processes data simultaneously from multiple sources.
- **Multiple Data Sources**:
  - SQL database for sales data.
  - PDF document parser for customer feedback.
  - Mock APIs for competitor and market trends analysis.
- **Summarization**: Combines and summarizes insights using the Groq API.
- **Scalable Pipeline**: Easily add new steps to the reasoning pipeline.

---

## **System Architecture**

1. **Query Parsing**:
   - The `QueryParser` extracts tasks like "Analyze sales data" from the user's query.

2. **Data Retrieval**:
   - **SQLDataSource**: Queries a SQLite database.
   - **DocumentParser**: Extracts text from PDF files.
   - **APIDataSource**: Retrieves data from mock APIs.

3. **Parallel Processing**:
   - Uses Python's `ThreadPoolExecutor` to analyze data from multiple sources simultaneously.

4. **Insight Processing**:
   - Each data source has a dedicated processor for specific insights (e.g., `SalesProcessor`, `FeedbackProcessor`).

5. **Summarization**:
   - Combines insights and summarizes them using the Groq API.

---

## **Installation**

### Prerequisites
- Python 3.8 or higher
- A virtual environment is recommended for dependencies.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/multi-hop-reasoning-agent.git
   cd multi-hop-reasoning-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the SpaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Create a `.env` file to store your Groq API key:
   ```env
   API_KEY=your_groq_api_key
   ```

---

## **Usage**

### Running the Program
1. Ensure the SQLite database (`sales.db`) is set up with the required table and data.
2. Place the PDF file (`feedback.pdf`) containing customer feedback in the project directory.
3. Execute the script:
   ```bash
   python main.py
   ```

### Output
The program processes the query, fetches insights, and prints a summarized report. Example output:
```
=== Enhanced Multi-Hop Reasoning Agent ===

Parsed Tasks: ['Analyze sales data', 'Analyze customer feedback', ...]

Analyze sales data
Insights: Sales data: [('Product X', 'Region A', 100), ...]

Analyze customer feedback
Insights: Customer feedback: Region A: Customers reported durability issues...

Analyze competitor data
Insights: Competitor insights: Competitors in Region A offer durable products...

Analyze market trends
Insights: Market trends: Growing demand for sustainable and durable products...

=== Final Summary ===
Key factors driving the decline in sales for Product X include durability issues in Region A, strong competition, and market demand for sustainability.
```

---

## **Project Structure**
```
multi-hop-reasoning-agent/
├── main.py                  # Main script
├── sales.db                 # SQLite database with sales data
├── feedback.pdf             # Sample PDF for customer feedback
├── requirements.txt         # Project dependencies
├── .env                     # Environment file for API keys
```

---

## **Key Components**

### Query Parsing (`QueryParser`)
- Parses user queries to identify relevant tasks.
- Powered by SpaCy’s dependency parsing.

### Data Sources
- **SQLDataSource**: Fetches sales data from an SQLite database.
- **DocumentParser**: Extracts text from PDFs using PyPDF2.
- **APIDataSource**: Simulates competitor and market trend data retrieval.

### Reasoning Pipeline (`ParallelReasoningPipeline`)
- Runs reasoning tasks in parallel for efficient analysis.

### Summarization (`SummarizationProcessor`)
- Combines and summarizes insights using the Groq API.

---

## **Extending the Project**

### Adding a New Data Source
1. Create a new class that implements the `fetch_data` method.
2. Add it as a step in the pipeline:
   ```python
   pipeline.add_step(
       "Description of task",
       NewDataSource(),
       NewProcessor(),
   )
   ```

### Customizing Summarization
Modify the `SummarizationProcessor` class to use a different summarization method or model.

---

## **Dependencies**
See `requirements.txt` for the full list of dependencies:
- `spacy`
- `PyPDF2`
- `fpdf`
- `groq`
- `transformers`
- `python-dotenv`

---

## **Contributing**
Contributions are welcome! Feel free to submit issues or pull requests.

---
