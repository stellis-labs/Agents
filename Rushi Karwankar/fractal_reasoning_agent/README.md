# 🌀 Fractal Reasoning Agent (FRA)

**⚠️ NOTICE: This project is still under development. Expect frequent changes and improvements. ⚠️**

## 🔍 Overview

The Fractal Reasoning Agent (FRA) is an AI-powered system designed to tackle complex problems through fractal decomposition. The system breaks down complex problems into manageable sub-problems, processes them independently, and then integrates the solutions into a comprehensive answer.

## ✨ Key Features

- **🧩 Fractal Problem Decomposition**: Breaks complex problems into simpler, manageable components
- **⚡ Parallel Processing**: Solves sub-problems concurrently for efficiency
- **🔍 Quality Control**: Evaluates and optimizes solutions at every level
- **🔄 Integration Framework**: Combines sub-solutions into cohesive final answers
- **🧠 Powered by LLM**: Leverages Ollama's llama3.1 for reasoning capabilities

## 🏗️ Architecture

The FRA system consists of four main layers:
1. **📥 Problem Input Layer**: Processes and analyzes the input problem
2. **📊 Decomposition Layer**: Breaks down complex problems into sub-problems
3. **⚙️ Processing Layer**: Solves, evaluates, and optimizes each sub-problem
4. **🔗 Integration Layer**: Combines sub-solutions into a coherent final solution

## 📋 Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com/) with llama3.1:latest model

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fractal-reasoning-agent
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama server** (in a separate terminal):
   ```bash
   ollama serve
   ```

5. **Pull the llama3.1 model**:
   ```bash
   ollama pull llama3.1:latest
   ```

6. **Run the agent**:
   ```bash
   python main.py --problem "Design a sustainable city transportation system that reduces carbon emissions while accommodating a growing population."
   ```

## 🛠️ Usage

```bash
python main.py [--problem PROBLEM] [--config CONFIG] [--output OUTPUT]
```

- `--problem`: The problem statement to solve
- `--config`: Path to configuration file (default: config/default_config.json)
- `--output`: Path to save the output (default: output/solution.json)

If no problem is provided via command line, you will be prompted to enter one.

## 💡 Example Problems

- "Design a sustainable city transportation system that reduces carbon emissions while accommodating a growing population."
- "Develop a comprehensive strategy to improve education outcomes in underserved communities."
- "Create a plan to reduce hospital readmission rates for chronic disease patients."

## 📁 Project Structure

```
fractal_reasoning_agent/
├── config/
│   └── default_config.json
├── layers/
│   ├── __init__.py
│   ├── input_layer.py
│   ├── decomposition_layer.py
│   ├── processing_layer.py
│   └── integration_layer.py
├── __init__.py
├── main.py
├── fra_system.py
├── ollama_client.py
└── requirements.txt
```

## 👥 Contribution

As this project is under active development, contributions are welcome. Please check the issue tracker for current development priorities.

## 📜 License

[MIT License](LICENSE)

## ⚠️ Disclaimer

This project is a research prototype and should not be used for critical decision-making without human oversight.
