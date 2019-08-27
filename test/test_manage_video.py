import unittest
import time

from video.managing import VideoManaging


class ManageVideoTest(unittest.TestCase):

    def setUp(self):

        RES_PATH = '.tmp/{}.wav'.format(str(int(time.time())))
        RATE = 16000

        self.bad_video_managing = VideoManaging(
            '/Users/danielhidalgo/Documents/developer/tfg/video_to_text/samples/harry_potter.mp4',
            RATE, RES_PATH
        )

        self.good_video_managing = VideoManaging(
            '/Users/danielhidalgo/Documents/developer/tfg/video_to_text/samples/showgirls.mp4',
            RATE, RES_PATH
        )

    def test_video_to_audio(self):

        # managing heavy video
        self.assertRaises(IOError, self.bad_video_managing.manage)

        # good video
        expected_audio_duration = 112.2
        audio_path, audio_duration = self.good_video_managing.manage()
        self.assertEqual(audio_duration, expected_audio_duration)

if __name__ == '__main__':
    unittest.main()
