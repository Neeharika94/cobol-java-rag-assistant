import chromadb

# Step 1 - Create a ChromaDB client - A client is your connection to the database system.
client = chromadb.Client()

# Step 2 - Create a collection (like a table in SQL)
collection = client.create_collection(name="cobol_examples")

# Step 3 - Store your 5 COBOL->Java examples
# inserts records into the vector database
# documents are main text entries
# hidden step - When you add documents, ChromaDB automatically converts text into vectors (embeddings).
collection.add(
    documents=[
        "MOVE A TO B",
        "DISPLAY 'HELLO'",
        "ACCEPT WS-DATE FROM DATE",
        "ADD A TO B",
        "PERFORM UNTIL WS-COUNT > 10"
    ],
    metadatas=[ # additional information attached to documents
        {"java": "b = a;"},
        {"java": "System.out.println('HELLO');"},
        {"java": "LocalDate.now();"},
        {"java": "b = a + b;"},
        {"java": "while(wsCount <= 10) { }"}
    ],
    ids=["ex1", "ex2", "ex3", "ex4", "ex5"] # unique identifiers for each record like primary keys in sql
)

# Step 4 - Query with a new COBOL snippet
# n_results = 2 mean - Return the 2 most similar examples
results = collection.query(
    query_texts=["MOVE X TO Y"],
    n_results=2
)

# Step 5 - Print results
print("Most similar examples found:")
for i, doc in enumerate(results['documents'][0]):
    java = results['metadatas'][0][i]['java']
    print(f"\nCOBOL: {doc}")
    print(f"Java:  {java}")