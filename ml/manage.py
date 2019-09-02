import getopt
import sys
import os
import logging

from ml.classifier import TextClassifier


# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# main
if __name__ == '__main__':

    optlist, additional = getopt.getopt(sys.argv[1:], "t:np:")

    models_set = (
        'LinearSVC', 'MultinomialNB',
        'RandomForest', 'LogisticRegression'
        )

    classifier = TextClassifier()

    models_map = {
        'LinearSVC': classifier.LINEAR_SVC,
        'MultinomialNB': classifier.MULTINOMIAL_NB,
        'RandomForest': classifier.RANDOM_FOREST,
        'LogisticRegression': classifier.LOGISTIC_REGRESSION
    }

    for opt, value in optlist:
        if opt == '-t':
            if value in models_set:
                logging.info("Training model with {}".format(value))
                classifier.train(models_map[value])
            else:
                print("Model {} doesn't exist".format(value))
        elif opt == '-p':
            print(classifier.predict(value))
        elif opt == '-n':
            print(classifier.get_classifier_name)
