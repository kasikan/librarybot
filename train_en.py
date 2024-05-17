from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
import multiprocessing
import os

def english_preprocess_text(text):
    tokens = word_tokenize(text)
    english_stopwords = set(nltk_stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in english_stopwords]
    return tokens

def read_input_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    preprocessed_sentences = [english_preprocess_text(line) for line in lines]
    return preprocessed_sentences

if __name__ == '__main__':
    folder_path = r'C:\Users\kanka\Downloads\test\text\coca-samples-text'
    file_names = os.listdir(folder_path)
    file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]

    sentences = []
    for file_path in file_paths:
        sentences.extend(read_input_text(file_path))

    model = Word2Vec(sentences, vector_size=400, window=5, min_count=5, workers=multiprocessing.cpu_count())
    model.save('output_model.model')

