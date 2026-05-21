from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import anthropic
from dotenv import load_dotenv
import os
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

# ---- Initialize FastAPI app ----
app = FastAPI(
    title="COBOL to Java RAG Assistant",
    description="Convert COBOL code to Java using AI and RAG",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ui")
def ui():
    return FileResponse("static/index.html")

# ---- Load examples from JSON ----
def load_examples():
    with open("cobol_examples.json", "r") as f:
        data = json.load(f)
    return data["examples"]

# ---- Setup ChromaDB ----
def setup_chromadb():
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="cobol_examples")
    examples = load_examples()
    documents = []
    metadatas = []
    ids = []
    for example in examples:
        documents.append(example["cobol"])
        metadatas.append({
            "java": example["java"],
            "category": example["category"],
            "explanation": example["explanation"]
        })
        ids.append(example["id"])
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"✅ Loaded {len(examples)} examples into ChromaDB")
    return collection

# ---- Initialize ChromaDB on startup ----
collection = setup_chromadb()

# ---- Request and Response models ----
class ConvertRequest(BaseModel):
    cobol_code: str

class ConvertResponse(BaseModel):
    cobol_code: str
    java_code: str
    similar_examples: list

# ---- RAG Functions ----
def retrieve_examples(cobol_code):
    results = collection.query(
        query_texts=[cobol_code],
        n_results=3
    )
    examples = []
    for i, doc in enumerate(results['documents'][0]):
        java = results['metadatas'][0][i]['java']
        explanation = results['metadatas'][0][i]['explanation']
        examples.append({
            "cobol": doc,
            "java": java,
            "explanation": explanation
        })
    return examples

def build_prompt(cobol_code, examples):
    examples_text = "\n\n".join([
        f"COBOL: {ex['cobol']}\nJava: {ex['java']}\nNote: {ex['explanation']}"
        for ex in examples
    ])
    return f"""You are a COBOL to Java migration expert.

Here are some similar migration examples:
{examples_text}

Now convert this COBOL code to Java:
{cobol_code}

Provide only the Java code and a brief explanation."""

def generate_java(prompt):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# ---- API Endpoints ----
@app.get("/")
def home():
    return {
        "message": "COBOL to Java RAG Assistant",
        "usage": "POST /convert with cobol_code field",
        "docs": "/docs"
    }

@app.post("/convert", response_model=ConvertResponse)
def convert_cobol(request: ConvertRequest):
    similar_examples = retrieve_examples(request.cobol_code)
    prompt = build_prompt(request.cobol_code, similar_examples)
    java_code = generate_java(prompt)
    return ConvertResponse(
        cobol_code=request.cobol_code,
        java_code=java_code,
        similar_examples=similar_examples
    )

@app.get("/health")
def health():
    return {"status": "healthy"}