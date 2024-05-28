# english_functions.py
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import gensim
from gensim.models import Word2Vec

eng_model_filename = "/Users/kasikan/Documents/librarybot_project/Test/eng_model.model"
eng_model = gensim.models.Word2Vec.load(eng_model_filename)

def english_tokenizer(text):
    english_stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens_without_stopwords = [word for word in tokens if word.lower() not in english_stop_words]
    return tokens_without_stopwords

def english_shorten_question(question):
    shorten_words = ["please", "could", "you", "please", "may", "i"]
    for word in shorten_words:
        question = question.replace(word, '')
    return question

def english_get_similar_words(word):
    similar_words = []
    try:
        similar_words = eng_model.wv.most_similar(word)
    except KeyError:
        pass
    return similar_words
