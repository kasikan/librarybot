from gensim.models import Word2Vec
import gensim
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from pythainlp import word_tokenize
from pythainlp.util import isthai

app = Flask(__name__)

line_bot_api = LineBotApi('ETbJGvEZK098id/U/FnX1KZxZQE7Ihn4HP4/OmuTeKd5hnYEc7zdydJIUW52tXqJalpgfk+eI1qSmGg8FzFAACu+6KSsMF3SnnSP+EfCxiyMpvDyRiY3jX87z7vznFL0A93TbTEZwG1Fwnzeqyfk+AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e0f2290c36e6036b32156d6b90b09ef3')

# Load the Word2Vec model from Wikipedia corpus
wiki_model_filename = "wiki.th.text.model"
wiki_model = gensim.models.Word2Vec.load(wiki_model_filename)

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
                    print("Best Answer:", best_answer)
                    return best_answer  # Return the best answer
                else:
                    print(f"No similar answers found for '{word}' in the database.")
                    return None  # Return None if no answer is found
            else:
                print(f"No similar answers found for '{word}' in the database.")
                return None  # Return None if no answer is found
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table:", e)
        return None  # Return None if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    response = search_similar_from_database(user_message)
    if response:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="No similar answer found."))

if __name__ == "__main__":
    app.run(port=8080,debug=True)
