
import re
import sys
import json

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from video.audio import AudioStreaming


class AudioTranscribe:

    def __init__(
            self, video_name, path, rate, chunk, audio_duration,
            on_transcribe=print
            ):
        self.video_name = video_name
        self._path = path
        self._rate = rate
        self._chunk = chunk
        self._audio_duration = audio_duration
        self._on_transcribe = on_transcribe

    def __print_responses(self, responses):

        num_chars_printed = 0
        text_buffer = ""
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care
            # about the first result being considered, since once it's
            # `is_final`, it moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end
            # of the line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')

                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                self._on_transcribe({
                    'video_name': self.video_name,
                    'transcription': transcript + overwrite_chars
                    })

                text_buffer += transcript + overwrite_chars

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break

                num_chars_printed = 0

        return text_buffer

    def transcribe(self):
        language_code = 'en-US'

        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self._rate,
            language_code=language_code)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        with AudioStreaming(self._path, self._rate,
                            self._chunk, self._audio_duration) as stream:
            audio_generator = stream.generator()
            response_buffer = ""
            for content in audio_generator:
                requests = [
                    types.StreamingRecognizeRequest(audio_content=content)
                    ]
                responses = client.streaming_recognize(
                    streaming_config, requests
                    )

                # Now, put the transcription responses to use.
                response_buffer += self.__print_responses(responses)
