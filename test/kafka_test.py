import unittest
from kafka import KafkaProducer, KafkaConsumer
import json
import threading

SERVER_IP = "localhost:29092"

class TestKafkaMessaging(unittest.TestCase):

    def test_kafka_messaging(self):
        # Set the timeout value in seconds
        timeout_seconds = 10

        # Create KafkaProducer
        value = ""
        group_id = 'test_user'
        producer = KafkaProducer(bootstrap_servers=SERVER_IP, acks="all", value_serializer=(lambda v: json.dumps(v).encode('utf-8')))

        # Send a test message
        producer.send(topic="test", value="Hello")

        # Create KafkaConsumer
        consumer = KafkaConsumer('test', bootstrap_servers=SERVER_IP, group_id=group_id, auto_offset_reset='earliest')

        # Define a function to consume messages
        def consume_messages():
            nonlocal value
            for message in consumer:
                value = json.loads(message.value.decode("utf-8"))  # Decode the value using JSON decoding
                self.assertEqual(value, "Hello", "Test message not received from Kafka")
                break

        # Start the consuming thread
        consuming_thread = threading.Thread(target=consume_messages)
        consuming_thread.start()
        consuming_thread.join(timeout_seconds)

        if consuming_thread.is_alive():
            # If the thread is still running, it means it timed out
            self.fail(f"Test timed out after {timeout_seconds} seconds.")

if __name__ == '__main__':
    unittest.main()
