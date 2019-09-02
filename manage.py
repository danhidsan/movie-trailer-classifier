import time
import os
import sys
import logging
import csv
import random
import requests
import argparse
import pickle

import pandas as pd

from video.managing import VideoManaging
from transcribe.transcribe import AudioTranscribe
from _kafka.producer import Producer
from _kafka.consumer import Consumer
from data.dataset_subtitle import get_subtitles
from data.dataset_video import get_year

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'
] = os.path.join(FILE_PATH, "credentials.json")


# On transcribe callback
def on_transcribe_data(data):
    kafka_connector.send_data(data)


# main
if __name__ == '__main__':

    parser = argparse.ArgumentParser('Run video transcribe')
    parser.add_argument(
        'video', metavar='V', type=str, help="Video path"
        )
    parser.add_argument(
        '--servers', type=str, nargs='+', help='Servers hosts'
        )

    args = parser.parse_args()

    RES_PATH = '.tmp/{}.wav'.format(str(int(time.time())))
    RATE = 16000
    CHUNK = 1024*100

    video_managing = VideoManaging(
        args.video, RATE, RES_PATH
        )

    audio_path, audio_duration = video_managing.manage()

    kafka_connector = Producer(
            'in_data', servers=args.servers
            )

    audio_transcribe = AudioTranscribe(
        args.video.split('/')[-1],
        RES_PATH, RATE, CHUNK, audio_duration,
        on_transcribe=on_transcribe_data
        )

    audio_transcribe.transcribe()
