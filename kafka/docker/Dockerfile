# syntax=docker/dockerfile:1

# Stage 0: Fetch rockylinux-9.2
FROM rockylinux:9.2 AS baseos
RUN dnf -y upgrade && dnf -y install java-17-openjdk
RUN mkdir /home/root
WORKDIR /home/root

# Stage 1: Download kafka
FROM baseos AS install-kafka

# Download the tar file
RUN curl -sLO https://dlcdn.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz && \
    tar -xzf kafka_2.13-3.5.0.tgz && \
    rm -f kafka_2.13-3.5.0.tgz && \
    mv kafka_2.13-3.5.0 kafka
# Enter the directory
WORKDIR /home/root/kafka

# Run kafka
COPY run_kafka.sh /home/root/kafka/run_kafka.sh
RUN chmod +x run_kafka.sh
ENTRYPOINT ["/bin/bash", "/home/root/kafka/run_kafka.sh"]
