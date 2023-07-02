import yfinance as yf
import datetime


def get_quote(ticker: str) -> dict:
    """
    Given a ticker, return last quote
    :param ticker: Ticker
    :return: Regular market price, post market bid price, ask price, bid size, ask size, quote access datetime
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    return {"ticker": ticker,
            "bid": info["bid"],
            "ask": info["ask"],
            "bidSize": info["bidSize"],
            "askSizes": info["askSize"],
            "accessTime": datetime.datetime.now(tz=datetime.timezone.utc)}
