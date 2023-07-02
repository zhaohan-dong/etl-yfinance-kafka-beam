import yfinance as yf

def parse_ticker_to_str_list(tickers: yf.Ticker | yf.Tickers | str | list[str]) -> list[str] | None:
    if isinstance(tickers, yf.Ticker):
        return [tickers.ticker]
    elif isinstance(tickers, yf.Tickers):
        return tickers.tickers
    elif isinstance(tickers, str):
        return [tickers]
    elif isinstance(tickers, list):
        return tickers
    else:
        raise TypeError("Wrong ticker type")
