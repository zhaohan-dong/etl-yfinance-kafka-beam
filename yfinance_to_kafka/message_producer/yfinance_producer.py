import json
from kafka import KafkaProducer
import logging
import threading
from typing import Any
import yfinance as yf


class YFinanceProducer:

    def __init__(self,
                 bootstrap_servers: str | list[str] = "localhost:9092",
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
        if bootstrap_servers== "localhost:9092":
            logging.warning("Using default bootstrap server. This is not recommended for production.")

    def __repr__(self) -> str:
        return 'yfinance_to_kafka.YFinanceProducer object'

    # TODO: start/end parameters are broken for the moment
    def send_batch_price(self,
                         tickers: str | list[str],
                         start: Any = None,
                         end: Any = None,
                         period: str = "5d",
                         interval: str = "1m",
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
                                      args=(ticker, start, end, period, interval, prepost, keepna))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def _download_and_send_ticker_data(self,
                                       ticker: str,
                                       start: Any = None,
                                       end: Any = None,
                                       period: str = "5d",
                                       interval: str = "1m",
                                       prepost: bool = True,
                                       keepna: bool = False) -> None:
        """
        Helper method to download ticker data and send it to Kafka.
        """
        try:
            # Download data from Yahoo Finance
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
            df.insert(1, "Ticker", ticker)
            logging.info(f"Downloaded {ticker} from Yahoo Finance")

            # Serialize the dataframe to JSON and send to Kafka
            for index, row in df.iterrows():
                value = row.to_json(orient='records')
                self.__producer.send(topic="yfinance", key=ticker, value=value)

            # Flush the Kafka producer to ensure all messages in batch are sent
            self.__producer.flush()
            logging.info(f"Sent {ticker} to Kafka")
        except Exception as e:
            logging.error(f"Error downloading Ticker {ticker} from Yahoo Finance: {e}. Continuing...")
