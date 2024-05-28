# main.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import StickerMessage
import mysql.connector
from thai import thai_tokenizer, thai_shorten_question
from eng  import english_tokenizer, english_shorten_question
from thai import thai_get_similar_words
from eng  import english_get_similar_words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

line_bot_api = LineBotApi('ETbJGvEZK098id/U/FnX1KZxZQE7Ihn4HP4/OmuTeKd5hnYEc7zdydJIUW52tXqJalpgfk+eI1qSmGg8FzFAACu+6KSsMF3SnnSP+EfCxiyMpvDyRiY3jX87z7vznFL0A93TbTEZwG1Fwnzeqyfk+AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e0f2290c36e6036b32156d6b90b09ef3')

def load_data_from_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="linebot"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT question, question_en, answer, answer_en FROM questionanswer")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def find_similar_answer(input_text, data, tfidf_vectorizer_thai, tfidf_matrix_thai, tfidf_vectorizer_eng, tfidf_matrix_eng):
    input_text_thai = thai_shorten_question(input_text)
    input_text_eng = english_shorten_question(input_text)
               
    similar_words_thai = thai_get_similar_words(input_text_thai)
    similar_words_eng = english_get_similar_words(input_text_eng)
    
    input_vector_thai = tfidf_vectorizer_thai.transform([input_text_thai])
    input_vector_eng = tfidf_vectorizer_eng.transform([input_text_eng])
    
    cosine_similarities_thai = cosine_similarity(input_vector_thai, tfidf_matrix_thai)
    max_sim_index_thai = cosine_similarities_thai.argmax()

    cosine_similarities_eng = cosine_similarity(input_vector_eng, tfidf_matrix_eng)
    max_sim_index_eng = cosine_similarities_eng.argmax()

    if cosine_similarities_thai[0, max_sim_index_thai] > cosine_similarities_eng[0, max_sim_index_eng]:  
        if cosine_similarities_thai[0, max_sim_index_thai] > 0.5: 
            return data[max_sim_index_thai][2]  
    else:
        if cosine_similarities_eng[0, max_sim_index_eng] > 0.5:  
            return data[max_sim_index_eng][3]  

    return "ขอโทษครับ/ค่ะ ไม่พบข้อมูลใกล้เคียง"

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



@handler.add(MessageEvent, message=(TextMessage, StickerMessage))
def handle_message(event):
    if isinstance(event.message, StickerMessage):
        reply_text = "สวัสดีค่ะ ModLibrary ยินดีให้บริการค่ะ สอบถามเรื่องอะไรคะ"
    else:
        input_text = event.message.text

        # Check if input text is a greeting
        if input_text in ["สวัสดีคะ", "สวัสดีค่ะ", "สวัสดีครับ", "สวัสดีคับ"]:
            reply_text = "สวัสดีค่ะ ModLibrary ยินดีให้บริการค่ะ สอบถามเรื่องอะไรคะ"
        elif input_text in ["Hi", "Hello","hi","hello"]:
            reply_text = "Hello, ModLibrary is happy to serve you. What are you asking about?"
        else:
            data = load_data_from_database()
                
            tfidf_vectorizer_thai = TfidfVectorizer(tokenizer=thai_tokenizer)
            questions_thai = [item[0] for item in data]
            tfidf_matrix_thai = tfidf_vectorizer_thai.fit_transform(questions_thai)

            tfidf_vectorizer_eng = TfidfVectorizer(tokenizer=english_tokenizer)
            questions_eng = [item[1] for item in data]
            tfidf_matrix_eng = tfidf_vectorizer_eng.fit_transform(questions_eng)

            similar_answer = find_similar_answer(input_text, data, tfidf_vectorizer_thai, tfidf_matrix_thai, tfidf_vectorizer_eng, tfidf_matrix_eng)

            if similar_answer:
                reply_text = similar_answer
            else:
                reply_text = "ขอโทษครับ/ค่ะ ไม่พบข้อมูลใกล้เคียง"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(port=8080, debug=True)
