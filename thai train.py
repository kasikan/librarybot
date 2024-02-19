import multiprocessing
import mysql.connector
from pythainlp import word_tokenize
from gensim.models import Word2Vec

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="linebot"  # Remove the space in "linebot"
)
cursor = connection.cursor()

# Fetch questions from the database
query = "SELECT question FROM questionanswer"
cursor.execute(query)
result = cursor.fetchall()
questions = [row[0] for row in result]

# Function to preprocess text
def preprocess_text(text):
    tokens = word_tokenize(text, keep_whitespace=False)
    return tokens

# Preprocess questions
processed_questions = [preprocess_text(question) for question in questions]

# Configure Word2Vec parameters
model_size = 100  # You can adjust this based on your needs
window_size = 5
min_count = 1
workers = multiprocessing.cpu_count()

# Train the Word2Vec model
word2vec_model = Word2Vec(
    processed_questions,
    vector_size=model_size,
    window=window_size,
    min_count=min_count,
    workers=workers
)

# Save the trained model to a file
model_filename = "word2vecTH_model.model"
word2vec_model.save(model_filename)

# Close MySQL connection
cursor.close()
connection.close()
