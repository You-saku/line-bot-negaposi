import aws
import config
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
import message
import os

app = Flask(__name__)

#os.environ -> 環境変数からもってくる
line_bot_api = LineBotApi(config.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.YOUR_CHANNEL_SECRET)

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
    request_message = event.message.text
    result = aws.detect_emotion(request_message)

    response_message = message.create_response(request_message, result['Sentiment'])
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_message)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT",8000))#os.getenv -> 環境変数の数字を取得　引数2つめのおかげで仮に環境変数がヒットしなくてもその引数を設定してくれる
    #0.0.0.0 = どこからでも通信可能なやつ
    app.run(host="0.0.0.0",port=port)
