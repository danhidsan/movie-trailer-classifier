import unittest
import time

from ml.classifier import TextClassifier


class ClassifierTest(unittest.TestCase):

    def setUp(self):
        self.classifier = TextClassifier()

    def test_get_classifier_name(self):

        names_list = [
            'MultinomialNB', 'LinearSVC',
            'LogisticRegression', 'RandomForestClassifier'
            ]

        model_name = self.classifier.get_classifier_name
        self.assertTrue(model_name in names_list)

    def test_train(self):

        # train model with wrong model
        self.assertRaises(
            AttributeError, self.classifier.train, 'WrongModel'
            )

        # train model with correct model
        self.classifier.train('get_linear_svc')
        model_name = self.classifier.get_classifier_name
        self.assertEqual(model_name, 'LinearSVC')
    
    def test_predict(self):
        prediction = self.classifier.predict(
            """It is a curious thing, Harry, but perhaps those who
                are best suited to power are those who have never sought it."""
            )

        self.assertTrue(len(prediction) == 1)

if __name__ == '__main__':
    unittest.main()
