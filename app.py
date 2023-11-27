from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ใส่ Channel Access Token และ Channel Secret ของคุณที่ได้จาก LINE Developers Console
channel_access_token = 'ETbJGvEZK098id/U/FnX1KZxZQE7Ihn4HP4/OmuTeKd5hnYEc7zdydJIUW52tXqJalpgfk+eI1qSmGg8FzFAACu+6KSsMF3SnnSP+EfCxiyMpvDyRiY3jX87z7vznFL0A93TbTEZwG1Fwnzeqyfk+AdB04t89/1O/w1cDnyilFU='
channel_secret = 'e0f2290c36e6036b32156d6b90b09ef3'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_token = event.reply_token
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

if __name__ == "__main__":
    app.run(port=5000)

@app.route("/callback", methods=["GET"])
def verify():
    return request.args.get("hub.challenge")
