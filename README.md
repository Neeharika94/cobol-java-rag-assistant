# COBOL to Java RAG Assistant 🤖

An AI-powered tool that converts COBOL code to Java using 
Retrieval Augmented Generation (RAG). Built by a 7-year 
enterprise migration engineer to solve a real production problem.

## Live Demo
🔗 Coming soon (AWS deployment in progress)

## What it does
- Takes COBOL code as input via REST API
- Retrieves semantically similar migration examples 
  from a vector database
- Uses Claude AI to generate accurate Java equivalents
- Returns Java code + similar examples + explanation

## Tech Stack
| Layer | Technology |
|---|---|
| LLM | Claude (Anthropic) |
| Vector Database | ChromaDB |
| API Framework | FastAPI |
| Language | Python |
| Cloud | AWS (coming soon) |

## Architecture
User sends COBOL code
↓
FastAPI receives POST /convert request
↓
ChromaDB retrieves 3 similar examples (Retrieval)
↓
LangChain builds enriched prompt (Augmented)
↓
Claude generates Java code (Generation)
↓
API returns Java code + similar examples
## How RAG improves output quality
Without RAG — Claude guesses based on general knowledge.
With RAG — Claude sees YOUR specific migration patterns 
as context, producing accurate enterprise-grade output.

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Welcome message |
| GET | /health | Health check |
| POST | /convert | Convert COBOL to Java |
| GET | /docs | Interactive Swagger UI |

## Example
### Request
```json
POST /convert
{
  "cobol_code": "MOVE WS-NAME TO WS-OUTPUT"
}
```

### Response
```json
{
  "cobol_code": "MOVE WS-NAME TO WS-OUTPUT",
  "java_code": "wsOutput = wsName;",
  "similar_examples": [
    {
      "cobol": "MOVE WS-FIRST-NAME TO WS-OUTPUT-NAME",
      "java": "wsOutputName = wsFirstName;",
      "explanation": "Copy string variable to another"
    }
  ]
}
```

## Setup & Run Locally
```bash
# Clone the repo
git clone https://github.com/Neeharika94/cobol-java-rag-assistant
cd cobol-java-rag-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install langchain anthropic chromadb fastapi uvicorn openai python-dotenv pydantic

# Add your API key
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Run the server
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` to test the API.

## Project Structure
cobol-java-rag-assistant/
├── main.py                 # FastAPI app + endpoints
├── rag_pipeline.py         # Core RAG pipeline
├── cobol_examples.json     # 40 COBOL→Java examples
├── chromadb_test.py        # ChromaDB retrieval test
├── test_claude.py          # Basic Claude API test
└── .env                    # API keys (not committed)

## Example Conversions
| COBOL | Java |
|---|---|
| `MOVE A TO B` | `b = a;` |
| `ADD A TO B` | `b = b + a;` |
| `PERFORM UNTIL WS-COUNT > 10` | `while (wsCount <= 10) {}` |
| `DISPLAY 'HELLO'` | `System.out.println("HELLO");` |
| `IF WS-AGE > 18 MOVE 'ADULT' TO WS-STATUS END-IF` | `if (wsAge > 18) { wsStatus = "ADULT"; }` |

## About
Built by Neeharika Cheruku — 8 years of enterprise full 
stack software development and mainframe migration 
experience at AWS. This tool automates the most 
repetitive part of mainframe modernization using RAG and 
Claude AI.
