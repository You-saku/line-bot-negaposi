from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import message as mess


app = Flask(__name__)

#os.environ -> 環境変数からもってくる　アクセストークンの記述の必要なし
#結構メジャーなやり方
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


'''
@app.route("/hello")
def hello():
    return "Hello Flask"
'''

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    responce = mess.kusoripu()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=responce))


if __name__ == "__main__":
    port = int(os.getenv("PORT",5000))#os.getenv -> 環境変数の数字を取得　引数2つめのおかげで仮に環境変数がヒットしなくてもその引数を設定してくれる
    app.run(host="0.0.0.0",port=port)