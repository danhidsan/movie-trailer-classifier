import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS

# for install other languajes models, run next command:
# - python3 -m spacy download ${lang_code}
# - Example: python3 -m spacy download en

sample = u"Words are, in my not-so-humble opinion,\
    our most inexhaustible source of magic"


nlp = spacy.load('en')
doc = nlp(sample)

# Print out tokens
for token in doc:
    print(token)

# Store tokens as list, print out
tokens = [token for token in doc]
print(tokens)

# Store tokens as list, without stop words
token_without_sw = [token for token in doc if not token.is_stop]
print(token_without_sw)

# Print token information
for token in doc:
    print(
        token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        token.shape_, token.is_alpha, token.is_stop
    )

# Visualizing doc with displacy. For visusalization in a server user next
# command: displacy.serve()
displacy = displacy.render(
    doc, style='dep', options={'distance': 70}
    )
