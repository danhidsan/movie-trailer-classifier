import unittest

from nlp.nlp import text_tokenizer


class NlpTest(unittest.TestCase):

    def test_text_tokenizer(self):

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
