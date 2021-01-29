from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction, CarouselTemplate, CarouselColumn, QuickReply, QuickReplyButton, FlexSendMessage
)
# LINE所支援的回覆格式可參考官方文件內的 Message Object章節
# https://github.com/line/line-bot-sdk-python


faq = {
    '捷運':TextSendMessage(
        text="metro"
    ),
    '貼圖': StickerSendMessage(
        package_id='1',
        sticker_id='1'
    ),
    '照片': ImageSendMessage(
        original_content_url='https://picsum.photos/900/400',
        preview_image_url='https://picsum.photos/900/400'
    ),
    '電話': TextSendMessage(text='0912-345-678'),
    '交通': TextSendMessage(text='請問您想使用何種方式前往？',
                          quick_reply=QuickReply(items=[
                              QuickReplyButton(action=MessageAction(
                                  label="搭乘捷運", text="捷運")
                              ),
                              QuickReplyButton(action=MessageAction(
                                  label="搭乘公車", text="公車")
                              )
                          ])
                          ),
}

# 主選單
menu = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            # 卡片一
            CarouselColumn(
                # 卡片一圖片網址
                thumbnail_image_url='https://picsum.photos/id/1/900/400',
                title='卡片一標題',
                text='內文一',
                actions=[
                    MessageAction(
                        label='台積電(2330)',
                        text='2330'
                    ),
                    MessageAction(
                        label='中華電(2412)',
                        text='2412'
                    ),
                    MessageAction(
                        label='鴻海(2317)',
                        text='2317'
                    )
                ]
            ),
            # 卡片二
            CarouselColumn(
                # 卡片二圖片網址
                thumbnail_image_url='https://picsum.photos/id/2/900/400',
                title='卡片二標題',
                text='內文二',
                actions=[
                    MessageAction(
                        label='兆豐金(2886)',
                        text='2886'
                    ),
                    MessageAction(
                        label='玉山金(2884)',
                        text='2884'
                    ),
                    MessageAction(
                        label='中信金(2891)',
                        text='2891'
                    )
                ]
            ),
            CarouselColumn(
                # 卡片二圖片網址
                thumbnail_image_url='https://picsum.photos/id/2/900/400',
                title='Functions',
                text='What do you wanna do?',
                actions=[
                    MessageAction(
                        label='Transportation',
                        text='交通'
                    ),
                    MessageAction(
                        label='Photo',
                        text='照片'
                    ),
                    MessageAction(
                        label='Sticker',
                        text='貼圖'
                    )
                ]
            )
        ]
    )
)

def get_stock_flex(stock):
    fsm =  FlexSendMessage(
        alt_text="Ur Device Doens't support this type of Message",
        contents= {
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "STOCKS",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                  },
                  {
                    "type": "text",
                    "text": stock['report']['name'],
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": True,
                    "text": " "
                  },
                  {
                    "type": "separator",
                    "margin": "xs"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "text",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                            "text": "資料時間"
                          },
                          {
                            "type": "text",
                            "text": stock['report']['updated_at'],
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                          }
                        ]
                      },
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "text",
                            "text": " ",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                          },
                          {
                            "type": "text",
                            "text": " ",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                          }
                        ]
                      },
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "text",
                            "text": " ",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                          },
                          {
                            "type": "text",
                            "text": " ",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                          }
                        ]
                      },
                      {
                        "type": "separator",
                        "margin": "xxl"
                      },
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "xxl",
                        "contents": [
                          {
                            "type": "text",
                            "text": "成交價",
                            "size": "sm",
                            "color": "#555555"
                          },
                          {
                            "type": "text",
                            "text": f"${stock['report']['price']}",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                          }
                        ]
                      },
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "text",
                            "text": "買價",
                            "size": "sm",
                            "color": "#555555"
                          },
                          {
                            "type": "text",
                            "text": f"${stock['report']['bid']}",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                          }
                        ]
                      },
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "text",
                            "text": "賣價",
                            "size": "sm",
                            "color": "#555555"
                          },
                          {
                            "type": "text",
                            "text": f"${stock['report']['offer']}",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                          }
                        ]
                      },
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "text",
                            "text": " ",
                            "size": "sm",
                            "color": "#555555"
                          },
                          {
                            "type": "text",
                            "text": " ",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "separator",
                    "margin": "xxl"
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "Source",
                        "size": "xs",
                        "color": "#aaaaaa",
                        "flex": 0
                      },
                      {
                        "type": "text",
                        "text": "Yahoo Stocks",
                        "color": "#aaaaaa",
                        "size": "xs",
                        "align": "end"
                      }
                    ]
                  }
                ]
              },
              "styles": {
                "footer": {
                  "separator": True
                }
              }
            }
    )
    return fsm