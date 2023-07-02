import datetime
import pytz
import pandas as pd

def get_exchange_tz(timezone: str) -> datetime.tzinfo:
    """
    Get timezone given exchange's country
    :param market: Country of the Exchange
    :return:
    """

    if timezone != "UTC":
        return pytz.timezone(timezone)
    else:
        return pytz.timezone("UTC")


def df_to_exchange_tz(df: pd.DataFrame, exchangeTimeZoneName: str) -> pd.DataFrame:
    # Get Exchange timezone
    exchange_tz = get_exchange_tz(exchangeTimeZoneName)

    # If dataframe is timezone naive
    if df["Datetime"].dt.tz is None:
        df["Datetime"] = df["Datetime"].dt.tz_localize(exchange_tz)

    # If dataframe is timezone aware
    elif df["Datetime"].dt.tz != get_exchange_tz(exchangeTimeZoneName):
        df["Datetime"] = df["Datetime"].dt.tz_convert(exchange_tz)

    return df


def market_open_close(df: pd.DataFrame, exchangeTimeZoneName: str) -> pd.DataFrame:
    if exchangeTimeZoneName == "America/New_York":
        # Change dataframe's timezone to market's
        df = df_to_exchange_tz(df, exchangeTimeZoneName)
        df["Market"] = df["Datetime"].apply(lambda x: "Closed" if x.time() < datetime.time(hour=9, minute=30) or
                                                                  x.time() > datetime.time(hour=16) else "Open")
    else:
        print("Market open/close status not supported yet.")
        df["Market"] = None
        return df
    return df