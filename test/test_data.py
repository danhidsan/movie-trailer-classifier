import unittest
import logging

from unittest.mock import patch

from data.dataset_subtitle import (
    format_imdb_id, clean_text, get_subs_zip_url_yifysubtitles,
    get_subtitles
)

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class DataTestModule(unittest.TestCase):

    logging.info("Preparing set up test for Data Module")

    def test_format_imdb_id(self):

        logging.info("Format IMDB id test")

        # imdb_id equal to 5
        self.assertEqual(format_imdb_id(56231), 'tt0056231')

        # imdb_id equal to 6
        self.assertEqual(format_imdb_id(456321), 'tt0456321')

        # imdb_id grater than 6
        self.assertEqual(format_imdb_id(464654654), 'tt464654654')

    def test_clean_text(self):

        logging.info("Clean text test")

        # remove punctuation simbols
        text = "hello, world: this is .Python"
        text_result = "hello  world  this is  Python"
        self.assertEqual(clean_text(text), text_result)

        # remove <i> caracters
        text = "<i>hello, world: this is .Python</i>"
        text_result = " hello  world  this is  Python "
        self.assertEqual(clean_text(text), text_result)

    def test_get_zip_opensubtitles(self):

        logging.info("Get zip opensubtitles test")

        enviroment = {
            'RPC_USER': 'danhidsan',
            'RPC_PASS': 'rWWbKzEQfqXTG2X',
            'RPC_TOKEN': ''
        }

        with patch.dict('os.environ', enviroment):
            # good imdb id (Toy Story 3)
            imdb_id = '0435761'
            self.assertNotEqual(
                get_subs_zip_url_yifysubtitles(imdb_id), None
                )

            # bad imdb id
            imdb_id = 'imdb_id'
            self.assertEqual(
                get_subs_zip_url_yifysubtitles(imdb_id), None
            )

    def test_get_zip_yifysubtitles(self):

        logging.info("Get zip yifysubtitles test")

        # good imdb id (Toy Story 3)
        imdb_id = '0435761'
        self.assertNotEqual(
            get_subs_zip_url_yifysubtitles(imdb_id), None
            )

        # bad imdb id
        imdb_id = 'imdb_id'
        self.assertEqual(
            get_subs_zip_url_yifysubtitles(imdb_id), None
        )

    def test_get_subtitles(self):

        logging.info("Get subtitles test")

        # subtitle source not supported
        imdb_id = '0435761'
        bad_source = "my_source"
        self.assertRaises(Exception, get_subtitles, imdb_id, bad_source)

        # zip imposible access
        imdb_id = 'bad_0979098'
        good_source = 'yifysubtitles'
        self.assertEqual(get_subtitles(imdb_id, good_source), None)

        # correct imdb_id and correct source
        imdb_id = '0435761'
        good_source = 'yifysubtitles'
        self.assertIsInstance(get_subtitles(imdb_id, good_source), str)

if __name__ == '__main__':
    unittest.main()
