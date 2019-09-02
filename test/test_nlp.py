import unittest
import logging

from nlp.nlp import text_tokenizer

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class NlpTest(unittest.TestCase):

    logging.info("Preparing set up test for NLP")

    def test_text_tokenizer(self):

        logging.info("Text tokenizer test")

        # test pos_discard shorts words
        text = ": hello $ & . one  the dlskdhd she he now!"
        tokenization_result = text_tokenizer(text)
        self.assertFalse(len(tokenization_result) > 1)

        # test lemmatization
        text = "Copied"
        tokenization_result = text_tokenizer(text)
        self.assertEqual(tokenization_result[0], 'copy')

        # test stop words
        text = "above text"
        tokenization_result = text_tokenizer(text)
        self.assertEqual(tokenization_result[0], 'text')

if __name__ == '__main__':
    unittest.main()
