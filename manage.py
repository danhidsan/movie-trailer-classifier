from video.managing import VideoManaging
from video.audio import AudioStreaming
from transcribe.transcribe import AudioTranscribe
import time
import os
import io
from google.cloud import speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/danielhidalgo/Downloads/credentials.json"

RES_PATH = '.tmp/{}.wav'.format(str(int(time.time())))
RATE = 16000
CHUNK = 1024*1000


video_managing = VideoManaging('samples/florentino.mp4', RATE, RES_PATH)

audio_path = video_managing.manage()

audio_transcribe = AudioTranscribe(RES_PATH, RATE, CHUNK)

audio_transcribe.transcribe()



