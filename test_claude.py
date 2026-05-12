import anthropic # anthropics python package - has prebuilt tools -how to connect to clause, send req, recieve responses etc
from dotenv import load_dotenv
import os
load_dotenv()
# this creates a connection object called client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# this called anthropic api's create messages function. the o/p of which is stored in message
# role - who is speaking - user - human, assistant - AI, system - instructoins/context
# content: actual text
# messages is a python list - The messages format exists because modern AI models work like conversations, where each message needs speaker, and actual text
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Convert this COBOL code to Java: MOVE WS-NAME TO WS-OUTPUT"}
    ]
)

print(message.content[0].text)