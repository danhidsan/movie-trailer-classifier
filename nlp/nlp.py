import spacy

from spacy.lang.en.stop_words import STOP_WORDS

sample = u"Words are, in my not-so-humble opinion,\
    our most inexhaustible source of magic"


def text_tokenizer(text):
    # TODO: do that this line run only one time
    nlp = spacy.load('en')
    doc = nlp(text)

    # pos discard tuple
    pos_discard = ('PUNCT', 'SPACE', 'X', 'SYM', 'PRON', 'NUM', 'INTJ')

    # Applies conditions to tokens and return the token lemma
    tokens = [
        (token.lemma_, token.pos_) for token in doc
        if not token.is_stop and    # Remove stop words
        token.pos_ not in pos_discard and   # Discard some pos
        len(token.text) > 2
        ]

    return tokens
