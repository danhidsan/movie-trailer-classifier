import pickle
import time

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from nlp.nlp import text_tokenizer


def load_dataset(path: str, sep=',') -> pd.DataFrame:
    dataframe = pd.read_csv(path, sep=sep)

    return dataframe


def train(classifier, dataframe: pd.DataFrame):

    start = time.time()

    df_notnull = dataframe[pd.notna(dataframe['rated'])]

    train_data, test_data, train_target, test_target = train_test_split(
        df_notnull['subtitles'], df_notnull['rated'], random_state=0
    )

    classifier.fit(train_data.values.astype('U'), train_target)

    score = classifier.score(test_data, test_target)

    end = time.time()

    print("Accuracy: " + str(score) + ", Time duration: " + str(end - start))

    return classifier


dataframe = load_dataset(
    '/Users/danielhidalgo/Documents/developer/tfg/video_to_text/data/datasets/train_data2.csv',
    '|'
)

classifier = Pipeline(
    verbose=True,
    steps=[
        ('count_vectorizer', CountVectorizer(tokenizer=text_tokenizer)),
        ('transformer', TfidfTransformer()),
        ('classifier', MultinomialNB())
        ]
)

model = train(classifier, dataframe)

with open("ml/train/model.pickle", 'wb') as handle:
    pickle.dump(model, handle)

print("Training has been finished!!")
