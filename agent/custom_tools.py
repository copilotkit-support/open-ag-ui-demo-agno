from agno.tools import tool
import yfinance as yf
from datetime import datetime

from pydantic import BaseModel, RootModel
from typing import Dict
from datetime import date


class PriceData(RootModel[Dict[date, float]]):
    pass


class SymbolData(BaseModel):
    Price: PriceData


class StockMarketData(RootModel[Dict[str, SymbolData]]):
    pass

@tool(
  name="change_background_colour",
  description="This tool is used to change the background colour of the canvas.",
  show_result= True
)
def change_background_colour(colour: str):
  """
  This tool is used to change the background colour of the canvas.
  """
  return colour


@tool(
    name = "extract_relevant_data_from_user_input",
    description = "This tool is used to extract relevant data from the user's input.",
    show_result = True
)
def extract_relevant_data_from_user_input(tickers: list[str], amount: list[int], investment_date : list[str]):
  """
  This tool is used to extract relevant data from the user's input.
  """
  return {"tickers" : tickers, "amount" : amount, "investment_date" : investment_date}

# def gather_stock_data(tickers: list[str], investment_dates: list[str]):
#   """
#   This tool is used to gather stock data from the user's input.
#   """
#   stock_data = {}
#   for ticker, investment_date in zip(tickers, investment_dates):
#     stock_data[ticker] = yf.download(ticker, interval="3mo", start=investment_date, end=datetime.now().strftime("%Y-%m-%d"))
  
#   return stock_data

# def calculate_investment_value(stock_data: StockMarketData, amount: list[int], investment_dates: list[str]):
#   """
#   This tool is used to calculate the investment value of the user's input. It should take the stock data that is returned from the gather_stock_data tool and calculate the investment value of the user's input.
#   """
#   print(investment_dates)
#   investment_value = {}
#   for ticker, data in stock_data.items():
#     investment_value[ticker] = data.Price.iloc[-1] * amount
#   return investment_value

@tool(
  name="calculate_investment_return_multi",
  description="Calculates the return of investments made in multiple stocks, each with a single investment date and amount.",
  show_result=True
)
def calculate_investment_return_multi(
    tickers: list[str],
    investment_dates: list[str],
    investment_amounts: list[float]
):
    """
    Calculates the return of investments made in multiple stocks, each with a single investment date and amount.
    Args:
        tickers: List of stock ticker symbols (e.g., ['AAPL', 'GOOG'])
        investment_dates: List of dates (YYYY-MM-DD), one per ticker
        investment_amounts: List of amounts invested at each date, one per ticker
    Returns:
        A summary for each ticker: total invested, current value, and return.
    """
    if not (len(tickers) == len(investment_dates) == len(investment_amounts)):
        return "tickers, investment_dates, and investment_amounts must be the same length."
    
    results = {}
    for ticker, date, amount in zip(tickers, investment_dates, investment_amounts):
        data = yf.download(ticker, start=date, end=datetime.today().strftime('%Y-%m-%d'))
        if data.empty:
            results[ticker] = f"No data found for {ticker}."
            continue
        price_row = data.loc[data.index >= date]
        if price_row.empty:
            results[ticker] = f"No price data for {ticker} on or after {date}."
            continue
        buy_price = price_row.iloc[0]['Close']
        shares = amount / buy_price
        current_price = data.iloc[-1]['Close']
        current_value = shares * current_price
        total_return = current_value - amount
        return_pct = (total_return / amount) * 100 if amount != 0 else 0
        results[ticker] = {
            "investment_date": date,
            "amount_invested": amount,
            "buy_price": buy_price,
            "shares": shares,
            "current_price": current_price,
            "current_value": current_value,
            "total_return": total_return,
            "return_pct": return_pct
        }
    return results