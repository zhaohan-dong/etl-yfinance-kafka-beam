import logging
import os
from yfinance_producer import YFinanceProducer


def main() -> int:
    # Read tickers
    with open("./tickers.txt") as f:
        tickers = f.read().splitlines()
    if not tickers:
        logging.warning("No tickers found in tickers.txt. Exiting...")
        return 1

    # Download and send data to Kafka
    yfinance_producer = YFinanceProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    yfinance_producer.send_batch_price(kafka_topic=os.getenv("KAFKA_TOPIC"), tickers=tickers, period="5d",
                                       interval="1m")
    return 0


if __name__ == "__main__":
    main()
