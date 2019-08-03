import zipfile
import io
import requests
import os
import pysrt
import logging
import string

from xmlrpc.client import ServerProxy
from bs4 import BeautifulSoup

from nlp.nlp import text_tokenizer

# log config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def format_imdb_id(imdb_id: int):
    """ Format imdb id acording his length
    """

    if len(str(imdb_id)) is 5:
        return 'tt00{}'.format(imdb_id)
    elif len(str(imdb_id)) is 6:
        return 'tt0{}'.format(imdb_id)
    else:
        return 'tt{}'.format(imdb_id)


def clean_text(text: str):

    # split by spaces
    text_split = text.split()

    table = str.maketrans(string.punctuation, ' '*len(string.punctuation))

    replaced_text = [
        w.replace('</i>', ' ').replace('<i>', ' ') for w in text_split
        ]

    stripped = [w.translate(table) for w in replaced_text]

    words_join = ' '.join(stripped)

    return words_join


def preprocessing_subtitles(subtitle: str):
    # Get subtitle tokens
    subtitles_tokens = text_tokenizer(subtitle)

    # get tokens text list
    text_first = [token for token in subtitles_tokens]
    text_join_first = ' '.join(text_first)

    # clean text
    clean_first = clean_text(text_join_first)

    # second tokenizer
    subtitles_tokens_second = text_tokenizer(clean_first)
    text_second = [token for token in subtitles_tokens_second]
    text_join_second = ' '.join(text_second)

    return text_join_second


def read_srt_file(path: str):
    # open .srt file
    subs = pysrt.open(path, encoding='iso-8859-1')

    # extract subs text
    subs_list = [
        sub.text
        for sub in subs
        ]

    return ' '.join(subs_list)


def get_subs_zip_url_opensubtitles(imdb_id: str):

    rpc_server = ServerProxy('https://api.opensubtitles.org:443/xml-rpc')
    rpc_user = os.environ.get('RPC_USER')
    rpc_pass = os.environ.get('RPC_PASS')
    rpc_token = os.environ.get('RPC_TOKEN')

    # imdb id search without login
    search_response = rpc_server.SearchSubtitles(
        os.environ.get('RPC_TOKEN'),
        [{'imdbid': imdb_id, 'sublanguageid': 'eng'}]
        )

    # If status 200 return data
    if search_response['status'].find('200') is not -1:
        data = search_response['data']
        if len(data) is 0:
            return None
        return data[0]['ZipDownloadLink']
    else:
        logging.info('Authentication failed')
        logging.info('Trying the athentication')
        # opensubtitles API login
        login_response = rpc_server.LogIn(
            rpc_user, rpc_pass, 'en', 'My Application v0.1'
        )

        if login_response['status'].find('200') is not -1:
            logging.info('Authenticated successfully')
            os.environ['RPC_TOKEN'] = login_response['token']

            # imdb id search before login
            search_response = rpc_server.SearchSubtitles(
                login_response['token'],
                [{'imdbid': imdb_id, 'sublanguageid': 'eng'}]
            )
            if search_response['status'].find('200') is not -1:
                data = search_response['data']
                if len(data) is 0:
                    return None
                return data[0]['ZipDownloadLink']
            else:
                logging.error('Search response error')
                return None
        else:
            logging.error('Authentication error')
            return None


def get_subs_zip_url_yifysubtitles(imdb_id: str):

    yify_url = 'https://www.yifysubtitles.com'
    yify_uri = yify_url + '/movie-imdb/'

    sub_request = requests.get(yify_uri + format_imdb_id(imdb_id))

    if sub_request.status_code == 200:
        url_list = []
        soup = BeautifulSoup(sub_request.text, 'html.parser')

        try:
            table_body = soup.find('tbody')
            table_tr_all = table_body.find_all('tr')
            for tr in table_tr_all:
                rating = int(tr.find(attrs={'class': 'rating-cell'}).text)
                lang = tr.find(attrs={'class': 'sub-lang'}).text
                sub_zip_url = yify_url + tr.find(
                    attrs={'class': 'download-cell'}
                    ).find('a').get('href').replace(
                        'subtitles/', 'subtitle/'
                        ) + '.zip'

                if lang == 'English':
                    url_list.append({
                        'rating': rating,
                        'sub_zip_url': sub_zip_url
                    })

            if len(url_list) == 0:
                return None

            result_url = sorted(
                url_list, key=lambda x: x['rating'], reverse=True
                )[0]['sub_zip_url']

        except Exception:
            return None

        return result_url
    elif sub_request.status_code == 401:
        logging.info('YIFY Subtitles unauthorized')
        return None


def get_subtitles(imdb_id: str, sub_source: str = 'opensubtitles'):

    sources = {
        'opensubtitles': get_subs_zip_url_opensubtitles,
        'yifysubtitles': get_subs_zip_url_yifysubtitles
    }

    if sub_source not in sources.keys():
        raise Exception(
            'Subtitle source not suported for "{}"'.format(sub_source)
            )

    store_path = 'data/srt/'

    logging.info('Getting subtitle for {}'.format(imdb_id))

    # get zipfile url
    zip_url = sources[sub_source](imdb_id)
    if zip_url is None:
        logging.error('Imposible obtain zip url for {}'.format(imdb_id))
        return None

    # dowloading zip file
    try:
        r = requests.get(zip_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
    except zipfile.BadZipFile:
        logging.error('Bad zip file for {} - {}'.format(imdb_id, r))
        return None

    # find .srt file and store the name
    srt_file_name = ''
    for file_name in z.namelist():
        if file_name.find('.srt') is not -1:
            srt_file_name = file_name
            break

    if srt_file_name is '':
        logging.error('srt file not found for {}'.format(imdb_id))
        return None

    # extract .srt file
    z.extract(srt_file_name, store_path)

    # read subtitles from .srt file
    srt_subs = read_srt_file(store_path + srt_file_name)

    # remove .srt file when process is finished
    os.remove(store_path + srt_file_name)

    return srt_subs

