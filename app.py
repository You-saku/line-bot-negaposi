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

from packages import message as mess
from packages import negaposi as np
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
    if len(text) >= 45:
        responce = "文字が長すぎるよ\n30文字くらいで会話しようぜ処理できないよ"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=responce))

    elif len(text) > 10 and len(text) > 40:
        responce = np.negaposi_check(text)
        #pythonの改行コードは [\n]
        cresit = "\n\n『小林のぞみ，乾健太郎，松本裕治，立石健二，福島俊一. 意見抽出のための評価表現の収集. 自然言語処理，Vol.12, No.3, pp.203-222, 2005. / Nozomi Kobayashi, Kentaro Inui, Yuji Matsumoto, Kenji Tateishi. Collecting Evaluative Expressions for Opinion Extraction, Journal of Natural Language Processing 12(3), 203-222, 2005.』参照"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ネガポジ判別結果\n"+responce+cresit))
    else:
        responce = "大丈夫だよ。\nそんな短い文章送ってくるならまだ余裕がある証拠だ。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=responce))


if __name__ == "__main__":
    port = int(os.getenv("PORT",5000))#os.getenv -> 環境変数の数字を取得　引数2つめのおかげで仮に環境変数がヒットしなくてもその引数を設定してくれる
    #0.0.0.0 = どこからでも通信可能なやつ
    app.run(host="0.0.0.0",port=port)