import unittest
import time
from kafka import KafkaProducer, KafkaConsumer
import json

SERVER_IP = "127.0.0.1:50518"

class TestKafkaMessaging(unittest.TestCase):

    def test_kafka_messaging(self):
        # Create KafkaProducer
        producer = KafkaProducer(bootstrap_servers=SERVER_IP, acks="all", value_serializer=(lambda v: json.dumps(v).encode('utf-8')))

        # Send a test message
        producer.send(topic="yfinance", value="Hello")

        # Create KafkaConsumer
        consumer = KafkaConsumer('yfinance', bootstrap_servers=SERVER_IP, auto_offset_reset='earliest')

        # Consume messages from the topic
        for _ in range(5):  # Try to consume messages for 5 seconds
            for message in consumer:
                value = json.loads(message.value.decode("utf-8"))  # Decode the value using JSON decoding
                if value == "Hello":
                    break  # Test message received successfully, exit the loop
            else:
                time.sleep(1)  # Wait for a second and try again
        self.fail("Test message not received from Kafka within the timeout")
        # Assert that the test message was received
        self.assertEqual(value, "Hello", "Test message not received from Kafka")

if __name__ == '__main__':
    unittest.main()
