import logging
from typing import Any

from kafka import KafkaProducer
import json
import yfinance as yf


class YFinanceProducer:

    def __init__(self,
                 bootstrap_servers: str | list[str] = "localhost:9092",
                 acks: int | str = "all",
                 value_serializer=(lambda v: json.dumps(v).encode('utf-8')),
                 **kwargs):
        """
        :param bootstrap_servers: Server of the Kafka cluster to connect to. Default: localhost:9092.
        :param acks: The number of acknowledgments the producer requires the leader to have received before considering a request complete. Default: all.
        :param value_serializer: Used to convert user-supplied message values to bytes. Defaults to a built-in function that converts json to bytes using utf-8.
        :param kwargs: Other arguments to pass to [KafkaProducer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html)
        """
        self.__producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                      acks=acks,
                                      value_serializer=value_serializer,
                                      **kwargs)

    def __repr__(self):
        return 'yfinance_to_kafka.YFinanceProducer object'

    # TODO: start/end parameters are broken for the moment
    def __get_historical_price(self,
                                    ticker: str,
                                    start: Any = None,
                                    end: Any = None,
                                    period: str = "5d",
                                    interval: str = "1m",
                                    prepost: bool = True,
                                    keepna: bool = False):
        """
         Method to load previous trading session's data
         (Should run after 8pm Eastern Time / end of post-market session)

        :param ticker: Ticker to get data for
        :param start: Start date for historical data query
        :param end: End date for historical data query
        :param period: Period of query, default to 5 days (can be set to max in conjunction with start/end)
        :param interval: Resolution interval for data, smallest is 1 minute, but can only get the last 7 days
        :param prepost: Pre-/Post-market data
        :param keepna: Keep NA entries
        :return: A pandas dataframe of prices
        """
        df = yf.download(tickers=ticker,
                               start=start,
                               end=end,
                               period=period,
                               interval=interval,
                               prepost=prepost,
                               actions=True,
                               progress=False,
                               group_by="ticker",
                               keepna=keepna).reset_index()
        df.insert(1, "Ticker", ticker)
        try:
            return df.to_json(orient='records')
        except Exception as e:
            logging.error(f"Error downloading from Yahoo Finance: {e}")
            return None

    def send_msg(self, topic: str, tickers: str | list[str],
                   start: Any = None,
                   end: Any = None,
                   period: str = "5d",
                   interval: str = "1m",
                   prepost: bool = True,
                   keepna: bool = False):
        """
        Send ticker messages to a Kafka topic.
        :param topic: Topic to send message to.
        :param value: Message to send.
        :param start: Start date for historical data query
        :param end: End date for historical data query
        :param period: Period of query, default to 5 days (can be set to max in conjunction with start/end)
        :param interval: Resolution interval for data, smallest is 1 minute, but can only get the last 7 days
        :param prepost: Pre-/Post-market data
        :param keepna: Keep NA entries
        :return: None
        """
        for ticker in tickers:
            self.__producer.send(topic=topic, value=self.__get_historical_price(ticker=ticker,
                                                                                   start=start,
                                                                                   end=end,
                                                                                   period=period,
                                                                                   interval=interval,
                                                                                   prepost=prepost,
                                                                                   keepna=keepna))
        self.__producer.flush()