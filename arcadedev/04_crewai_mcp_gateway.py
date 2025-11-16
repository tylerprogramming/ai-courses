# you need the proper headers for this to work

mcp_url = "https://api.arcade.dev/mcp/tylerai-gmail"

from crewai import Agent, Task, Crew, LLM
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE
from crewai.mcp.filters import create_static_tool_filter

from dotenv import load_dotenv
import os

load_dotenv()

agent = Agent(
    role="Gmail Agent",
    goal="Help the user with their requests",
    backstory="You are a helpful assistant that can assist with Gmail API calls.",
    mcps=[
        # HTTP/Streamable HTTP transport for remote servers
        MCPServerHTTP(
            url=mcp_url,
            headers={
                "Authorization": f"Bearer {os.getenv('ARCADE_API_KEY')}",
                "Arcade-User-ID": "tylerreedytlearning@gmail.com"
            },
            streamable=True,
            cache_tools_list=True,
        )
    ],
    llm=LLM(model="gpt-4.1"),
    verbose=True
)

# Create task
research_task = Task(
    description="Get the 5 most recent emails from the user's inbox and summarize them then send an email of them summarized with subject to tylerreedytlearning@gmail.com",
    expected_output="An email sent to tylerreedytlearning@gmail.com with the subject 'Latest Emails' and the body 'Here are the latest emails: ' + the summary of the emails.  Create a Subject as well.",
    agent=agent
)

# Create and run crew
crew = Crew(agents=[agent], tasks=[research_task])
result = crew.kickoff()
print(result)