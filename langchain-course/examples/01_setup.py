"""
Topic 1: Basic Setup and Installation

Quick example showing:
- Setting up LangChain 1.0
- Making your first LLM call
- Provider-agnostic design
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Alternative providers - just swap the import:
# from langchain_anthropic import ChatAnthropic
# from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: Set your OPENAI_API_KEY environment variable")
    exit(1)

# Initialize the LLM - all providers use same interface
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

print("Making first LLM call...\n")

# Simple invoke
response = llm.invoke("Explain LangChain in one sentence.")
print(f"Response: {response.content}\n")

# Response includes metadata
print(f"Tokens used: {response.response_metadata.get('token_usage', {}).get('total_tokens', 'N/A')}")

print("\n✓ Setup complete! Move to 02_lcel_basics.py")
