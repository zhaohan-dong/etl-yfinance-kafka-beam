# Ingest YFinance data into Apache Kafka Topic
## Installing Kafka on Kubernetes
### Install kubectl Helm on Mac (Homebrew)
```bash
brew install helm kubernetes-cli
```
I have set-up a local kubernetes cluster using k3s on Raspberry Pi.
Copy the kubeconfig from `/etc/rancher/k3s/k3s.yaml` on the machine to `.kube/config`.
Rename the context and cluster address.

Install Kafka using Helm.
```bash
helm install mykafka oci://registry-1.docker.io/bitnamicharts/kafka
```
Install Kafka UI using Helm. The cluster name in UI and bootstrap server values are in `kafka_ui_values.yaml`.
```bash
helm repo add kafka-ui https://provectus.github.io/kafka-ui-charts
helm install kafka-ui kafka-ui/kafka-ui -f kafka_ui_values.yaml
```