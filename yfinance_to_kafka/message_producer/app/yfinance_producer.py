import json

import pandas as pd
from kafka import KafkaProducer
import logging
import threading
from typing import Any
import yfinance as yf
import time


class YFinanceProducer:

    def __init__(self,
                 bootstrap_servers: str | list[str],
                 acks: int | str = "all",
                 value_serializer=(lambda v: json.dumps(v).encode('utf-8')),
                 **kwargs) -> None:
        """
        :param bootstrap_servers: Server of the Kafka cluster to connect to. Default: localhost:9092. :param acks:
        The number of acknowledgments the producer requires the leader to have received before considering a request
        complete. Default: all. :param value_serializer: Used to convert user-supplied message values to bytes.
        Defaults to a built-in function that converts json to bytes using utf-8. :param kwargs: Other arguments to
        pass to [KafkaProducer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html)
        """
        self.__producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                        acks=acks,
                                        value_serializer=value_serializer,
                                        **kwargs)
        logging.info(f"Connected to Kafka at {bootstrap_servers}")

    def __repr__(self) -> str:
        return 'yfinance_to_kafka.YFinanceProducer object'

    # TODO: start/end parameters are broken for the moment
    def send_batch_price(self,
                         kafka_topic: str,
                         tickers: str | list[str],
                         start: Any = None,
                         end: Any = None,
                         period: str | None = "5d",
                         interval: str | None = "1m",
                         prepost: bool = True,
                         keepna: bool = False) -> None:
        """
         Method to load previous trading session's data
         (Should run after 8pm Eastern Time / end of post-market session)

        :param tickers: Tickers to get data for
        :param start: Start date for historical data query
        :param end: End date for historical data query
        :param period: Period of query, default to 5 days (can be set to max in conjunction with start/end)
        :param interval: Resolution interval for data, smallest is 1 minute, but can only get the last 7 days
        :param prepost: Pre-/Post-market data
        :param keepna: Keep NA entries
        :return: A pandas dataframe of prices
        """
        threads = []
        for ticker in tickers:
            thread = threading.Thread(target=self._download_and_send_ticker_data,
                                      args=(kafka_topic, ticker, start, end, period, interval, prepost, keepna))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def _download_and_send_ticker_data(self,
                                       kafka_topic: str,
                                       ticker: str,
                                       start: Any,
                                       end: Any,
                                       period: str | None,
                                       interval: str | None,
                                       prepost: bool,
                                       keepna: bool) -> None:
        """
        Helper method to download ticker data and send it to Kafka.
        """
        # Retry up to 3 times
        for _ in range(3):
            try:
                # Download data from Yahoo Finance
                df = self._download_data(ticker=ticker,
                                         start=start,
                                         end=end,
                                         period=period,
                                         interval=interval,
                                         prepost=prepost,
                                         keepna=keepna)

                # Serialize the dataframe to JSON and send to Kafka
                for index, row in df.iterrows():
                    value = row.to_json(orient='records')
                    self.__producer.send(topic=kafka_topic, key=ticker.encode(), value=value)

                # Flush the Kafka producer to ensure all messages in batch are sent
                self.__producer.flush()
                logging.info(f"Sent {ticker} to Kafka topic {kafka_topic}")
                break
            except Exception as e:
                logging.error(f"Error downloading Ticker {ticker} from Yahoo Finance: {e}. Retry in 30 seconds.")
                time.sleep(30)
        if _ == 2:
            logging.error(f"Failed to download Ticker {ticker} from Yahoo Finance after {_ + 1} retries.")

    def _download_data(self,
                       ticker: str,
                       start: Any,
                       end: Any,
                       period: str | None,
                       interval: str | None,
                       prepost: bool,
                       keepna: bool) -> pd.DataFrame:
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
        # Add ticker column
        df.insert(1, "Ticker", [ticker] * len(df))
        logging.info(f"Downloaded {ticker} from Yahoo Finance")
        return df
