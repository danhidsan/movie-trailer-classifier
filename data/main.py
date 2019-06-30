import logging
import csv
import requests
import time
import pandas as pd

from dataset_subtitle import get_subtitles
from dataset_video import get_year

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def write_csv(csv_writer: csv.DictWriter, dict_data: dict, json: dict):
    """ Write row in csv with csv DictWriter
    """

    if 'Rated' in json:
        dict_data['rated'] = json['Rated']
        csv_writer.writerow(
            dict_data
        )
    else:
        logging.info(
            'Rated not found for'.format(
                dict_data['imdb_id']
                )
            )


def format_imdb_id(imdb_id: int):
    """ Format imdb id acording his length
    """

    if len(str(imdb_id)) is 5:
        return 'tt00{}'.format(imdb_id)
    else:
        return 'tt0{}'.format(imdb_id)


def iterate_and_write_csv(
        dataframe: pd.DataFrame, csv_writer: csv.DictWriter,
        start_id: int = 0):
    """ Iterate dataframe data from id to dataframe final
    """

    sub_dataframe = dataframe[start_id:]

    for index, row in sub_dataframe.iterrows():
        time.sleep(1)
        if get_year(row['title']) > 1960:

            logging.info('Processing {}-{}'.format(
                row['imdbId'],
                row['title']
            ))

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

                subtitles = get_subtitles(row['imdbId'])
                if subtitles is not None:
                    write_csv(
                        csv_writer,
                        {
                            'id': index,
                            'imdb_id': row['imdbId'],
                            'title': row['title'],
                            'subtitles': subtitles
                        },
                        json
                    )
        else:
            continue


if __name__ == "__main__":
    logging.info('Starting load dataset')

    # load datasets
    yt_movielens = pd.read_csv('data/datasets/ml-youtube.csv')
    links_movielens = pd.read_csv('data/datasets/links.csv')

    # inner join datasets
    yt_movielens_imdb = pd.merge(
        left=yt_movielens, right=links_movielens,
        left_on='movieId', right_on='movieId'
        )

    with open('data/datasets/train_data.csv', 'a') as file:
        logging.info('Opening csv')
        field_names = ['id', 'imdb_id', 'title', 'rated', 'subtitles']
        csv_writer = csv.DictWriter(
            file, fieldnames=field_names, delimiter='|'
        )

        iterate_and_write_csv(
            yt_movielens_imdb, csv_writer, start_id=764
            )

        
