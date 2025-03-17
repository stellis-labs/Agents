**README.md**

# 🤖 Distributed Reasoning Agent

## Overview
The **Distributed Reasoning Agent** is an AI-driven system designed to decompose complex problems into structured sub-tasks, assign them to intelligent sub-agents, and synthesize results into a comprehensive solution. By leveraging **LLMs (Groq API & Gemini API) with LangChain**, this system efficiently automates problem-solving workflows, making it an ideal tool for research, automation, and decision-making processes.

## 🚀 Key Features
- **Automated Problem Decomposition**: Breaks down a user-input problem into sub-tasks.
- **Dynamic Sub-Agent Creation**: Generates dedicated sub-agents with meaningful names for targeted problem-solving.
- **LLM-Powered Execution**: Each sub-agent processes its task through an advanced language model.
- **Intelligent Result Synthesis**: Aggregates sub-agent findings into a structured, high-level summary.
- **Interactive Console Logging**: Provides clear, step-by-step execution insights using **Rich** for enhanced visualization.

## 📁 Detailed File Structure

```
Distributed-Reasoning-Agent/
│── agent.py                   # Main class for orchestrating task decomposition and execution
│── main.py                    # Entry point for user interaction
│── output.json                # Sub-agent logs saved in here
│── .env                        # Environment variables (API keys)
│── requirements.txt            # Dependencies for running the project
│── README.md                   # Project overview and usage guide
```

## 🚀 Getting Started
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Update `.env` file and add your ** API Key**:
   ```sh
   GROQ_API_KEY=your_api_key_here
   GEMINI_API_KEY=your_api_key_here
   ```
3. Run the agent:
   ```sh
   python main.py
   ```
4. Enter a problem statement when prompted and receive an intelligent breakdown and solution.

---

# System Design:

## **Architectural Overview**
The system follows a modular **multi-agent reasoning framework**, where an AI-powered main agent orchestrates the decomposition, delegation, execution, and synthesis of tasks using **LLMs (Groq API & Gemini API) with LangChain**.

## **Core Components**

### **1. User Interaction Module**
- Accepts a natural language problem statement from the user.
- Initiates the reasoning workflow via the `DistributedReasoningAgent`.

### **2. Problem Decomposition Engine**
- Utilizes AI to analyze and break down complex problems into structured sub-tasks.
- Generates a **maximum of 5** actionable sub-tasks.

### **3. Sub-Agent Management**
- Dynamically assigns **intelligent agent names** based on task requirements.
- Creates multiple `SubAgent` instances, each focused on a specific aspect of the problem.

### **4. Task Execution Module**
- Each sub-agent independently processes its assigned task using a large language model (LLM).
- Captures and logs insights for further synthesis.

### **5. Intelligent Result Synthesis**
- Aggregates and refines sub-agent outputs.
- Leverages an LLM to produce a **structured, insightful final solution**.
- Ensures clarity, coherence, and actionable recommendations.

## 🛠️ **Technology Stack**
- **Python** – Primary programming language
- **LangChain** – LLM integration and orchestration
- **Groq API & Gemini API** – Advanced AI model execution
- **Rich** – Enhanced console-based visualization
- **Dotenv** – Secure environment variable management

## **Workflow Diagram**
```
User Input → Problem Decomposition → Sub-Agent Creation → Task Execution → Result Synthesis → Output saved in JSON → Final Solution
```

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
Fork the repository.
```
Create a new branch (git checkout -b feature/your-feature-name).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Open a pull request.
```

## 📜 License

This project is licensed under the MIT License.

---

## 📧 Get in Touch

Hey there! Got questions, feedback, or just want to connect? Reach out to me:

- 📬 **Email:** [veda142.u@gmail.com](mailto:veda142.u@gmail.com)  
- 💼 **LinkedIn:** [linkedin.com/in/vedaupasanp](https://www.linkedin.com/in/vedaupasanp/)  
- 👨‍💻 **GitHub:** [github.com/VedaUpasan](https://github.com/VedaUpasan)  

Or, feel free to open an issue on the repo. Let’s build something cool together! 🌱