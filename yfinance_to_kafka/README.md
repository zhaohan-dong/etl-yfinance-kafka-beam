# Ingest YFinance data into Apache Kafka Topic

## Diagram
![yfinance-kafka](https://github.com/zhaohan-dong/etl-yfinance-kafka-beam/assets/65422392/938b50cf-6e00-411a-905e-8a968a2faf85)

## Setting up Kafka locally via docker-compose
Go to `./kafka_docker` directory and run the following command.
```bash
docker-compose up -d
```

## Message Producer
The message producer is a Python script that uses the `yfinance` library to fetch stock data from Yahoo Finance and sends the data to a Kafka topic. The script is located at `yfinance_to_kafka/message_producer/app/yfinance_producer.py`.<br />
Add `tickers.txt` file in this directory to pass the tickers into the producer script. The tickers are read from this file and sent to the Kafka topic.
The docker compose config will bind the container to the same docker network as Kafka and Zookeeper container. Modify the environment variables as needed.
On first run:
```bash
docker-compose build
```
Then:
```bash
docker-compose up
```

## Installing Kafka on Kubernetes (On backlog)
### Install kubectl Helm on Mac (Homebrew)
```bash
brew install helm kubernetes-cli
```
Install Kafka using Helm.
```bash
helm install mykafka oci://registry-1.docker.io/bitnamicharts/kafka
```
Install Kafka UI using Helm. The cluster name in UI and bootstrap server values are in `kafka_ui_values.yaml`.
```bash
helm repo add kafka-ui https://provectus.github.io/kafka-ui-charts
helm install kafka-ui kafka-ui/kafka-ui -f kafka_ui_values.yaml
```

