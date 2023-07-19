#!/bin/bash

# Start ZooKeeper
/bin/bash bin/zookeeper-server-start.sh config/zookeeper.properties &

# Start Kafka
/bin/bash bin/kafka-server-start.sh config/server.properties
