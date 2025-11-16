# pip install agents-arcade arcadepy

from arcadepy import AsyncArcade
from agents_arcade import get_arcade_tools
from agents_arcade.errors import AuthorizationError
from agents import Agent, Runner

from dotenv import load_dotenv
import os

load_dotenv()

USER_ID = "tylerreedytlearning@gmail.com"

async def main():
    client = AsyncArcade()
    tools = await get_arcade_tools(client, toolkits=["gmail"])
 
    google_agent = Agent(
        name="Google agent",
        instructions="You are a helpful assistant that can assist with Google API calls.",
        model="gpt-4.1",
        tools=tools,
    )
 
    try:
        result = await Runner.run(
            starting_agent=google_agent,
            input="What are my latest 10 emails?  Summarize them and then send an email to tylerreedytlearning@gmail.com with the subject 'Latest Emails' and the body 'Here are the latest emails: ' + the summary of the emails.  Create a Subject as well.",
            context={"user_id": USER_ID},
        )
        print("Final output:\n\n", result.final_output)
    except AuthorizationError as e:
        print("Please Login to Google:", e)
 
 
if __name__ == "__main__":
    import asyncio
 
    asyncio.run(main())