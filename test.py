from gensim.models import Word2Vec
import gensim
import mysql.connector
import pandas as pd
from pythainlp import word_tokenize
from pythainlp.util import isthai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Search for a word 
WordSearch = "็How many books can I borrow? and how many days? "


# Load the Word2Vec model from Wikipedia corpus
wiki_model_filename = "wiki.th.text.model"
wiki_model = gensim.models.Word2Vec.load(wiki_model_filename)

# Load the Word2Vec model from database
database_model_filename = "word2vecTH_model.model"
database_model = Word2Vec.load(database_model_filename)

ThaiQA = "ThaiQA.model"
ThaiQA_model = gensim.models.Word2Vec.load(ThaiQA)



# Load the Word2Vec model from database
database_model_filename = "word2vecTH_model.model"
database_model = Word2Vec.load(database_model_filename)



# Check if a word is in Thai
def is_thai(Word):
    return all(isthai(c) for c in Word)


def search_similar_from_database(word):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="linebot"  # Remove the space in "linebot"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Tokenize and preprocess the input word
            tokens = word_tokenize(word, engine='newmm')
            preprocessed_word = ' '.join(tokens)

            # Vectorize the preprocessed word using TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform([preprocessed_word])

            # Check if the input word is in Thai
            if is_thai(word):
                question_column = "question"
                answer_column = "answer"
            else:
                question_column = "question_en"
                answer_column = "answer_en"

            # Retrieve questions from database
            query = f"SELECT {question_column}, {answer_column} FROM questionanswer"
            cursor.execute(query)
            questions = cursor.fetchall()

            best_similarity = -1  # Initialize best similarity score
            best_answer = None

            if questions:
                print("Similar answers found in database:")
                for question, answer in questions:
                    # Preprocess and tokenize the question
                    question_tokens = word_tokenize(question, engine='newmm')
                    preprocessed_question = ' '.join(question_tokens)

                    # Vectorize the preprocessed question using TF-IDF
                    question_vector = tfidf_vectorizer.transform([preprocessed_question])

                    # Calculate cosine similarity between input word vector and question vector
                    similarity = cosine_similarity(tfidf_matrix, question_vector)

                    # Update best similarity and corresponding answer
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_answer = answer

                # Print the best answer
                if best_answer:
                    print(WordSearch)
                    print("Best Answer:", best_answer)
                else:
                    print(f"No similar answers found for '{word}' in the database.")
            else:
                print(f"No similar answers found for '{word}' in the database.")
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Set the threshold for similarity
threshold = 0.5

# Call the function
search_similar_from_database(WordSearch)
