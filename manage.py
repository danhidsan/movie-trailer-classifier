from video.managing import VideoManaging
from transcribe.transcribe import AudioTranscribe
from connector.connector import KafkaConnector
import time
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/danielhidalgo/Downloads/credentials.json"

RES_PATH = '.tmp/{}.wav'.format(str(int(time.time())))
RATE = 16000
CHUNK = 1024*100


video_managing = VideoManaging('samples/florentino.mp4', RATE, RES_PATH)

audio_path, audio_duration = video_managing.manage()

kafka_connector = KafkaConnector('audio-streaming')


# On transcribe callback
def on_transcribe_data(data):
    kafka_connector.send_data(data)


audio_transcribe = AudioTranscribe(RES_PATH, RATE, CHUNK, audio_duration, on_transcribe=on_transcribe_data)

audio_transcribe.transcribe()



