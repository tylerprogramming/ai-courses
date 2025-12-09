"""
Agno Framework - Lesson 6: AgentOS Deployment

Deploy agents as production web services with AgentOS.

To run: python 06_agentos_fastapi.py
Then visit: http://localhost:7777/docs
"""

from agno.agent import Agent
from agno.team import Team
from agno.os import AgentOS
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Example 1: Simple Agent
# =============================================================================

simple_agent = Agent(
    name="SimpleAssistant",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=["You are a helpful AI assistant."],
    add_history_to_context=True,
    markdown=True,
)

simple_os = AgentOS(
    name="SimpleAssistantOS",
    agents=[simple_agent],
    description="A simple AI assistant"
)


# =============================================================================
# Example 2: Research Agent with Tools
# =============================================================================

research_agent = Agent(
    name="ResearchAssistant",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools(), YFinanceTools()],
    db=SqliteDb(session_table="sessions", db_file="research.db"),
    instructions=[
        "You are a research assistant.",
        "Use web search and financial tools to provide comprehensive answers."
    ],
    add_history_to_context=True,
    num_history_runs=10,
    debug_mode=True,  # Shows tool calls in logs
    markdown=True,
)

research_os = AgentOS(
    name="ResearchAssistantOS",
    agents=[research_agent],
    description="Research assistant with web search and financial data"
)


# =============================================================================
# Example 3: Research Team
# =============================================================================

web_researcher = Agent(
    name="WebResearcher",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions=["Search for current information on the web."],
)

financial_analyst = Agent(
    name="FinancialAnalyst",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[YFinanceTools()],
    instructions=["Analyze financial data and stock metrics."],
)

research_team = Team(
    name="ResearchTeam",
    members=[web_researcher, financial_analyst],
    db=SqliteDb(session_table="team_sessions", db_file="team.db"),
    instructions=["Work together to provide comprehensive research."],
    add_history_to_context=True,
)

team_os = AgentOS(
    name="ResearchTeamOS",
    teams=[research_team],
    description="Collaborative research team"
)


# =============================================================================
# Serve the Application
# =============================================================================

# Choose which service to run (uncomment one):
# app = simple_os.get_app()
# app = research_os.get_app()
app = team_os.get_app()


if __name__ == "__main__":
    # Start the server on port 7777
    team_os.serve(
        app="05_agentos_fastapi:app",
        host="0.0.0.0",
        port=7777,
        reload=True
    )
