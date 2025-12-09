"""
Agno Framework - Lesson 2: Agents with Tools

This lesson covers:
- Using built-in toolkits (DuckDuckGo, YFinance)
- Creating custom Python functions as tools
- Combining multiple tools in a single agent
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Example 2: Custom Tools
def calculate_roi(initial_investment: float, final_value: float) -> dict:
    """
    Calculate Return on Investment (ROI).
    
    Args:
        initial_investment: Initial amount invested
        final_value: Final value of investment
    
    Returns:
        Dictionary with ROI percentage and profit/loss
    """
    profit = final_value - initial_investment
    roi_percentage = (profit / initial_investment) * 100
    
    return {
        "roi_percentage": round(roi_percentage, 2),
        "profit_loss": round(profit, 2),
        "initial": initial_investment,
        "final": final_value
    }

def get_current_datetime() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Example 2: Multi-Tool Agent
multi_tool_agent = Agent(
    name="InvestmentResearcher",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[
        DuckDuckGoTools(),
        YFinanceTools(),
        calculate_roi,
    ],
    instructions=[
        "You are an investment research assistant.",
        "Combine web research and financial data for comprehensive analysis.",
        "Use ROI calculations when relevant."
    ],
    debug_mode=True,
    markdown=True,
)

response = multi_tool_agent.run(
    "Research NVDA stock. What's the current price and recent news?"
)
print(f"[Multi-Tool Agent]\n{response.content}\n")
