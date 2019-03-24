from video.managing import VideoManaging
from transcribe.transcribe import AudioTranscribe
from video.audio import AudioStreaming
import time
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/danielhidalgo/Downloads/credentials.json"

RES_PATH = '.tmp/{}.wav'.format(str(int(time.time())))
RATE = 16000
CHUNK = 1024*1000


video_managing = VideoManaging('samples/florentino.mp4', RATE, RES_PATH)

audio_path, audio_duration = video_managing.manage()

audio_transcribe = AudioTranscribe(RES_PATH, RATE, CHUNK, audio_duration)

audio_transcribe.transcribe()



