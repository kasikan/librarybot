import multiprocessing
import mysql.connector
import nltk
from nltk.corpus import stopwords
from pythainlp import word_tokenize
from gensim.models import Word2Vec
from gensim.parsing.preprocessing import remove_stopwords
from pythainlp.corpus import thai_stopwords
import re


# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="linebot"  # Remove the space in "linebot"
)
cursor = connection.cursor()

# Fetch questions from the database
query = "SELECT * FROM questionanswer"
cursor.execute(query)
result = cursor.fetchall()
 

def preprocess_text(text_tuple):
    processed_texts = []
    for text in text_tuple:
        # Remove stop words and tokenize each text in the tuple
  
        tokens = remove_stopwords(text)
        tokens = word_tokenize(tokens, engine="longest",keep_whitespace=False)

        # อ่านไฟล์ข้อความที่มีคำที่ต้องการเพิ่ม
        additional_stopwords_path = "C:/Users/kanka/Downloads/test/additional_stopwords.txt"
        with open(additional_stopwords_path, "r", encoding="utf-8") as file:
            additional_stopwords = file.read().splitlines()
        
        # เพิ่มคำที่ต้องการเพิ่มลงในคำหยุด
        thai_stopwords_list = list(thai_stopwords())
        thai_stopwords_list.extend(additional_stopwords)
        
        tokens = [i for i in tokens if i not in thai_stopwords_list]

        english_stopwords = set(stopwords.words('english'))
        tokens = [token for token in tokens if token.lower() not in english_stopwords]
        processed_texts.append(tokens)
        #print(english_stopwords)

    return processed_texts

# Preprocess questions
processed_questions = []
for question in result:
    processed_texts = preprocess_text(question)
    processed_questions.extend(processed_texts)
#    print(processed_texts)

# Define the Regex pattern to remove unwanted characters
pattern = r'[?() ./:=://"\-\s’ & ; % @ .]+'
double = re.sub(r'(.)\1+', r'\1','')

# Iterate over the processed questions and remove unwanted characters
for i, question in enumerate(processed_questions):
    processed_questions[i] = [re.sub(pattern, '', word) for word in question]
   

# Print the preprocessed questions to verify the results
for question in processed_questions:
    print(question)

# Configure Word2Vec parameters
model_size = 400  # You can adjust this based on your needs
window_size = 20
min_count = 30
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

vector_filename = "word2vecTH_model.vector"
word2vec_model.wv.save_word2vec_format(vector_filename, binary=False)

# Close MySQL connection
cursor.close()
connection.close()
