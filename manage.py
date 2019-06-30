import time
import os
import sys
import logging
import csv
import random
import requests
import pandas as pd

from video.managing import VideoManaging
from transcribe.transcribe import AudioTranscribe
from _kafka.producer import Producer
from _kafka.consumer import Consumer
from nlp.nlp import text_pipeline
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

    if sys.argv[1] == 'consumer':
        with Consumer('audio-streaming') as stream:
            generator = stream.generator()
            for message in generator:
                tokens = text_pipeline(message.value.decode('utf-8'))
                print(tokens)
    elif sys.argv[1] == 'transcribe':

        RES_PATH = '.tmp/{}.wav'.format(str(int(time.time())))
        RATE = 16000
        CHUNK = 1024*100

        video_managing = VideoManaging(
            'samples/mayuko.mp4', RATE, RES_PATH
            )

        audio_path, audio_duration = video_managing.manage()

        kafka_connector = Producer('audio-streaming')

        audio_transcribe = AudioTranscribe(
            RES_PATH, RATE, CHUNK, audio_duration,
            on_transcribe=on_transcribe_data
            )

        audio_transcribe.transcribe()
