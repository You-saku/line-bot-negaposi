# LINE_BOT_NEGAPOSI

## Summary
普通のLINE Botです。感情分析を入れた

## Use
 * Python(Flask)
 * AWS Comprehend
 * LINE Messaging API

## Requirement
 * Python3
 * pip
 * AWS Account
 * LINE Messaging API

## Setup
1. clone
2. cd LINE_BOT_NEGAPOSI
3. cp .env.example .env
4. setup venv
5. setup LINE Messaging API
6. set .env VALUE
7. python3 -m pip install -r requirements.txt
8. setup ngrok ```ngrok http 8000```
9. python3 app.py

## Tips
 * [Messaging API](https://developers.line.biz/ja/docs/messaging-api/)
 * [ngrok](https://ngrok.com/)
 * [venv](https://camp.trainocate.co.jp/magazine/venv-python/)
