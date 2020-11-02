"""
AWS_ACCESS_KEY_ID=<aws-access-key>
AWS_SECRET_ACCESS_KEY=<aws-secret-access-key>
AWS_DEFAULT_REGION=<default-aws-region>
"""
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

import boto3
app = Flask(__name__)

#os.environ -> 環境変数からもってくる　アクセストークンの記述の必要なし
#結構メジャーなやり方
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

AWS_DEFAULT_REGION = os.environ["AWS_DEFAULT_REGION"]
language_code = "ja"

def detect_sentiment(text, language_code):
    comprehend = boto3.client('comprehend', region_name=AWS_DEFAULT_REGION)
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return response


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
        #webhookが正常ならば  handleに登録されている関数の実施を行う
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#イベントが発生した場合
#handleに付与する関数の記述
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #responce = mess.kusoripu()
    text = event.message.text
    if len(text) >= 300:
        responce = "文字が長すぎるよ\n落ち着こうぜ一回"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=responce))
    elif len(text) > 20 and len(text) < 300:
        result = detect_sentiment(text, language_code)
        responce = result['Sentiment']
        if responce == 'POSITIVE':
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ポジティブだね～\n何も悩みとかないの? 最高かよ!!!"))
        elif responce == 'NEGATIVE':
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='ネガティブになってるぞ。猫の画像見て元気だせよ\nあんま根詰めると死ぬぞ'))
        elif responce == 'MIXED':
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="今、君の頭の中カオスらしいぞ\nおかしくなる前に休んだりリフレッシュしような"))
        else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="特に言うことはない。今のままでいてくれよな"))
    else:
        responce = "大丈夫だよ。\nそんな短い文章送ってくるならまだ余裕がある証拠だ。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=responce))

if __name__ == "__main__":
    port = int(os.getenv("PORT",5000))#os.getenv -> 環境変数の数字を取得　引数2つめのおかげで仮に環境変数がヒットしなくてもその引数を設定してくれる
    #0.0.0.0 = どこからでも通信可能なやつ
    app.run(host="0.0.0.0",port=port)