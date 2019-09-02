import unittest
import time
import logging
import os

import moviepy.editor as moviepy

from video.audio import AudioStreaming
from video.managing import VideoManaging

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class ManageAudioTest(unittest.TestCase):

    logging.info("Preparing set up test for Manage Audio")

    def setUp(self):

        RATE = 16000
        CHUNK = 1024*100

        audio_path = os.path.join(FILE_PATH, 'samples/showgirls.wav')
        audio = moviepy.AudioFileClip(audio_path)

        with AudioStreaming(audio_path, RATE,
                            CHUNK, audio.duration) as stream:
            self.audio_generator = stream.generator()

    def test_streaming_audio(self):

        logging.info("Streaming audio test")

        # test streaming
        for value in self.audio_generator:
            self.assertIsNotNone(value)
            return

if __name__ == '__main__':
    unittest.main()
