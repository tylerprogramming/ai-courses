"""
Agno Framework - Lesson 1: Basic Agent Fundamentals

This lesson covers:
- Creating a minimal agent
- Configuring agents with instructions
- Multi-turn conversations with memory
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os

load_dotenv()

assistant = Agent(
    name="PythonTutor",
    model=OpenAIChat(id="gpt-4o-mini"),
    description="A helpful Python programming tutor",
    instructions=[
        "You are an expert Python tutor.",
        "Explain concepts clearly with practical examples.",
        "Be encouraging and patient.",
        "Always provide code examples when relevant."
    ],
    markdown=True,
)

while True:
    question = input("What would you like to learn about Python? (or 'exit' to quit): ")
    if question.lower() == "exit":
        break
    else:
        response = assistant.run(question)
        print(f"[Python Tutor]\n{response.content}\n")