import pandas as pd
def rename_index_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    The returned index is named "Datetime" when period is shorter than 1d, but "Date" when longer
    We'll format it to "Datetime"
    :return: Pandas dataframe
    """
    if df.index.name == "Date":
        df.index.rename("Datetime", inplace=True)
    return df


def pivot_price_df_by_ticker(df: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    """
    The downloaded data is in a dataframe with two levels of column labels
    One level is the tickers, and the other is Open, Close, etc.
    We'll flatten it here
    :param df: Price dataframe downloaded from yfinance, with two levels of columns
    :return: Pandas dataframe without index
    """
    # Pivot only if the number of column levels is greater than one (passing one ticker gives only one level)
    if df.columns.nlevels > 1:
        df = df.rename_axis(columns=('Ticker', None)).stack(0).reset_index().explode('Datetime')
    else:
        df = df.reset_index()
        df.insert(loc=1, column="Ticker", value=tickers[0])
    return df