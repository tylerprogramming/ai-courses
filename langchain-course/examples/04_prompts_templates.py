"""
Topic 4: Prompts and Prompt Templates

Prompt templates make it easy to construct dynamic prompts with variables,
system messages, and few-shot examples.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# ============================================================================
# Example 1: ChatPromptTemplate (Recommended)
# ============================================================================

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}. You always respond in a {style} manner."),
    ("human", "{user_input}")
])

chain = prompt | model | StrOutputParser()

print("Example 1: Dynamic Prompts")
print("-" * 60)

response = chain.invoke({
    "role": "pirate translator",
    "style": "pirate-like",
    "user_input": "Hello, how are you?"
})
print(response)

# ============================================================================
# Example 2: Few-Shot Prompting (Teaching by example)
# ============================================================================

examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "hot", "output": "cold"}
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert at finding antonyms."),
    few_shot_prompt,
    ("human", "{input}")
])

chain = final_prompt | model | StrOutputParser()

print("\n\nExample 2: Few-Shot Learning")
print("-" * 60)

test_words = ["fast", "bright", "loud"]
for word in test_words:
    result = chain.invoke({"input": word})
    print(f"{word} → {result}")

print("\n✓ Use ChatPromptTemplate for structured prompts")
print("✓ Few-shot learning teaches by example")
print("✓ Next: 05_agents.py")
