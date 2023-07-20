# Ingest YFinance data into Apache Kafka Topic

## Installing Kafka on docker-compose
Go to `./kafka_docker` directory and run the following command.
```bash
docker-compose up -d
```

To test the setup, run `kafka_test.py` script in the root test directory.

## Installing Kafka on Kubernetes
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