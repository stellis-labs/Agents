# patient_triage/app.py
from fastapi import FastAPI, HTTPException, Form, Request
from chromadb import Client
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb
from dotenv import load_dotenv
import os
import uvicorn
from pydantic import BaseModel
from typing import Dict, List, Union
import json
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from groq import Groq
import logging

logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Initialize ChromaDB
embed_fn = SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
chromadb_client = Client()
collection = chromadb_client.create_collection(
    name="medical_guidelines",
    embedding_function=embed_fn
)

# Define FastAPI app and response models
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://192.168.1.143:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

class TriageStep(BaseModel):
    description: str
    details: Union[dict, list, str]
    references: List[str] = []

class TriageResponse(BaseModel):
    steps: List[TriageStep]
    final_output: Dict[str, str]
    confidence: float
    guidelines_used: List[str]

class TriageRequest(BaseModel):
    symptoms: str
    history: str
    diagnosis: str

# Function to add documents to ChromaDB
def add_guidelines_to_chromadb():
    guidelines = [
        {
            "id": "1",
            "text": "Symptoms: Severe chest pain, radiating to the left arm, sweating, nausea. History: High blood pressure, family history of heart disease. Diagnosis: Suspected myocardial infarction (heart attack). Assign Level 1 (Resuscitation).",
            "metadata": {"condition": "myocardial infarction", "level": 1},
        },
        {
            "id": "2",
            "text": "Symptoms: Severe difficulty breathing, blue lips, unresponsiveness. History: None. Diagnosis: Severe asthma attack or respiratory arrest. Assign Level 1 (Resuscitation).",
            "metadata": {"condition": "severe asthma attack or respiratory arrest", "level": 1},
        },
        {
            "id": "3",
            "text": "Symptoms: Mild abdominal pain, no fever, no vomiting. History: None. Diagnosis: Gastritis. Assign Level 5 (Non-Urgent).",
            "metadata": {"condition": "gastritis", "level": 5},
        },
        {
            "id": "4",
            "text": "Symptoms: Sudden severe headache, difficulty speaking, weakness on one side of the body. History: None. Diagnosis: Suspected stroke. Assign Level 1 (Resuscitation).",
            "metadata": {"condition": "stroke", "level": 1},
        },
        {
            "id": "5",
            "text": "Symptoms: Sudden onset of severe abdominal pain, vomiting, inability to pass stool. History: History of abdominal surgery. Diagnosis: Suspected bowel obstruction. Assign Level 2 (Emergency).",
            "metadata": {"condition": "bowel obstruction", "level": 2},
        },
    ]
    for guideline in guidelines:
        collection.add(
            documents=[guideline["text"]],
            metadatas=[guideline["metadata"]],
            ids=[guideline["id"]]
        )

# Call this once to initialize the database
add_guidelines_to_chromadb()

# Function to retrieve context from ChromaDB
def retrieve_context_from_chromadb(query):
    try:
        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )
        return results["documents"], results["metadatas"], results["distances"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(e)}")

# Function to generate structured triage report using RAG
def generate_structured_triage_report(symptoms: str, history: str, diagnosis: str) -> dict:
    # Step 1: Retrieve relevant guidelines from ChromaDB
    query = f"Symptoms: {symptoms}, History: {history}, Diagnosis: {diagnosis}"
    documents, metadatas, distances = retrieve_context_from_chromadb(query)

    # Step 2: Augment the prompt with retrieved guidelines
    system_prompt = """You are a medical triage expert. Analyze the patient report and generate a structured response following these steps:

    1. Analyze Symptoms/History/Diagnosis
    2. Retrieve Relevant Guidelines
    3. Assign Triage Level
    4. Generate Explanation
    5. Final Output

    Follow this exact JSON format:
    {
        "steps": [
            {
                "description": "Analyzing Patient Report...",
                "details": {
                    "symptoms": ["list", "of", "key", "symptoms"],
                    "history": ["list", "of", "relevant", "history"],
                    "diagnosis": "preliminary diagnosis"
                }
            },
            {
                "description": "Retrieving Relevant Triage Guidelines...",
                "details": ["list", "of", "matched", "conditions"]
            },
            {
                "description": "Assigning Triage Level...",
                "details": {
                    "condition": "identified condition",
                    "level": "triage level with number"
                }
            },
            {
                "description": "Generating Explanation...",
                "details": "concise explanation linking symptoms/history to triage level"
            }
        ],
        "final_output": {
            "triage_level": "Level X (Category)",
            "explanation": "final concise explanation"
        }
    }"""

    user_input = f"""PATIENT DATA:
    - Symptoms: {symptoms}
    - History: {history}
    - Preliminary Diagnosis: {diagnosis}

    RELEVANT GUIDELINES:
    {documents}"""

    # Step 3: Generate the triage report using Groq (RAG)
    try:
        response = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",  # Use the appropriate Groq model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=1024,
            top_p=1,
            response_format={"type": "json_object"}
        )

        response_data = json.loads(response.choices[0].message.content)

        #  Step 4: Calculate confidence score based on retrieval distances
        if distances and distances[0]:  # Check if distances is not empty and has valid data
            flattened_distances = [d for sublist in distances for d in sublist]  # Flatten the list of lists
            average_distance = sum(flattened_distances) / len(flattened_distances)  # Calculate average
            confidence_score = 1 - average_distance  # Normalize to [0, 1]
        else:
            confidence_score = 0  # Default to 0 if no distances are available


        # Step 5: Add RAG metadata to the response
        response_data["confidence"] = confidence_score
        # response_data["guidelines_used"] = [m["condition"] for m in metadatas]
        flat_metadatas = [item for sublist in metadatas for item in sublist]
        response_data["guidelines_used"] = [m["condition"] for m in flat_metadatas if isinstance(m, dict) and "condition" in m]

        # Logging the response data for debugging
        logging.debug(f"Response Data: {response_data}")

        return response_data

    except json.JSONDecodeError:
        raise HTTPException(500, "Invalid JSON response from LLM")
    except Exception as e:
        raise HTTPException(500, f"Generation error: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Patient Triage Application"}

@app.post("/assign-triage-level/", response_model=TriageResponse)
@limiter.limit("10/minute")
async def assign_triage_level(
    request: Request,
    # symptoms: str = Form(...),
    # history: str = Form(...),
    # diagnosis: str = Form(...)
    triage_request: TriageRequest
):
    try:
        report = generate_structured_triage_report(
            triage_request.symptoms, 
            triage_request.history, 
            triage_request.diagnosis
        )
        # return report
        return TriageResponse(**report)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    add_guidelines_to_chromadb()
    uvicorn.run(app, host="0.0.0.0", port=8001)