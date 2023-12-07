from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from flair.models import TextClassifier
from flair.data import Sentence


stemmer = EnglishStemmer()
sia = TextClassifier.load('en-sentiment')


def smart_tokenize_and_preprocess(text):
    words = word_tokenize(text)
    result = [stemmer.stem(token.lower()) for token in words]
    return result


def flair_prediction(x):
    # x = smart_tokenize_and_preprocess(x)
    sentence = Sentence(x)
    sia.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
        return "POSITIVE"
    elif "NEGATIVE" in str(score):
        return "NEGATIVE"
    else:
        return "NEUTRAL"