#! /usr/bin/python3
import argparse
import logging
import json
import msgpack

from kafka import KafkaConsumer
from _kafka.producer import Producer
from ml.classifier import TextClassifier

# log config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Consumer:

    def __init__(self, topic, servers=['localhost:9092']):
        self._kafka_consumer = KafkaConsumer(
            topic, bootstrap_servers=servers, 
            value_deserializer=msgpack.unpackb
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
        '--servers', type=str, nargs='+', help='Servers hosts'
        )
    parser.add_argument(
        '--input', action='store_true',
        help='Run consumer type input data'
        )
    parser.add_argument(
        '--output', action='store_true',
        help='Run consumer type output data'
    )

    args = parser.parse_args()

    servers = ['localhost:32771']

    if args.servers is not None:
        print(args.servers)
        servers = args.servers

    if args.output:
        logging.info("Running consumer type output")
        with Consumer('out_data', servers=servers) as stream:
            generator = stream.generator()
            for message in generator:
                print(message.value.decode('utf-8'))

    if args.input:
        logging.info("Running consumer type input")
        classifier = TextClassifier()
        logging.info(
            "Created Classifier with ${}".format(
                classifier.get_classifier_name
                )
            )
        producer = Producer('out_data', servers=servers)
        with Consumer('in_data', servers=servers) as stream:
            generator = stream.generator()
            for message in generator:
                decoded = message.value.decode('utf-8')
                dict_decoded = json.loads(decoded)
                result = {
                    'video_name': dict_decoded['video_name'],
                    'rated': classifier.predict(
                        dict_decoded['transcription']
                        )[0]
                }
                print(result)
                producer.send_data(result)