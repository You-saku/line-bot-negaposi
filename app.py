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
from janome.tokenizer import Tokenizer
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
    elif len(text) > 10 and len(text) < 40:
        token = t.tokenize(text,wakati=True)

        #ネガポジカウンター
        pn = {'p':0,'n':0,'e':0}

        for i,word in enumerate(token):
            #まず最初に辞書にあるか否かチェック
            try:
                checker = np_dic[word]
            except KeyError:
                continue

            if checker=='p':
                pn["p"]+=1
            elif checker=="n":
                pn["n"]+=1
            elif checker=="e":
                pn["e"]+=1
            #print("{}文字目 : {}".format(i,word))

        max_key,max_value = max(pn.items(),key=lambda x:x[1])
        
        if max_value >= 5 and max_key == 'p':
            responce = "めっちゃポジティブだねぇ!!"
        elif max_value >= 5 and max_key == 'n':
            responce = "めっちゃネガティブだねぇ!!"
        elif max_value >= 5 and max_key == 'e':
            responce = "感情が普通らしいぞ もっと感情揺さぶられる体験をしろ!!"
        else:
            responce = "とにかく言うことはない。そのままの君でいてくれ"

        #pythonの改行コードは [\n]
        #licence = "『小林のぞみ，乾健太郎，松本裕治，立石健二，福島俊一. 意見抽出のための評価表現の収集. 自然言語処理，Vol.12, No.3, pp.203-222, 2005. / Nozomi Kobayashi, Kentaro Inui, Yuji Matsumoto, Kenji Tateishi. Collecting Evaluative Expressions for Opinion Extraction, Journal of Natural Language Processing 12(3), 203-222, 2005.』参照"
        licence = "https://ci.nii.ac.jp/naid/130004291853\n参照"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ネガポジ判別結果\n"+responce))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=licence))
    else:
        responce = "大丈夫だよ。\nそんな短い文章送ってくるならまだ余裕がある証拠だ。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=responce))

if __name__ == "__main__":
    t = Tokenizer()
    np_dic = np.dict_init()
    port = int(os.getenv("PORT",5000))#os.getenv -> 環境変数の数字を取得　引数2つめのおかげで仮に環境変数がヒットしなくてもその引数を設定してくれる
    #0.0.0.0 = どこからでも通信可能なやつ
    app.run(host="0.0.0.0",port=port)