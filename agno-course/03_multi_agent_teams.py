"""
Agno Framework - Lesson 3: Multi-Agent Teams

This lesson covers:
- Creating specialized agents with different roles
- Using Team to coordinate multiple agents
- Real-world team patterns (research, creative, problem-solving)
"""

from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat

from dotenv import load_dotenv
import os

load_dotenv()

strategist = Agent(
    name="ContentStrategist",
    role="Creative Strategist",
    model=OpenAIChat(id="gpt-4.1"),
    instructions=[
        "You are a creative content strategist.",
        "Generate innovative, audience-focused ideas.",
        "Consider engagement, SEO, and brand alignment."
    ],
)

writer = Agent(
    name="ContentWriter",
    role="Content Creator",
    model=OpenAIChat(id="gpt-4.1"),
    instructions=[
        "You are a skilled content writer.",
        "Write engaging, clear, and compelling content.",
        "Follow the strategist's creative direction.",
        "Use appropriate tone and style for the audience."
    ],
)

editor = Agent(
    name="Editor",
    role="Senior Editor",
    model=OpenAIChat(id="gpt-4.1"),
    instructions=[
        "You are a senior editor.",
        "Review content for clarity, grammar, and impact.",
        "Enhance readability and flow.",
        "Ensure professional quality and consistency."
    ],
)

creative_team = Team(
    name="ContentCreationTeam",
    members=[strategist, writer, editor],
    instructions=[
        "Collaborate to create high-quality content.",
        "Strategist: Develop the creative approach and key messages.",
        "Writer: Create the content following the strategy.",
        "Editor: Polish and perfect the final piece.",
    ]
)

response = creative_team.run(
    "Create a LinkedIn post about AI agents in software development. "
    "Target audience: CTOs and engineering leaders."
)
print(f"[Creative Team Output]\n{response.content}\n")
