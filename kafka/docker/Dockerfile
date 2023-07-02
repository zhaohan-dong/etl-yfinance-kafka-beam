# syntax=docker/dockerfile:1

# Fetch rockylinux-9.2
FROM rockylinux:9.2 AS baseos
RUN dnf -y upgrade
RUN mkdir /home/root
WORKDIR /home/root

# Download kafka
FROM baseos AS install-kafka
# Download the tar file
RUN curl -LOs https://dlcdn.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz
RUN tar -xzf kafka_2.13-3.5.0.tgz
RUN rm -f kafka_2.13-3.5.0.tgz
# Enter the directory
cd kafka_2.13-3.5.0



ENTRYPOINT ["/bin/bash"]