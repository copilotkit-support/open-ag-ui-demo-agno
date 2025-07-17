"""Example: Agno Agent with Finance tools

This example shows how to create an Agno Agent with tools (YFinanceTools) and expose it in an AG-UI compatible way.
"""

from agno.agent.agent import Agent
from agno.app.agui.app import AGUIApp
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
from custom_tools import (
    change_background_colour,
    extract_relevant_data_from_user_input,
    calculate_investment_return_multi,
)
from prompts import instructions

load_dotenv()


agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        # YFinanceTools(
        #   stock_price=True, analyst_recommendations=True, stock_fundamentals=True
        # ),
        change_background_colour,
        extract_relevant_data_from_user_input,
        calculate_investment_return_multi,
    ],
    debug_mode=True,
    description="You are an investment analyst that will analyse the user's input and provide a calculation of the user's investment made over a period of time.",
    instructions=instructions,
)

agui_app = AGUIApp(
    agent=agent,
    name="agno_agent",
    app_id="agno_agent",
    description="An investment analyst that will analyse the user's input and provide a calculation of the user's investment made over a period of time.",
)

app = agui_app.get_app()

if __name__ == "__main__":
    agui_app.serve(app="main:app", port=8000, reload=True)
