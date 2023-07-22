import logging
import os
from yfinance_producer import YFinanceProducer

def main() -> int:
    with open("./tickers.txt") as f:
        tickers = f.read().splitlines()
    if tickers == []:
        logging.warning("No tickers found in tickers.txt. Exiting...")
        return 1
    yfinance_producer = YFinanceProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    #yfinance_producer.send_batch_price(tickers=tickers, period="5d", interval="1m")
    return 0

if __name__ == "__main__":
    main()
