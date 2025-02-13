# Doctor Recommendation System

This is an doctor recommendation system that analyzes patient reports and suggests relevant doctors based on their specialization and experience. 
The system uses **ChromaDB** for storing doctor profiles and **Ollama** for generating explanations.

## Features
- Accepts patient symptoms, history, and preliminary diagnosis.
- Retrieves relevant specializations from stored doctor profiles.
- Queries **ChromaDB** to find matching doctors.
- Uses **Ollama** for generating explanations on doctor suitability.
- Displays recommendations in a structured format using **Rich**.

## File Structure
/doctor_recommendation_system
│── Generation.ipynb            # Jupyter Notebook for running the doctor profile generation system
│── Recommendation.ipynb        # Jupyter Notebook for running the doctor profile recommendation system
│── requirements.txt            # Dependencies required for the project
│── README.md                   # Documentation for setup and usage
│── chroma_db/     


## Installation

### 1. Clone the repository:
```sh
    git clone https://github.com/saranya-m-ai/Agents.git

Setup & Installation

Install Anaconda if not already installed:Download Anaconda

Run the application using Jupyter Notebook:

    Open main.ipynb and run the cells to execute the doctor generation and recommendation system.


Usage

    Follow the prompts to enter symptoms, patient history, and preliminary diagnosis.

    The system will analyze the input and retrieve matching doctor profiles.

    Recommended doctors are displayed with specialization, experience, and suitability explanation.

Technologies Used

    ChromaDB - Stores and retrieves doctor profiles efficiently.

    Rich - Enhances the CLI experience with styled output.

    Ollama - Generates natural language explanations for doctor recommendations.
