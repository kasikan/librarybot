import mysql.connector
import multiprocessing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec

# Replace 'your_username', 'your_password', and 'your_database' with your actual MySQL credentials
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="linebot"  # Remove the space in " linebot"
)
cursor = connection.cursor()
query = "SELECT * FROM questionanswer"
cursor.execute(query)

# Fetch all the rows
result = cursor.fetchall()

# Extract questions from the fetched data
questions = [row[0] for row in result]

# Preprocess data - Tokenize, clean text, and remove stop words
def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text, language='th')  # Use 'th' for Thai language
    
    # Remove punctuation and convert to lowercase
    tokens = [word.lower() for word in tokens if word.isalpha()]
    
    # Remove stop words
    stop_words = set(stopwords.words('thai'))
    tokens = [word for word in tokens if word not in stop_words]
    
    return tokens

# Apply preprocessing to all questions
processed_questions = [preprocess_text(question) for question in questions]

# Train Word2Vec Model
# Define Word2Vec model parameters
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
model_filename = "word2vec_model.bin"
word2vec_model.save(model_filename)

# Close MySQL connection
cursor.close()
connection.close()
