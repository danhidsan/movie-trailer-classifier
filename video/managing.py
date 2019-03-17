import moviepy.editor as moviepy


class VideoManaging:

    def __init__(self, path, rate, res_path):
        self._path = path
        self._rate = rate
        self._res_path = res_path

    def __video_to_audio(self):

        """
        Read audio from file, using AudioFileClip class from moviepy library

        :return: AudioFileClip from moviepy
        """

        try:
            audio = moviepy.AudioFileClip(self._path)
            return audio
        except Exception as e:
            raise e

    def __audio_to_wave(self, audio):

        """
        Convert AudioFileClip from moviepy library in mono (one channel) .wav audio file

        :param audio: AudioFileClip param from moviepy library
        :return: success boolean or None
        """

        try:
            audio.write_audiofile(
                self._res_path,
                verbose=False,
                fps=self._rate,
                ffmpeg_params=['-ac', '1'])
            return True
        except Exception as e:
            print(e)
            return None

    def manage(self):

        try:
            audio_from_video = self.__video_to_audio()
            audio_path = self.__audio_to_wave(audio_from_video)
            return audio_path
        except Exception as e:
            raise e
