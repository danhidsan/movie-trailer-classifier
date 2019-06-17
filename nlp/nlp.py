import spacy
from spacy.lang.en.stop_words import STOP_WORDS

sample = u"Words are, in my not-so-humble opinion,\
    our most inexhaustible source of magic"


def text_pipeline(text):
    # TODO: do that this line run only one time
    nlp = spacy.load('en')
    doc = nlp(text)

    # Applies conditions to tokens and return the token lemma
    tokens = [
        (token.lemma_, token.pos_) for token in doc
        if not token.is_stop and    # Remove stop words
        not token.pos_ == 'PUNCT' and   # Remove punctuation sign
        not token.pos_ == 'SPACE'   # Remove spaces
        ]

    return tokens
