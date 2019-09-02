import unittest
import time
import logging
import os

from video.managing import VideoManaging

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class ManageVideoTest(unittest.TestCase):

    logging.info("Preparing set up test for Manage Video")

    def setUp(self):

        RES_PATH = '.tmp/{}.wav'.format(str(int(time.time())))
        RATE = 16000

        self.bad_video_managing = VideoManaging(
            os.path.join(FILE_PATH, '../samples/harry_potter.mp4'),
            RATE, RES_PATH
        )

        self.good_video_managing = VideoManaging(
            os.path.join(FILE_PATH, '../samples/showgirls.mp4'),
            RATE, RES_PATH
        )

    def test_video_to_audio(self):

        logging.info("Video to Audio test")

        # managing heavy video
        self.assertRaises(IOError, self.bad_video_managing.manage)

        # good video
        expected_audio_duration = 112.2
        audio_path, audio_duration = self.good_video_managing.manage()
        self.assertEqual(audio_duration, expected_audio_duration)

if __name__ == '__main__':
    unittest.main()
