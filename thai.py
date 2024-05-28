# thai_functions.py
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
import gensim
from gensim.models import Word2Vec

# Load the Word2Vec model from database
database_model_filename = "/Users/kasikan/Documents/librarybot_project/Test/wiki.th.text.model"
database_model = Word2Vec.load(database_model_filename)

def thai_tokenizer(text):
    tokens = word_tokenize(text)
    tokens_without_stopwords = [word for word in tokens if word not in thai_stopwords()]
    return tokens_without_stopwords


def thai_shorten_question(question):
    shorten_words = ["ค่ะ", "ครับ", "คะ"]
    for word in shorten_words:
        question = question.replace(word, '')
    question = question.replace(".", "")
    question = question.replace(" ", "")
    return question
    
def thai_get_similar_words(word):
    similar_words = []
    try:
        similar_words = database_model.wv.most_similar(word)
    except KeyError:
        pass
    return similar_words
