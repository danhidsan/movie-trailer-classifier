import requests
import time
import random
import re
import logging
import os
import pandas as pd
from pytube import YouTube


# logging info
logging.basicConfig(level=logging.INFO)


# handle on complete download
def handle_on_complete(stream, file_handle):
    logging.info('download has been completed')


def download_youtube_video(
        youtube_id,
        on_complete_download=handle_on_complete):

    yt = YouTube(
        'https://www.youtube.com/watch?v={}'.format(youtube_id),
        on_complete_callback=on_complete_download
    )

    stream = yt.streams.filter(res='360p', audio_codec='mp4a.40.2').first()

    logging.info('Downloading {}'.format(stream.default_filename))
    stream.download('data/videos')


def get_year(title: str):
    year = re.search(r'\(\b(19|20)\d{2}\b\)', title)

    if year is not None:
        return int(year.group().replace('(', '').replace(')', ''))
    else:
        return None

