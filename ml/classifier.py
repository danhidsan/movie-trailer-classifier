import pickle
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

from nlp.nlp import text_tokenizer


def predict(text: str):

    # Loading model and vocabulary from pickle
    model = pickle.load(open('ml/train/model.pickle', 'rb'))
    vocabulary = pickle.load(open('ml/train/vocab.pickle', 'rb'))

    # Adding vocabulary∫
    model.set_params(count_vectorizer__vocabulary=vocabulary)

    # Predict text
    prediction = model.predict([r'{}'.format(text)])

    return prediction


class Pipeline:

    MULTINOMIAL_NB = 'get_multinomial_nb'
    LINEAR_SVC = 'get_linear_svc'
    LOGISTIC_REGRESSION = 'get_logistic_regression'
    RANDOM_FOREST = 'get_random_forest'

    @property
    def get_multinomial_nb(self):
        return SkPipeline(
            verbose=True,
            steps=[
                ('vectorizer', CountVectorizer(
                    tokenizer=text_tokenizer, ngram_range=(1, 3))),
                ('transformer', TfidfTransformer()),
                ('classifier', MultinomialNB())
                ]
            )

    @property
    def get_linear_svc(self):
        return SkPipeline(
                    verbose=True,
                    steps=[
                        ('vectorizer', CountVectorizer(
                            tokenizer=text_tokenizer, ngram_range=(1, 3)
                        )),
                        ('transformer', TfidfTransformer()),
                        ('classifier', LinearSVC())
                    ]
        )

    @property
    def get_logistic_regression(self):
        return Pipeline(
            verbose=True,
            steps=[
                ('vectorizer', CountVectorizer(
                    tokenizer=text_tokenizer, ngram_range=(1, 3))),
                ('transformer', TfidfTransformer()),
                ('classifier', LogisticRegression())
                ]
            )

    @property
    def get_random_forest(self):
        return SkPipeline(
            verbose=True,
            steps=[
                ('vectorizer', CountVectorizer(
                    tokenizer=text_tokenizer, ngram_range=(1, 3))),
                ('transformer', TfidfTransformer()),
                ('classifier', RandomForestClassifier())
                ]
            )


class TextClassifier(Pipeline):

    def __init__(self):

        try:
            self.model = pickle.load(open('/Users/danielhidalgo/Documents/developer/tfg/video_to_text/ml/train/model.pickle', 'rb'))
            self.vocabulary = pickle.load(open('/Users/danielhidalgo/Documents/developer/tfg/video_to_text/ml/train/vocab.pickle', 'rb'))
        except FileNotFoundError:
            raise FileNotFoundError()

    def __get_classifier(self, classifier: str):

        try:
            classifier = getattr(self, classifier)
        except AttributeError:
            raise AttributeError("unsupported classifier")

        return classifier

    @staticmethod
    def __print_confusion_matrix(
            target, pred, labels, figsize=(10, 7), fontsize=14):
        """ Prints a confusion matrix, as returned by
            sklearn.metrics.confusion_matrix, as a heatmap.
        """

        conf_mat = confusion_matrix(target, pred)

        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(
            conf_mat, annot=True, fmt='d', xticklabels=labels,
            yticklabels=labels
        )

        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.show()

    @property
    def get_classifier_name(self):

        classifier = self.model.get_params()['classifier']

        return classifier.__class__.__name__

    def train(self, classifier: str):
        dataframe = pd.read_csv(
            '/Users/danielhidalgo/Documents/developer/tfg/video_to_text/data/datasets/train_dataset.csv',
            sep='|'
        )
        classifier = self.__get_classifier(classifier)

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
        with open("vocab.pickle", 'wb') as handle:
            pickle.dump(vocabulary, handle)

        # Storing model
        with open("model.pickle", 'wb') as handle:
            pickle.dump(classifier, handle)

        # Returns the mean accuracy on the given test data and labels.
        score = classifier.score(test_data_values, test_target_values)
        print('-----------------ACCURANCY SCORE--------------------')
        print('Accuracy: {}'.format(str(score)))

        # Predicting class labels for samples
        pred = classifier.predict(test_data_values)

        # Confusion matrix
        self.__print_confusion_matrix(test_target_values, pred, labels)

        end = time.time()

        print('Time: {} s'.format(end-start))

        self.model = classifier

        print("Training has been finished!!")

    def predict(self, text: str):

        prediction = self.model.predict([r'{}'.format(text)])

        return prediction

