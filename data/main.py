import logging
import csv
import requests
import time
import random
import sys
import os

import pandas as pd

from dataset_subtitle import (
    get_subtitles, preprocessing_subtitles, format_imdb_id
    )
from dataset_video import get_year

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def get_subtitles_write_csv(
        csv_writer: csv.DictWriter, dict_data: dict, json: dict,
        rated_filter: str = None
        ):
    """ Write row in csv with csv DictWriter
    """
    rated_set = ('G', 'PG', 'PG-13', 'R', 'NC-17')

    if 'Rated' in json:
        dict_data['rated'] = json['Rated'] if json['Rated'] in rated_set else 'other'
        if rated_filter is None or rated_filter == dict_data['rated']:
            logging.info('Processing {}-{}'.format(
                dict_data['imdb_id'],
                dict_data['title']
            ))
            subtitles = get_subtitles(
                str(dict_data['imdb_id']), 'opensubtitles'
                )
            if subtitles is not None:
                dict_data['subtitles'] = preprocessing_subtitles(
                    str(subtitles)
                    )
                csv_writer.writerow(
                    dict_data
                )
    else:
        logging.info('Rated not found for'.format(dict_data['imdb_id']))


def iterate_and_write_csv(
        dataframe: pd.DataFrame, csv_writer: csv.DictWriter,
        start_id: int = 0):
    """ Iterate dataframe data from id to dataframe final
    """

    sub_dataframe = dataframe[start_id:]

    for index, row in sub_dataframe.iterrows():
        time.sleep(random.randint(0, 10))
        if get_year(row['title']) > 1960:
            formatted_imdb_id = format_imdb_id(row['imdbId'])

            # Params for the request
            params = {
                "i": formatted_imdb_id,
                "apikey": 'd18bfa21'
                }
            omdb_url = 'http://www.omdbapi.com/'

            # request to omdb for obtain Rated
            req = requests.get(omdb_url, params=params)
            if req.status_code == 200:
                json = req.json()
                get_subtitles_write_csv(
                    csv_writer,
                    {
                        'id': index,
                        'imdb_id': row['imdbId'],
                        'title': row['title']
                    },
                    json
                )
        else:
            continue


def iter_write_csv_random(
        input_dataframe: pd.DataFrame, train_dataframe: pd.DataFrame,
        csv_writer: csv.DictWriter, rated: str = None
        ):
    """ Iterate data frame a write csv randomly
    """

    rated_values = ('G', 'PG', 'PG-13', 'R', 'NC-17')

    if rated is not None and rated not in rated_values:
        raise Exception(
            "Rated parameter should be ('G', 'PG', 'PG-13', 'R', 'NC-17')"
            )

    # getting id set from train dataframe
    movie_id_set = set(train_dataframe['id'].values)

    # rows which is not in movie_id_set
    rest_data_frame = input_dataframe[
        ~input_dataframe['movieId'].isin(movie_id_set)
        ]

    while len(rest_data_frame) > 0:
        sample = rest_data_frame.sample().iloc[0]
        index = list(rest_data_frame.sample().to_dict()['youtubeId'].keys())[0]

        year = get_year(sample.title)
        if year is not None and year > 1960:
            formatted_imdb_id = format_imdb_id(sample.imdbId)

            # Params for the request
            params = {
                "i": formatted_imdb_id,
                "apikey": 'd18bfa21'
                }
            omdb_url = 'http://www.omdbapi.com/'

            # request to omdb for obtain Rated
            req = requests.get(omdb_url, params=params)
            if req.status_code == 200:
                json = req.json()
                get_subtitles_write_csv(
                    csv_writer,
                    {
                        'id': index,
                        'imdb_id': sample.imdbId,
                        'title': sample.title
                    },
                    json,
                    rated
                )

                # removing dataframe row
                rest_data_frame = rest_data_frame[
                    rest_data_frame['movieId'] != sample.movieId
                ]
            elif req.status_code == 401:
                logging.info("OMDB API Unanthorized")     
        else:
            # removing dataframe row
            rest_data_frame = rest_data_frame[
                    rest_data_frame['movieId'] != sample.movieId
                ]
            continue


if __name__ == "__main__":

    if sys.argv[1] == 'id':
        logging.info('Starting load dataset')

        # load datasets
        yt_movielens = pd.read_csv(
            os.path.join(FILE_PATH, "datasets/ml-youtube.csv")
            )
        links_movielens = pd.read_csv(
            os.path.join(FILE_PATH, "datasets/links.csv")
            )

        # inner join datasets
        yt_movielens_imdb = pd.merge(
            left=yt_movielens, right=links_movielens,
            left_on='movieId', right_on='movieId'
            )

        with open(os.path.join(FILE_PATH, 'datasets/train_data2.csv'), 'a') as file:
            logging.info('Opening csv')
            field_names = ['id', 'imdb_id', 'title', 'rated', 'subtitles']
            csv_writer = csv.DictWriter(
                file, fieldnames=field_names, delimiter='|'
            )

            iterate_and_write_csv(
                yt_movielens_imdb, csv_writer, start_id=int(sys.argv[2])
                )

    elif sys.argv[1] == 'random':

        logging.info('Starting load dataset randomly')

        # load datasets
        yt_movielens = pd.read_csv(
            os.path.join(FILE_PATH, "datasets/ml-youtube.csv")
            )
        links_movielens = pd.read_csv(
            os.path.join(FILE_PATH, "datasets/links.csv")
            )

        # inner join datasets
        yt_movielens_imdb = pd.merge(
            left=yt_movielens, right=links_movielens,
            left_on='movieId', right_on='movieId'
            )

        # load train dataset
        train_dataframe = pd.read_csv(
            os.path.join(FILE_PATH, 'datasets/train_dataset.csv'), sep='|'
            )

        with open(os.path.join(FILE_PATH, 'datasets/train_dataset.csv'), 'a') as file:
            logging.info('Opening csv')
            field_names = ['id', 'imdb_id', 'title', 'rated', 'subtitles']
            csv_writer = csv.DictWriter(
                file, fieldnames=field_names, delimiter='|'
            )

            iter_write_csv_random(
                yt_movielens_imdb, train_dataframe, csv_writer
                )

    else:
        print(
            """
            Error: Choose any of following params:
                - id
                - random
            """
            )
