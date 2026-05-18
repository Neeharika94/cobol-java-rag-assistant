import chromadb
import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()

# ---- STEP 1: Load examples from JSON file ----
def load_examples():
    with open("cobol_examples.json", "r") as f:
        data = json.load(f)
    return data["examples"]

# ---- STEP 2: Setup ChromaDB and store examples ----
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

# ---- STEP 3: Retrieve similar examples (R of RAG) ----
def retrieve_examples(collection, cobol_code):
    results = collection.query(
        query_texts=[cobol_code],
        n_results=3
    )
    examples = []
    for i, doc in enumerate(results['documents'][0]):
        java = results['metadatas'][0][i]['java']
        explanation = results['metadatas'][0][i]['explanation']
        examples.append(f"COBOL: {doc}\nJava: {java}\nNote: {explanation}")
    return "\n\n".join(examples)

# ---- STEP 4: Build prompt (A of RAG) ----
def build_prompt(cobol_code, examples):
    return f"""You are a COBOL to Java migration expert.

Here are some similar migration examples:
{examples}

Now convert this COBOL code to Java:
{cobol_code}

Provide only the Java code and a brief explanation."""

# ---- STEP 5: Call Claude (G of RAG) ----
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

# ---- STEP 6: Full RAG Pipeline ----
def convert_cobol_to_java(collection, cobol_code):
    print(f"\n{'='*50}")
    print(f"Input COBOL: {cobol_code}")
    print(f"{'='*50}")

    print(f"\n--- Retrieved Examples (R) ---")
    examples = retrieve_examples(collection, cobol_code)
    print(examples)

    print(f"\n--- Claude's Response (G) ---")
    prompt = build_prompt(cobol_code, examples)
    java_code = generate_java(prompt)
    print(java_code)

# ---- Run it! ----
collection = setup_chromadb()

# Test with multiple COBOL snippets
convert_cobol_to_java(collection, "MULTIPLY WS-PRICE BY WS-QTY GIVING WS-TOTAL")
convert_cobol_to_java(collection, "IF WS-BALANCE < 0 MOVE 'OVERDRAWN' TO WS-STATUS END-IF")
convert_cobol_to_java(collection, "PERFORM VARYING I FROM 1 BY 1 UNTIL I > 5 DISPLAY I END-PERFORM")