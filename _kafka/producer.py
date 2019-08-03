import json

from kafka import KafkaProducer
from kafka.errors import KafkaError


class Producer:

    def __init__(self, topic, server="localhost:9092"):
        self._kafka_instance = KafkaProducer(bootstrap_servers=[server])
        self._topic = topic

    def send_data(self, data):
        data_str = json.dumps(data)
        data_bytes = bytes(data_str, 'utf-8')
        try:
            self._kafka_instance.send(self._topic, value=data_bytes)
        except KafkaError as e:
            raise e
