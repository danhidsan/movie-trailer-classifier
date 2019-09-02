import unittest
import time
import logging

from ml.classifier import TextClassifier

# logging config
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class ClassifierTest(unittest.TestCase):

    logging.info("Preparing set up test for Classifier Module")

    def setUp(self):
        self.classifier = TextClassifier()

    def test_get_classifier_name(self):
        logging.info("Get classifier name test")
        names_list = [
            'MultinomialNB', 'LinearSVC',
            'LogisticRegression', 'RandomForestClassifier'
            ]

        model_name = self.classifier.get_classifier_name
        self.assertTrue(model_name in names_list)

    def test_train(self):
        logging.info("Train model test")
        # train model with wrong model
        self.assertRaises(
            AttributeError, self.classifier.train, 'WrongModel'
            )

        # train model with correct model
        self.classifier.train('get_linear_svc')
        model_name = self.classifier.get_classifier_name
        self.assertEqual(model_name, 'LinearSVC')

    def test_predict(self):
        logging.info("Predict text test")
        prediction = self.classifier.predict(
            """It is a curious thing, Harry, but perhaps those who
                are best suited to power are those who have never sought it."""
            )

        self.assertTrue(len(prediction) == 1)

if __name__ == '__main__':
    unittest.main()
