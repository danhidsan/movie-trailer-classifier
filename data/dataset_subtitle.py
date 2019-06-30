import zipfile
import io
import requests
import os
import pysrt
import logging

from xmlrpc.client import ServerProxy

# log config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


rpc_server = ServerProxy('https://api.opensubtitles.org:443/xml-rpc')
rpc_user = os.environ.get('RPC_USER')
rpc_pass = os.environ.get('RPC_PASS')
rpc_token = os.environ.get('RPC_TOKEN')


def read_srt_file(path: str):
    # open .srt file
    subs = pysrt.open(path, encoding='iso-8859-1')

    # extract subs text
    subs_list = [sub.text for sub in subs]

    return ''.join(subs_list)


def get_subs_zip_url(imdb_id: str):

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


def get_subtitles(imdb_id: str):
    store_path = 'data/srt/'

    logging.info('Getting subtitle for {}'.format(imdb_id))

    # get zipfile url
    zip_url = get_subs_zip_url(imdb_id)
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
