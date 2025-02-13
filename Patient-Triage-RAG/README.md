# 🏥 **Patient Triage Gen AI**  
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-00BFFF?style=flat&logo=groq&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF4500?style=flat&logo=chromadb&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-000000?style=flat&logo=rag&logoColor=white)

**Patient Triage Gen AI** is an intelligent application designed to prioritize patients based on the severity of their medical conditions. It uses a **Retrieval-Augmented Generation (RAG)** architecture powered by **Groq** and **ChromaDB** to provide accurate and context-aware triage recommendations.  

---

## 🚀 **Key Features**
- **Patient Triage Levels**: Assigns one of 5 triage levels based on severity:
  - Level 1: Resuscitation (Immediate life-threatening condition)
  - Level 2: Emergency (Potentially life-threatening condition)
  - Level 3: Urgent (Serious but not life-threatening condition)
  - Level 4: Semi-Urgent (Less serious condition)
  - Level 5: Non-Urgent (Minor or stable condition)
- **Knowledge Base**: Uses a comprehensive database of medical guidelines and protocols for triage.
- **RAG Architecture**: Combines retrieval of relevant guidelines with generative AI for detailed explanations.
- **Console-Based Interface**: Provides a user-friendly console interface for input and output.
- **Real-Time Processing**: Generates triage reports in real-time using Groq's high-performance LLM.

---

## 🛠️ **Tech Stack**
- **Backend**: FastAPI
- **AI Model**: Groq (LLaMA 3.2-90B Vision Preview)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Console Interface**: Rich (for formatted output)
- **Environment Management**: Python Virtual Environment (`.venv`)

---

## Execution Screenshot: 
### Console Interface
![image](https://github.com/user-attachments/assets/d7f55fb8-723e-49ae-b2a0-5a164a785822)

### React JS
<img width="1438" alt="image" src="https://github.com/user-attachments/assets/b67c07d3-e366-41be-b8a4-d7745898fbe2" />
<br />
<br />
<img width="1422" alt="image" src="https://github.com/user-attachments/assets/912cb7f2-80e0-4d88-9519-21bf635266ae" />

---

## 📂 **Repository Structure**
patient_triage_gen_ai/ </br>
├── app/                     # FastAPI application </br>
│   ├── main.py              # FastAPI server and endpoints </br>
│   ├── models.py            # Pydantic models for request/response </br>
│   ├── chromadb_utils.py    # ChromaDB utility functions </br>
│   └── groq_utils.py        # Groq API utility functions </br>
├── console_interfaces.py    # Console-based interface for user interaction </br>
├── requirements.txt         # Python dependencies </br>
├── .env.example             # Environment variables template </br>
└── README.md                # Project documentation </br>


## 🚀 Getting Started
### Prerequisites
- Python 3.10 or higher
- Groq API Key (Get it from Groq Cloud)
- ChromaDB (for local vector storage)

## Installation
**Step 1: Clone the repository:**
```
git clone https://github.com/varshahindupur09/patient_triage_gen_ai.git
cd patient_triage_gen_ai
```

**Step 2: Set up a virtual environment and install dependencies:**

```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Step 3: Set up environment variables:**
- Rename .env.example to .env.
- Add your Groq API key:
```
GROQ_API_KEY=enter_your_groq_api_key_here
```

- Initialize ChromaDB with medical guidelines
```
python app/chromadb_utils.py
```

- Run the FastAPI server:
```
uvicorn app.main:app --reload
```

- Use the console interface:
```
python console_interfaces.py
```
- To use React UI
```
cd ui
npm install
npm start
```

## 🖥️ Usage

### Console Interface:

- Run the console interface:
```
python console_interfaces.py
```
### Output:
```
Enter patient details:
Symptoms: Sudden severe headache, difficulty speaking, weakness on one side of the body.
History: None.
Preliminary Diagnosis: Suspected stroke.

View the triage report:
Triage Level: Level 1 (Resuscitation)
Explanation: Immediate life-threatening condition. The patient requires resuscitation and urgent medical attention.
```

### API Endpoints
```
GET /: Welcome message.
POST /assign-triage-level/: Assigns a triage level based on patient data.
```
```
Request Body:
{
  "symptoms": "Severe chest pain, radiating to the left arm, sweating, nausea",
  "history": "High blood pressure, family history of heart disease",
  "diagnosis": "Suspected myocardial infarction"
}
Response:
{
  "steps": [
    {
      "description": "Analyzing Patient Report...",
      "details": {
        "symptoms": ["Severe chest pain", "radiating to the left arm", "sweating", "nausea"],
        "history": ["High blood pressure", "family history of heart disease"],
        "diagnosis": "Suspected myocardial infarction"
      }
    },
    {
      "description": "Assigning Triage Level...",
      "details": {
        "condition": "myocardial infarction",
        "level": "Level 1 (Resuscitation)"
      }
    }
  ],
  "final_output": {
    "triage_level": "Level 1 (Resuscitation)",
    "explanation": "Immediate life-threatening condition. The patient requires resuscitation and urgent medical attention."
  },
  "confidence": 0.95,
  "guidelines_used": ["myocardial infarction"]
}
```

## 📊 Example Domains for Testing
Cardiology: Heart attack, arrhythmia, heart failure.
Trauma: Severe injuries, fractures, burns.
Neurology: Stroke, seizures, severe migraines.
Pediatrics: High fever, dehydration, respiratory distress.
General Medicine: Minor injuries, infections, chronic conditions.

## 🛠️ Future Enhancements
Multilingual Support: Handle patient reports in multiple languages.
EHR Integration: Integrate with Electronic Health Records (EHR) for automated data retrieval.
Confidence Scoring: Improve confidence scoring based on retrieval distances.
Deployment: Deploy the application using Docker and Kubernetes for scalability.

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
### This project is licensed under the MIT License. See the LICENSE file for details.

## 📧 Contact
For questions or feedback, feel free to reach out:
**Email:** varshashindupur@gmail.com
**LinkedIn:** [Varsha Hindupur](https://www.linkedin.com/in/varsha-hindupur/)
**GitHub:** https://www.github.com/varshahindupur09
