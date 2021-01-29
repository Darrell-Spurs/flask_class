# 運行以下程式需安裝模組: line-bot-sdk, flask, pyquery, firebase-admin

# 引入flask模組
from flask import Flask, request, abort
# 引入linebot相關模組
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

# 處理器請參閱以下網址的 Message objects 章節
# https://github.com/line/line-bot-sdk-python
from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, StickerSendMessage, LocationSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction, CarouselTemplate, CarouselColumn
)

# 引用股價查詢函數
from modules.stock import get_stock_info
# 引用常用回應與主選單
from modules.reply import faq, menu, get_stock_flex
# 引用時間模組
import time

# 定義應用程式是一個Flask類別產生的實例
app = Flask(__name__)

# LINE的Webhook為了辨識開發者身份所需的資料
# 相關訊息進入網址(https://developers.line.me/console/)
CHANNEL_ACCESS_TOKEN = 'UygZoxj63ijgPHyWk1ZdhPNZz5vTaJK8i4THTNOdmLibDW9UKKwUoTugUoSJp10Zz4eP+twwdeu1OT7Ci6aLtOtC9oP5zCZ0GE9iXTg+0UVei8SIvD8az2R+gARKajxUEdsjgdLpI4yL1zOdVc2xIgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '1f6a5a42b19004c7bc1aeb76cc9097c5'

# *********** 以下為 X-LINE-SIGNATURE 驗證程序 ***********
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/", methods=['POST'])
def callback():
    # 當LINE發送訊息給機器人時，從header取得 X-Line-Signature
    # X-Line-Signature 用於驗證頻道是否合法
    signature = request.headers['X-Line-Signature']

    # 將取得到的body內容轉換為文字處理
    body = request.get_data(as_text=True)

    # 一但驗證合法後，將body內容傳至handler
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('[X-Line-Signature 驗證失敗]')
        abort(400)

    return 'OK'
# *********** 以上為 X-LINE-SIGNATURE 驗證程序 ***********


# 文字訊息傳入時的處理器
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當有文字訊息傳入時
    # event.message.text : 使用者輸入的訊息內容
    print('*'*40)
    print('[使用者傳入文字訊息]')
    # print(str(event))
    # 使用者說的文字
    user_msg = event.message.text
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    print("[profile]",profile.display_name)

    reply = menu
    if user_msg in faq:
        reply = faq[user_msg]
    else:
        data = get_stock_info(user_msg)
        # if data got
        if data["is_success"]:
            reply = get_stock_flex(data)

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
    reply = TextSendMessage("把我踢掉啦")
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        reply)


import os
if __name__ == "__main__":
    print('[伺服器開始運行]')
    port = int(os.environ.get('PORT', 5500))
    # 使app開始在此連接端口上運行
    print('[Flask運行於連接端口:{}]'.format(port))
    # 本機測試使用127.0.0.1, debug=True
    # Heroku部署使用 0.0.0.0
    app.run(host='127.0.0.1', port=port, debug=True)
