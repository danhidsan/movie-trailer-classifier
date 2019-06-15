#! /usr/bin/python3
import sys
import getopt
import argparse

from kafka import KafkaConsumer


class Consumer:

    def __init__(self, topic, servers=['localhost:9092']):
        self._kafka_consumer = KafkaConsumer(
            topic, bootstrap_servers=servers
            )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def generator(self):
        for message in self._kafka_consumer:
            yield message


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Run kafka consumer')
    parser.add_argument(
        'topic', metavar='T', type=str, help='Topic for the consumer'
        )
    parser.add_argument('--servers', type=str, nargs='+')

    args = parser.parse_args()

    topic = args.topic
    servers = ['localhost:9092']

    if args.servers is not None:
        servers = args.servers

    with Consumer(topic, servers=servers) as stream:
        generator = stream.generator()
        for message in generator:
            print(message)
