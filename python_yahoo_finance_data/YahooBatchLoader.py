# Wrapper class to download data from Yahoo Finance using yfinance package
from typing import Any
import pytz
import yfinance
import yfinance as yf
import pandas as pd
import datetime
from . import utils
from . import quote


class YahooBatchLoader:
    def __repr__(self):
        return 'yahoo_finance_data.YahooBatchLoader object'

    def get_historical_prices(self, tickers: yf.Ticker | yf.Tickers | str | list[str],
                   start: Any = None,
                   end: Any = None,
                   period: str = "5d",
                   interval: str = "1m",
                   prepost: bool = True,
                   keepna: bool = False) -> pd.DataFrame:
        """
         Method to load previous trading session's data
         (Should run after 8pm Eastern Time / end of post-market session)

         Note: start/end parameters are broken for the moment
        :param start: Start date for historical data query
        :param end: End date for historical data query
        :param period: Period of query, default to 5 days (can be set to max in conjunction with start/end)
        :param interval: Resolution interval for data, smallest is 1 minute, but can only get the last 7 days
        :param prepost: Pre-/Post-market data
        :param keepna: Keep NA entries
        :return: A pandas dataframe of prices
        """
        tkrs = utils.parse_ticker_to_str_list(tickers)

        # Download ticker data from yahoo
        df = yf.download(tickers=tkrs,
                         start=start,
                         end=end,
                         period=period,
                         interval=interval,
                         prepost=prepost,
                         actions=True,
                         progress=False,
                         group_by="ticker",
                         keepna=keepna)

        df = utils.rename_index_datetime(df)

        df = utils.pivot_price_df_by_ticker(df, tkrs)

        df = utils.market_open_close(df, exchangeTimeZoneName="America/New_York")

        return df

    def get_prices(self, tickers: yf.Ticker | yf.Tickers | str | list[str]) -> pd.DataFrame:

        tkrs = utils.parse_ticker_to_str_list(tickers)
        tickers_df = pd.DataFrame()

        for ticker in tkrs:
            ticker_df = pd.DataFrame([quote.get_quote(ticker)])
            tickers_df = pd.concat([tickers_df, ticker_df])

        return tickers_df

    # Get options data for all available future dates at the moment
    def options_data(self, tickers: yf.Ticker | yf.Tickers | str | list[str]) -> pd.DataFrame:

        tkrs = utils.parse_ticker_to_str_list(tickers)

        options_df = pd.DataFrame()  # create an empty DataFrame to store options data

        for ticker in tkrs:

            ticker_options_df = pd.DataFrame()

            # Get a list of expiration dates
            expiration_dates = yf.Ticker(ticker).options

            # yfinance does not provide a way to get all expiration date options price, so we have to query one by one
            for expiration_date in expiration_dates:
                option_chain = yf.Ticker(ticker).option_chain(
                    date=expiration_date)  # get the option chain for the ticker
                call_options = option_chain.calls  # get call options data
                put_options = option_chain.puts  # get put options data
                ticker_options_df = pd.concat(
                    [ticker_options_df, call_options, put_options])  # concatenate call and put options data
                ticker_options_df["accessTime"] = datetime.datetime.now(tz=pytz.UTC)
                ticker_options_df["ticker"] = ticker

            options_df = pd.concat([options_df, ticker_options_df])

        return options_df

