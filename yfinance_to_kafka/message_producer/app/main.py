import logging
import os
from yfinance_producer import YFinanceProducer
import json
from kafka import KafkaConsumer

def main() -> int:
    with open("./tickers.txt") as f:
        tickers = f.read().splitlines()
    if tickers == []:
        logging.warning("No tickers found in tickers.txt. Exiting...")
        return 1
    yfinance_producer = YFinanceProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    yfinance_producer.send_batch_price(tickers=tickers, period="5d", interval="1m")
    group_id = "my-group"
    consumer = KafkaConsumer(
        'yfinance',
        bootstrap_servers='kafka:29092',
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
