import wave
import os
import time


class AudioStreaming:

    def __init__(self, path, rate, chunk, audio_duration):
        self._wf = wave.open(path, 'rb')
        self._file_stats = os.stat(path)
        self._chunk = chunk
        self._rate = rate
        self._duration = audio_duration
        self.closed = True

    def __enter__(self):

        # Audio chunks number
        audio_chunks = self._file_stats.st_size / self._chunk

        # Calculating wait time to add time sleep between data chunks
        self._wait_time = self._duration / audio_chunks

        # Streaming state is active
        self.closed = False

        return self

    def __exit__(self, type, value, traceback):

        # close
        self.closed = True

    def generator(self):
        while not self.closed:

            data = self._wf.readframes(self._chunk)
            time.sleep(self._wait_time)
            if data != b'':
                yield data
            else:
                break










