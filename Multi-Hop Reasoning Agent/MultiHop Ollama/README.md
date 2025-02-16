# Enhanced Multi-Hop Reasoning Agent

## Overview

This project implements a **Multi-Hop Reasoning Agent** that performs complex business intelligence analysis by integrating **structured** (SQL databases), **semi-structured** (APIs), and **unstructured** (PDF documents) data sources. It leverages an **LLM (TinyLlama)** to extract insights and synthesize a final summary.

## Features

* **Query Parsing** : Uses an LLM to extract key analysis targets from a user query.
* **Parallel Reasoning Pipeline** : Executes multiple data analysis tasks in parallel using `ThreadPoolExecutor`.
* **Multi-Source Data Retrieval** :
* SQL databases for structured data
* PDF documents for unstructured data
* APIs for real-time competitor and market trend analysis
* **AI-Driven Data Processing** :
* LLM-powered sales analysis
* Customer feedback sentiment analysis
* Competitor strategy analysis
* Market trends extraction
* **Final Insight Summarization** : Generates a concise, actionable summary using an LLM.

## Dependencies

Ensure you have the following dependencies installed:

```bash
pip install requests PyPDF2 dotenv rich
```

## File Structure

```
.
├── main.py                # Main script to execute the reasoning agent
├── sales.db               # SQLite database (example file for sales data)
├── feedback.pdf           # Sample PDF file (example customer feedback)
├── .env                   # Environment variables (if needed)
├── README.md              # Project documentation
```

## How to Run

1. Start the **TinyLlama API Server** locally (ensure it's running on `localhost:11434`).
2. Run the script:

```bash
python main.py
```

3. The system will:
   * Parse the query
   * Retrieve relevant data
   * Process insights in parallel
   * Display stepwise results using **Rich**
   * Generate and display a final summary

## Example Query

**Input Query:**

```
What are the key factors driving the decline in sales for Product X in the last quarter?
```

**Pipeline Execution:**

1. **Retrieve & analyze sales data** (SQL Database)
2. **Retrieve & analyze customer feedback** (PDF Document)
3. **Retrieve & analyze competitor data** (API)
4. **Retrieve & analyze market trends** (API)
5. **Summarize insights** (LLM-based summary)

**Final Output:**

* Comprehensive insights into sales trends, customer sentiment, competitor strategies, and market shifts.

## Customization

* Modify `SQLDataSource` query for different product sales.
* Update `DocumentParser` to analyze different feedback files.
* Change API URLs to fetch real-time competitor and market data.
* Swap out `TinyLlama` with another LLM model.

## Future Enhancements

* Support for more file formats (CSV, JSON, etc.).
* Integration with real-world APIs for dynamic data.
* Improved prompt engineering for better LLM responses.

## License

MIT License

## Author

Developed by Mayur Kishor Kumar
