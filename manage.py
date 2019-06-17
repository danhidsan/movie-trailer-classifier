import time
import os
import sys

from video.managing import VideoManaging
from transcribe.transcribe import AudioTranscribe
from _kafka.producer import Producer
from _kafka.consumer import Consumer
from nlp.nlp import text_pipeline


# On transcribe callback
def on_transcribe_data(data):
    kafka_connector.send_data(data)

# main
if __name__ == '__main__':
    try:
        if sys.argv[1] == 'consumer':
            with Consumer('audio-streaming') as stream:
                generator = stream.generator()
                for message in generator:
                    tokens = text_pipeline(message.value.decode('utf-8'))
                    print(tokens)
        elif sys.argv[1] == 'transcribe':
            os.environ[
                'GOOGLE_APPLICATION_CREDENTIALS'
                ] = "/Users/danielhidalgo/Downloads/credentials.json"

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
    except IndexError:
        print("""
            Debe introducir uno de los 2 siguientes argumentos
                - consumer
                - transcribe
        """)
