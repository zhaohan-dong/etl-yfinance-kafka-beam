import logging
import os
from yfinance_producer import YFinanceProducer
import json
from kafka import KafkaConsumer

def main() -> int:
    # Read tickers
    with open("./tickers.txt") as f:
        tickers = f.read().splitlines()
    if tickers == []:
        logging.warning("No tickers found in tickers.txt. Exiting...")
        return 1

    # Download and send data to Kafka
    yfinance_producer = YFinanceProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    yfinance_producer.send_batch_price(kafka_topic="test", tickers=tickers, period="5d", interval="1m")
    # TODO: Test consumer, delete later with tests completed
    group_id = "test-group"
    consumer = KafkaConsumer(
        'test',
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        group_id=group_id,
        auto_offset_reset='earliest'  # Set the desired offset reset behavior
    )
    # Consume messages from the topic
    for message in consumer:
        value = json.loads(message.value.decode("utf-8"))  # Decode the value using JSON decoding
        print(value)
    return 0

if __name__ == "__main__":
    main()
