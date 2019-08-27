import unittest
import time

import moviepy.editor as moviepy

from video.audio import AudioStreaming
from video.managing import VideoManaging


class ManageAudioTest(unittest.TestCase):

    def setUp(self):

        RATE = 16000
        CHUNK = 1024*100

        audio_path = '/Users/danielhidalgo/Documents/developer/tfg/video_to_text/test/samples/showgirls.wav'
        audio = moviepy.AudioFileClip(audio_path)

        with AudioStreaming(audio_path, RATE,
                            CHUNK, audio.duration) as stream:
            self.audio_generator = stream.generator()

    def test_streaming_audio(self):

        # test streaming
        for value in self.audio_generator:
            self.assertIsNotNone(value)
            return

if __name__ == '__main__':
    unittest.main()
