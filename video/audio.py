import pyaudio
import wave
import io

from six.moves import queue


class AudioStreaming:

    def __init__(self, path, rate, chunk):
        self._wf = wave.open(path, 'rb')
        self._chunk = chunk
        self._rate = rate

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            output=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.start_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        data = self._wf.readframes(frame_count)
        self._buff.put(data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    print(chunk)
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

    def __init_streaming(self):

        stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                             channels=self.wf.getnchannels(),
                             rate=self.wf.getframerate(),
                             output=True)

        return stream

    def __start_streaming(self, stream):
        data = self.wf.readframes(self.chunk)

        while data != '':
            stream.write(data)
            data = self.wf.readframes(self.chunk)

    def __stop_streaming(self, stream):
        stream.stop_stream()
        stream.close()

        self.p.terminate()










