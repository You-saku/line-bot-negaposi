def create_response(request_message, sentiment):
    if len(request_message) >= 300:
        return "文字が長すぎるよ\n落ち着こうぜ一回"
    elif len(request_message) > 10 and len(request_message) < 300:
        if sentiment == 'POSITIVE':
            return "ポジティブだな\nそのままでOK"
        elif sentiment == 'NEGATIVE':
            return 'ネガティブだな\n根詰めると死ぬぞ'
        elif sentiment == 'MIXED':
            return "頭の中カオスじゃん\n寝ろ"
        else:
            return "特に言うことはない。今のままでいてくれよな"
    else:
        return "短い文章送ってくるな\n暇なのか？"
