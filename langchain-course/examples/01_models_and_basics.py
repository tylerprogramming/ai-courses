"""
Example 1: Models and Basics

Learn how to:
- Initialize models using init_chat_model() (recommended pattern)
- Make basic invocations
- Stream responses for better UX
- Use batch processing

Based on: https://docs.langchain.com/oss/python/langchain/models
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: Set your OPENAI_API_KEY environment variable")
    exit(1)


# ============================================================================
# 1. Initialize Model with init_chat_model (Recommended)
# ============================================================================

# Provider-agnostic initialization - easiest way to get started
model = init_chat_model(
    "gpt-4o-mini",
    temperature=0.7,
    max_tokens=150,
)

# Alternative providers - just change the model name:
# model = init_chat_model("claude-sonnet-4-5-20250929")
# model = init_chat_model("google_genai:gemini-2-flash")


# ============================================================================
# 2. Basic Invocation
# ============================================================================

response = model.invoke("Explain LangChain in one sentence.")
print(f"Response: {response.content}")
print(f"Tokens: {response.response_metadata.get('token_usage', {})}\n")


# ============================================================================
# 3. Using Messages API
# ============================================================================

messages = [
    SystemMessage(content="You are a helpful Python tutor."),
    HumanMessage(content="What is a decorator in Python?")
]

response = model.invoke(messages)
print(f"Response: {response.content}\n")


# ============================================================================
# 4. Streaming Responses
# ============================================================================

for chunk in model.stream("Tell me a short joke about programming."):
    print(chunk.content, end="", flush=True)

print("\n")


# ============================================================================
# 5. Batch Processing
# ============================================================================

questions = [
    "What is Python?",
    "What is JavaScript?",
    "What is Go?"
]

responses = model.batch(questions)
for q, r in zip(questions, responses):
    print(f"Q: {q}")
    print(f"A: {r.content}\n")


# ============================================================================
# Key Takeaways
# ============================================================================

print("=" * 70)
print("KEY TAKEAWAYS:")
print("✓ init_chat_model() is the recommended way to initialize models")
print("✓ Provider-agnostic: switch providers by changing model name")
print("✓ invoke() for single requests")
print("✓ stream() for better UX on long responses")
print("✓ batch() for parallel processing")
