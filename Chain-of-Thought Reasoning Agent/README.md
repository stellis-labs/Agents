# 🧠 Chain of Thought (CoT) Reasoning Agent  

The **Chain of Thought (CoT) Reasoning Agent** is a console-based AI agent designed to solve complex problems by breaking them down into smaller, manageable steps and progressively refining the reasoning process using modular sub-agents.  

---

## 🚀 Project Overview  
The CoT Reasoning Agent uses a hierarchical tree structure to simulate human-like logical reasoning. The agent dynamically creates and manages sub-agents to handle different layers of reasoning, including:  
- ✅ Identifying key components of the problem  
- ✅ Generating intermediate questions  
- ✅ Forming hypotheses  
- ✅ Evaluating hypotheses  
- ✅ Generating solutions  
- ✅ Consolidating results into a final recommendation  

The agent supports both **local LLM models** (using Ollama) and **cloud-based models** (using Groq).  

---

## 🎯 Features  
- **Dynamic Problem Decomposition** – Breaks down problems into a multi-layered tree structure  
- **Modular Sub-Agent Handling** – Dynamically spawns sub-agents at each step  
- **Multiple LLM Support** – Supports Ollama (local) and Groq (cloud-based)  
- **Efficient Caching** – Reduces redundant API calls using `@lru_cache`  
- **Structured Output** – Clean and structured console output using `rich`  

---

## 📂 Project Structure  
CoT_Reasoning_Agent/ 
├── main.py # Entry point for user input

├── reasoning_agent.py # Main reasoning agent 

├── agents/ # Handles CoT tree logic 

│ ├── reasoning_tree.py # Expands CoT tree recursively 

│ ├── sub_agent.py # Sub-agent logic for each step 

├── llm_interfaces/ # LLM integration 

│ ├── base_llm.py # Base LLM interface 

│ ├── ollama_llm.py # Ollama LLM client 

│ ├── groq_llm.py # Groq LLM client 

│ ├── llm_factory.py # Dynamically selects LLM 

├── utils/ # Utility functions 

│ ├── response_cleaner.py # Cleans raw LLM output 

│ ├── display_manager.py # Handles console output formatting 

└── README.md # Project documentation

---
## ⚙️ Setup Instructions  

### 1. **Clone the Repository**  
```git
git clone https://github.com/your-repo/cot-reasoning-agent.git
cd cot-reasoning-agent
```

2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
```
## OR
```bash
.\venv\Scripts\activate   # Windows
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. (Optional) Set Up API Key
If using Groq, set your API key directly in the terminal:

For Mac/Linux:
```bash
export GROQ_API_KEY="your-groq-api-key"
```
For Windows (Command Prompt):
```cmd
set GROQ_API_KEY=your-groq-api-key
```
For Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="your-groq-api-key"
```

5. Start the Application
```bash
python main.py
```

### 🧠 How It Works
The user enters a problem statement in the console.  
The agent identifies the problem domain and breaks it down into key components.  
Each key component is passed to sub-agents to generate intermediate questions.  
Sub-agents create hypotheses based on each question.  
Hypotheses are evaluated, leading to solutions.  
Historical data is used to evaluate solutions.  
A final recommendation is generated based on all outcomes.  
💡 Example Output  
```
Problem Statement: How can we optimize the delivery routes for a fleet of 50 vehicles in a congested city?

╭──────────────────── Step 1: Identify Key Components ────────────────────╮
│ - Traffic congestion impact                                              │
│ - Route optimization strategies                                          │
│ - Fuel efficiency concerns                                               │
│ - Vehicle scheduling                                                     │
│ - Delivery time constraints                                              │
╰─────────────────────────────────────────────────────────────────────────╯

╭──────────────────── Step 2: Generated Questions ────────────────────────╮
│ - How can real-time data optimize delivery routes?                       │
│ - What alternative paths can reduce congestion?                          │
╰─────────────────────────────────────────────────────────────────────────╯

╭──────────────────── Step 3: Hypotheses ─────────────────────────────────╮
│ - Hypothesis 1: Using real-time traffic data can improve routing.        │
│ - Hypothesis 2: Identifying alternative routes during peak hours         │
╰─────────────────────────────────────────────────────────────────────────╯

╭──────────────────── Step 4: Hypotheses Evaluation ──────────────────────╮
│ - Hypothesis 1: Data from Google Maps shows a 20% improvement in timing. │
│ - Hypothesis 2: Historical traffic data supports alternative routes.      │
╰─────────────────────────────────────────────────────────────────────────╯

╭──────────────────── Step 5: Solutions ──────────────────────────────────╮
│ - Solution 1: Implement real-time traffic data in the routing algorithm.  │
│ - Solution 2: Pre-identify alternative routes for peak hours.             │
╰─────────────────────────────────────────────────────────────────────────╯

╭──────────────────── Step 6: Final Recommendation ────────────────────────╮
│ - Integrate real-time traffic data into the routing system.               │
│ - Pre-identify alternative routes for use during peak traffic hours.       │
╰─────────────────────────────────────────────────────────────────────────╯
```
## 🛠️ Tech Stack
Python – Core language  
Rich – For console formatting  
Ollama – Local LLM execution  
Groq – Cloud-based LLM execution  
requests – For API communication  

## ✅ Key Design Decisions
Dynamic LLM Support – Supports both local and cloud-based models.  
Tree-Structured Reasoning – Hierarchical approach using recursive sub-agents.  
Efficient Resource Handling – Cached responses using @lru_cache.  
Modular Design – Clean separation of concerns for easy extension.  

## 🌟 Best Practices Followed
✔️ Clean and modular code structure  
✔️ Minimized redundant LLM calls using caching  
✔️ Secure handling of API keys using environment variables  
✔️ Graceful handling of user input and invalid responses  

## 🚀 Future Improvements
✅ Improve handling of real-time data sources  
✅ Add support for additional LLM providers (like OpenAI)  
✅ Improve multi-agent communication strategies  
✅ Test with more diverse problem domains  

## 👥 Contributors
Animesh Giri – Lead Developer  

## 📝 License
This project is licensed under the MIT License.  
