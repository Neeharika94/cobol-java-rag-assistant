import chromadb
import anthropic
from dotenv import load_dotenv
import os
load_dotenv()

# ---- STEP 1: Setup ChromaDB ----
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="cobol_examples")

# ---- STEP 2: Store your COBOL->Java examples ----
collection.add(
    documents=[
        "MOVE A TO B",
        "DISPLAY 'HELLO'",
        "ACCEPT WS-DATE FROM DATE",
        "ADD A TO B",
        "PERFORM UNTIL WS-COUNT > 10"
    ],
    metadatas=[
        {"java": "b = a;"},
        {"java": "System.out.println('HELLO');"},
        {"java": "LocalDate.now();"},
        {"java": "b = a + b;"},
        {"java": "while(wsCount <= 10) { }"}
    ],
    ids=["ex1", "ex2", "ex3", "ex4", "ex5"]
)

# ---- STEP 3: Retrieve similar examples (R of RAG) ----
def retrieve_examples(cobol_code):
    results = collection.query(
        query_texts=[cobol_code],
        n_results=2
    )
    examples = []
    for i, doc in enumerate(results['documents'][0]):
        java = results['metadatas'][0][i]['java']
        examples.append(f"COBOL: {doc}\nJava: {java}")
    return "\n\n".join(examples)

# ---- STEP 4: Build prompt with examples (A of RAG) ----
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
def convert_cobol_to_java(cobol_code):
    print(f"\n--- Input COBOL ---")
    print(cobol_code)
    
    print(f"\n--- Retrieved Examples (R) ---")
    examples = retrieve_examples(cobol_code)
    print(examples)
    
    print(f"\n--- Building Prompt (A) ---")
    prompt = build_prompt(cobol_code, examples)
    print(prompt)
    
    print(f"\n--- Claude's Response (G) ---")
    java_code = generate_java(prompt)
    print(java_code)

# ---- Run it! ----
convert_cobol_to_java("ADD X TO Y")