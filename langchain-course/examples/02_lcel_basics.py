"""
Topic 2: LCEL (LangChain Expression Language) Basics

LCEL is the MODERN way to build chains (replaces legacy LLMChain).
Uses the pipe operator (|) to chain components together.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ============================================================================
# Example 1: Basic LCEL Chain (prompt | model | parser)
# ============================================================================

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that explains concepts clearly."),
    ("human", "{question}")
])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
output_parser = StrOutputParser()

# Chain them together with the pipe operator - this is LCEL!
chain = prompt | model | output_parser

print("Example 1: Basic Chain")
print("-" * 60)
response = chain.invoke({"question": "What is machine learning?"})
print(response)

# ============================================================================
# Example 2: Streaming (built-in with LCEL)
# ============================================================================

print("\n\nExample 2: Streaming")
print("-" * 60)
print("Streaming response: ", end="", flush=True)

for chunk in chain.stream({"request": "Tell me a one-sentence joke about AI."}):
    print(chunk, end="", flush=True)

print("\n\n✓ LCEL chains are: clean, composable, and support streaming!")
print("✓ Next: 03_tool_calling.py")
