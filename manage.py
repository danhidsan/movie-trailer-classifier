import time
import os
import sys
import logging
import csv
import random
import requests
import argparse

import pandas as pd

from video.managing import VideoManaging
from transcribe.transcribe import AudioTranscribe
from _kafka.producer import Producer
from _kafka.consumer import Consumer
from data.dataset_subtitle import get_subtitles
from data.dataset_video import get_year

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'
] = "/Users/danielhidalgo/Downloads/credentials.json"


# On transcribe callback
def on_transcribe_data(data):
    kafka_connector.send_data(data)


# On complete transcribe
def handle_on_complete_transcribe(response_buffer):
    logging.info('transcribe has been finished')
    print(response_buffer)

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
            'in_data', servers=["192.168.100.110:32776"]
            )

    audio_transcribe = AudioTranscribe(
        RES_PATH, RATE, CHUNK, audio_duration,
        on_transcribe=on_transcribe_data,
        on_complete=handle_on_complete_transcribe
        )

    audio_transcribe.transcribe()
