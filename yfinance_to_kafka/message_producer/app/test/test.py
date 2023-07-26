import json
import unittest
from yfinance_producer import YFinanceProducer
import yfinance as yf
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = "localhost:9092"

# TODO: Fix NoBrokersAvailable error when building docker image
class TestYFinanceProducer(unittest.TestCase):
    def test_initialize_class(self):
        self.assertIsInstance(YFinanceProducer(bootstrap_servers=BOOTSTRAP_SERVERS), YFinanceProducer,
                              "Failed to initialize YFinanceProducer class object")

    def test_yfinance_download(self):
        data = yf.download(tickers="AAPL", start='2022-01-03', end='2022-01-04', interval="1d", period=None,
                           prepost=True, keepna=False, progress=False)
        self.assertEqual(data.shape, (1, 6), "Yahoo Finance download shape error")
        self.assertEqual(data.iloc[0]["Open"], 177.830002, "Yahoo Finance download data error")

    def test_yfinance_kafka_producer(self):
        yf_producer = YFinanceProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        yf_producer._download_and_send_ticker_data(kafka_topic="test",
                                                   ticker="AAPL", start='2022-01-03', end='2022-01-04', interval="1d",
                                                   period=None, prepost=True, keepna=False)
        group_id = "test-group"
        kafka_consumer = KafkaConsumer(
            topics="test",
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=group_id,
            auto_offset_reset='earliest'  # Set the desired offset reset behavior
        )
        last_value = None  # Initialize a variable to hold the last value

        # Consume messages from the topic
        for message in kafka_consumer:
            last_value = json.loads(message.value.decode("utf-8"))

        self.assertEqual(last_value["Open"], 177.830002, "Yahoo Finance kafka download data error")
        self.assertEqual(last_value["Ticker"], "AAPL", "Yahoo Finance kafka parse ticker error")

    def test_yfinance_kafka_producer_threading(self):
        yf_producer = YFinanceProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        yf_producer.send_batch_price(kafka_topic="test",
                                     tickers=["AAPL", "GOOGL"],
                                     start='2022-01-03', end='2022-01-04', interval="1d", period=None, prepost=True,
                                     keepna=False)

        group_id = "test-group"
        kafka_consumer = KafkaConsumer(
            topics="test",
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=group_id,
            auto_offset_reset='earliest'  # Set the desired offset reset behavior
        )

        tickers_received = set()  # A set to hold the tickers of all received messages
        for message in kafka_consumer:
            value = json.loads(message.value.decode("utf-8"))
            tickers_received.add(value["Ticker"])

        # Assert that we have received messages for both tickers
        self.assertSetEqual(tickers_received, {"AAPL", "GOOGL"}, "Not all tickers received in Kafka topic")


if __name__ == '__main__':
    unittest.main()
