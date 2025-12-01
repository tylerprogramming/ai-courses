from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv

load_dotenv()

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)


async def main():
    result = await Runner.run(triage_agent, input="Hello, how are you?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())