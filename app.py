# import flask/ line modules
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, StickerMessage,
    TextSendMessage, StickerSendMessage, LocationSendMessage,
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate,
    PostbackAction, MessageAction, URIAction, CarouselTemplate,
    CarouselColumn
)
# Doc link https://github.com/line/line-bot-sdk-python

from modules.stock import get_stock_info
from modules.reply import youtube_menu, get_stock_flex, ReplyActions, get_route
from modules.test import sel_test
import time

app = Flask(__name__)

# LINE Webhook Auth -- (https://developers.line.me/console/)
CHANNEL_ACCESS_TOKEN = 'UygZoxj63ijgPHyWk1ZdhPNZz5vTaJK8i4THTNOdmLibDW9UKKwUoTugUoSJp10Zz4eP+twwdeu1OT7Ci6aLtOtC9oP5zCZ0GE9iXTg+0UVei8SIvD8az2R+gARKajxUEdsjgdLpI4yL1zOdVc2xIgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '1f6a5a42b19004c7bc1aeb76cc9097c5'

# X-LINE-SIGNATURE Auth - Check if channel is valid
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# just test
@app.route("/seltest")
def testtest():
    return sel_test

# post to handlers
@app.route("/", methods=['POST'])
def callback():
    # Get X-Line-Signature from header when Line bot received a message
    signature = request.headers['X-Line-Signature']

    # convert body to text
    body = request.get_data(as_text=True)

    # send body text to handler
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('[X-Line-Signature Auth Failed]')
        abort(400)
    return 'OK'

# Send text to handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當有文字訊息傳入時
    # event.message.text : 使用者輸入的訊息內容
    print('-'*40)
    # print(str(event))

    # 使用者說的文字
    user_msg = event.message.text
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    print("[profile]",profile.display_name)
    print("[message]",user_msg)

    reply_actions = ReplyActions()
    reply = None
    if user_msg.capitalize() == "Intro":
        reply = youtube_menu
    elif user_msg == "test":
        reply = get_route("松山圖書館", "台北101")
    # check if the prefix is in actions
    elif user_msg[:user_msg.find(" ")].capitalize() in reply_actions.actions:
        # get action type
        action = user_msg[:user_msg.find(" ")].capitalize()
        # get what the user want to send out
        user_msg_par = user_msg[user_msg.find(" ")+1:]
        # pass to the instance user's message and action and receive reply
        reply = reply_actions.get_user_msg_par_action(user_msg_par, action)
    else:
        data = get_stock_info(user_msg)
        # if data got
        if data["is_success"]:
            reply = get_stock_flex(data)
    if reply:
        line_bot_api.reply_message(
            event.reply_token,
            reply)

    # else:
    #     reply = menu

    # 回傳訊息


# 貼圖訊息傳入時的處理器
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # 當有貼圖訊息傳入時
    print('*'*40)
    print('[使用者傳入貼圖訊息]')
    print(str(event))

    # 準備要回傳的貼圖訊息
    # TODO: 機器人可用的貼圖 https://devdocs.line.me/files/sticker_list.pdf
    # reply = StickerSendMessage(package_id='2', sticker_id='149')
    # # 回傳訊息
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     reply)


import os
if __name__ == "__main__":
    print('[伺服器開始運行]')
    port = int(os.environ.get('PORT', 5500))
    # 使app開始在此連接端口上運行
    print('[Flask運行於連接端口:{}]'.format(port))
    # 本機測試使用127.0.0.1, debug=True
    # Heroku部署使用 0.0.0.0
    # app.run(host='127.0.0.1', port=port, debug=True)
    app.run(host='0.0.0.0', port=port, debug=True)
