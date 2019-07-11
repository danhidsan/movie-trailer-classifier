import pickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def load_model(model_path: str, vocab_path: str):
    model = pickle.load(open(model_path, 'rb'))
    vocabulary = pickle.load(open(vocab_path, 'rb'))

    count_vect = CountVectorizer(vocabulary=vocabulary)
    count_vect._validate_vocabulary()

    tf_idf_transformer = TfidfTransformer()

    return count_vect, tf_idf_transformer, model


def predict(text: str):

    count_vect, tf_idf_transformer, model = load_model(
        'ml/train/model.pickle', 'ml/train/vocab.pickle'
    )

    X_new_counts = count_vect.transform([text])
    X_new_tf_idf = tf_idf_transformer.fit_transform(X_new_counts)

    prediction = model.predict(X_new_tf_idf)

    return prediction

model = pickle.load('ml/train/model.pickel')

prediction = predict('Hector Babenco think Beth stand anymore Matt Beth Beth glad finally return don sound self righteous return call mad talk share responsibility know Beth Beth scream scream know sort gutless wonder argue embarrass able kid Beth listen wait second listen know long Beth know exactly long feel strange hell choice break dry spell life problem know problem place year old time job right scared try particularly try particularly thank daughter way Beth look let tell Beth mind kind work work embarrass pep talk Popcorn Pictures truck ridiculous Lexus Lexus nut today Cathy Matt Hobbs Cathy remember minute know Shannon refer people Development Executives easy way remember want know Matt Hobbs Matt Hobbs Matt Hobbs re dull guy Redford play natural Roy Hobbs Matt Hobbs cautiously enthusiastic figure finish script evaluation Matt good good time time night act school Matt actually know start hurry audition today problem later thank interrupt script awful title little dick mean thing story story story story love right problem little garbagey cast right Cathy know smash Popcorn Pictures hold recommend sorry available understand interrupt check soon number know sure remember let help stop good favor fresh slant list promise Claire Matt Hobbs Claire good meet George LaForest Harry seat thank Matt Hobbs John Earl McAlpine director good meet Burke Adler')
print(prediction)