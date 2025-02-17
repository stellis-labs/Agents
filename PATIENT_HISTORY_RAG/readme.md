# 🏥 Patient History Analyzer (RAG-Powered)

## 📚 Overview

The Patient History Analyzer is an AI-powered Retrieval-Augmented Generation (RAG) application designed to help healthcare professionals quickly understand a patient's medical history. By integrating multiple worker agents and leveraging LLMs (Groq API), this system retrieves, analyzes, and presents patient medical data in a concise and actionable summary.

This tool streamlines the diagnostic process, improves decision-making efficiency, and provides doctors with relevant insights from scattered medical records.

---

## 🔍 Problem Statement

Doctors often need to quickly understand a patient's medical history to make informed decisions. However, medical histories can be lengthy, complex, and scattered across multiple sources, making it time-consuming to extract relevant insights.

---

## 💡 Solution

The **Patient History Analyzer** is a Retrieval-Augmented Generation (RAG) application that streamlines the process of summarizing patient history. It leverages vector databases and LLMs to retrieve, analyze, and present patient history in a concise, readable format for healthcare professionals.

---

## 🚀 Key Features

RAG-based Retrieval: Retrieves structured and unstructured patient data from multiple sources.

Natural Language Query: Accepts user input in plain text and answers questions about the patient's medical history.

Multi-Agent Collaboration: Utilizes multiple specialized agents:

Retriever Agent: Gathers patient data from EHR and medical records.

Validator Agent: Validates data integrity.

Analyzer Agent: Identifies patterns, trends, and risks.

Contextualizer Agent: Adds clinical context based on guidelines.

Decision Support Agent: Suggests next steps for doctors.

Presenter Agent: Summarizes the final report in a readable format.

LLM-Powered Summary: Generates precise AI-enhanced summaries using Groq API.

Fast and Efficient: Optimized with sentence transformers (device support: MPS, CUDA) and ChromaDB for rapid vector similarity search.

Console-based Visualization: Uses Rich library for visually appealing outputs.

---

## 📋 Prerequisites

- Python 3.9+
- Jupyter Notebook (Optional)
- Virtual Environment (Recommended)

---

## 🛠️ Tech Stack

Python - Core programming language.

Sentence Transformers - Embedding model for data chunks.

ChromaDB - Vector similarity search for RAG.

Groq API (DeepSeek LLM) - LLM-powered patient history summary.

Rich Library - Console-based visualization.

Pandas - Data manipulation and processing.

---

## 📁 Detailed Folder Structure

```
PATIENT_HISTORY_RAG/
│── chromadb/                     # Persistent vector database for embeddings
│── data/                         # Patient medical data (CSV & Text Files)
│── .env                          # Environment variables 
│── .gitignore                    # Ignore sensitive files (e.g., .env, chromadb, data)
│── data.zip                      # Sample patient data archive
│── Patient-History-RAG.ipynb     # Jupyter Notebook containing the full implementation
│── requirements.txt               # Python dependencies
│── README.md                      # Project documentation

```

---

## 🚀 Getting Started

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/Komal-A99/Komal-AI-Patient-History-Dev.git

cd PATIENT_HISTORY_RAG

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

```

---

## Setting Up API Key

Create a `.env` file in your project directory:
```
GROQ_API_KEY=your_api_key_here
```
**DO NOT PUSH `.env` TO GITHUB.**

Add `.env` to `.gitignore` file:
```
.env
```

---

## 🏗️ System Design


Architectural Overview

The Patient History Analyzer is built using a modular, multi-agent RAG architecture optimized for speed and medical data handling.

![System Design](./System-Design-Patient-History-Analyzer.png)

---

### 🔄 Data Flow

1. **Input**: User provides Patient ID and query.
2. **Retrieval**: Patient data is fetched and embedded.
3. **Vector Search**: Relevant chunks are retrieved from ChromaDB.
4. **Validation**: Missing or erroneous data is flagged.
5. **Analysis**: Retrieved chunks are analyzed based on the query.
6. **Contextualization**: Insights are enriched with clinical context.
7. **Decision Support**: Suggestions are made for the next steps.
8. **LLM Summary**: Concise summary is generated via DeepSeek LLM.
9. **Output**: Summary is displayed to the user.

---

## 🖥️ Sample Query & Output


``` Example Query: 
    Doctor: What are the patient’s chronic conditions?
```

``` Example Output:
    **Patient History Summary:**
    - Chronic Conditions: Hypertension, Hyperlipidemia

    **Contextualized Insights:**
    Hypertension and Hyperlipidemia require lifestyle modification and medication adherence.

    **Suggested Next Steps:**
    1. Review current medication adherence.
    2. Schedule blood pressure monitoring.   
```     

---

## 🚀 Future Enhancements

- Integrate Real-Time EHR APIs
- Implement Caching Mechanism for Faster Retrieval
- Expand Contextualization with Medical Knowledge Graphs
- Support for Multi-Modal Data (e.g., Images, PDFs)

---

## 📜 License

This project is licensed under the MIT License. 

---

## 📧 Contact

Got questions or feedback? 

Reach out:

Email: komalalbhar1999@gmail.com

LinkedIn: https://www.linkedin.com/in/komalalbhar/

GitHub: https://github.com/Komal-A99

Let's improve healthcare solutions together! 🚀

---

## 📄 MIT License

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```