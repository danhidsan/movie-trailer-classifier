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


# load datasets
yt_movielens = pd.read_csv('data/datasets/ml-youtube.csv')
links_movielens = pd.read_csv('data/datasets/links.csv')

# inner join datasets
yt_movielens_imdb = pd.merge(
  left=yt_movielens, right=links_movielens,
  left_on='movieId', right_on='movieId'
)


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
    year = re.search(
        r'\(\b(19|20)\d{2}\b\)', title
            ).group().replace('(', '').replace(')', '')

    return int(year)


