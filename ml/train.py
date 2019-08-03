import pickle
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import xgboost as xgb

from sklearn.feature_extraction.text import (
    CountVectorizer, TfidfTransformer, TfidfVectorizer
    )
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

from nlp.nlp import text_tokenizer


def load_dataset(path: str, sep=',') -> pd.DataFrame:
    dataframe = pd.read_csv(path, sep=sep)

    return dataframe


def print_confusion_matrix(
        test_target, pred, labels, figsize=(10, 7), fontsize=14):
    """ Prints a confusion matrix, as returned by
        sklearn.metrics.confusion_matrix, as a heatmap.
    """

    conf_mat = confusion_matrix(test_target, pred)

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        conf_mat, annot=True, fmt='d', xticklabels=labels,
        yticklabels=labels
    )

    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()


def train(classifier, dataframe: pd.DataFrame):

    start = time.time()

    df_clean = dataframe[
        (pd.notna(dataframe['rated'])) &
        (
            (dataframe.rated == 'G') |
            (dataframe.rated == 'PG') |
            (dataframe.rated == 'PG-13') |
            (dataframe.rated == 'R') |
            (dataframe.rated == 'NC-17')
        )
        ]

    train_data, test_data, train_target, test_target = train_test_split(
        dataframe['subtitles'], dataframe['rated'],
        test_size=0.25, random_state=0
    )

    labels = list(set(dataframe.rated.values))

    # Train data values
    train_data_values = train_data.values.astype('U')
    train_target_values = train_target.values.astype('U')

    # Test data values
    test_data_values = test_data.values.astype('U')
    test_target_values = test_target.values.astype('U')

    # Fitting classifier
    classifier.fit(train_data_values, train_target_values)

    # Storing vocabulay
    vocabulary = classifier.get_params()['vectorizer'].vocabulary_
    pickle.dump(vocabulary, open("vocab.pickle", 'wb'))

    # Returns the mean accuracy on the given test data and labels.
    score = classifier.score(test_data_values, test_target_values)
    print('-----------------ACCURANCY SCORE--------------------')
    print('Accuracy: {}'.format(str(score)))

    # Predicting class labels for samples
    pred = classifier.predict(test_data_values)

    # F1 Score
    f1_score_ = f1_score(test_data_values, pred, labels=labels, average='weighted')
    print('-----------------F1 Score----------------------')
    print('Score: {}'.format(f1_score_))

    # Confusion matrix
    print_confusion_matrix(test_target_values, pred, labels)

    end = time.time()

    print('Time: {} s'.format(end-start))

    return classifier


dataframe = load_dataset(
    '/Users/danielhidalgo/Documents/developer/tfg/video_to_text/data/datasets/train_dataset.csv',
    '|'
)

classifier_naive_bayes = Pipeline(
    verbose=True,
    steps=[
        ('vectorizer', CountVectorizer(
            tokenizer=text_tokenizer, ngram_range=(1, 3)
            )),
        ('transformer', TfidfTransformer()),
        ('classifier', MultinomialNB())
        ]
)

classifier_linear_svc = Pipeline(
    verbose=True,
    steps=[
        ('vectorizer', CountVectorizer(
            tokenizer=text_tokenizer, ngram_range=(1, 3)
            )),
        ('transformer', TfidfTransformer()),
        ('classifier', LinearSVC())
        ]
)

classifier_logistic_regression = Pipeline(
    verbose=True,
    steps=[
        ('vectorizer', CountVectorizer(
            tokenizer=text_tokenizer, ngram_range=(1, 3)
            )),
        ('transformer', TfidfTransformer()),
        ('classifier', LogisticRegression())
        ]
)

classifier_random_forest = Pipeline(
    verbose=True,
    steps=[
        ('vectorizer', CountVectorizer(
            tokenizer=text_tokenizer, ngram_range=(1, 3)
            )),
        ('tranformer', TfidfTransformer()),
        ('classifier', RandomForestClassifier())
    ]
)

classifier_xgb = Pipeline(
    verbose=True,
    steps=[
        ('vectorizer', CountVectorizer(
            tokenizer=text_tokenizer, ngram_range=(1, 3)
            )),
        ('transformer', TfidfTransformer()),
        ('classifier', xgb.XGBClassifier(
            max_depth=3, n_estimators=300, learning_rate=0.1, verbosity=3,
            n_jobs=4
            ))
        ]
)

model = train(classifier_linear_svc, dataframe)

with open("ml/train/model.pickle", 'wb') as handle:
    pickle.dump(model, handle)

print("Training has been finished!!")
