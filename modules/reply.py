from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction, CarouselTemplate, CarouselColumn, QuickReply, QuickReplyButton, FlexSendMessage
)
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
import time
# https://github.com/line/line-bot-sdk-python

def lowerlize(string):
    return chr(ord(string[0])+32)+string[1:]

class ReplyActions:
    def __init__(self):
        self.user_msg_par = None
        self.actions = ["Search","Wiki",
                        "Channel","Latest",
                        "Location","Route"]
    def get_user_msg_par_action(self, msg, action):
        self.user_msg_par = msg
        func_name = lowerlize(action)+"_string"
        action_func = getattr(self,func_name)
        return action_func()
    def search_string(self):
        return TextSendMessage(
            text=f"https://www.google.com/search?q={self.user_msg_par.replace(' ','+')}"
        )
    def wiki_string(self):
        return TextSendMessage(
            text=f"https://en.wikipedia.org/wiki/{self.user_msg_par.replace(' ','_')}"
        )
    def channel_string(self):
        return TextSendMessage(
            text=self.get_channel(self.user_msg_par)
        )
    def latest_string(self):
        return TextSendMessage(
            text=self.get_latest(self.user_msg_par)
        )
    def location_string(self):
        return TextSendMessage(
            text=f"https://www.google.com.tw/maps/search/{self.user_msg_par}"
        )
    def route_string(self):
        start,end = self.user_msg_par.split("-")
        return TextSendMessage(
            text=f"https://www.google.com.tw/maps/dir/{quote(start)}/{quote(end)}"
        )

    def get_channel(self,keyword):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        url = f"https://www.youtube.com/results?search_query={quote(keyword)}"
        driver.get(url)
        driver.implicitly_wait(30)
        target = driver.find_elements_by_class_name("ytd-channel-renderer")
        for elem in target:
            if elem.get_attribute("href"):
                channel_link = elem.get_attribute("href")
                break
        driver.close()
        return channel_link
    def get_latest(self,keyword):

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        url = f"https://www.youtube.com/results?search_query={quote(keyword)}"
        driver.get(url)
        driver.implicitly_wait(30)
        target = driver.find_elements_by_class_name("ytd-channel-renderer")
        channel_link = None
        for elem in target:
            if elem.get_attribute("href"):
                channel_link = elem.get_attribute("href")
                break

        channel_videos = channel_link + "/videos"
        driver.get(channel_videos)
        links = driver.find_elements_by_id("video-title")

        return links[0].get_attribute("href")

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

youtube_menu = TemplateSendMessage(
    alt_text='Introduction',
    template=CarouselTemplate(
        columns=[
            # 卡片一
            CarouselColumn(
                # 卡片一圖片網址
                thumbnail_image_url='https://frankchiu.io/wp-content/uploads/2020/01/youtube_logo_dark.jpg',
                title='Introduction',
                text= "Find out what this chatbot can do for you!",
                actions=[
                    MessageAction(
                        label='Basic Functions',
                        text='Basic Functions'
                    ),
                    MessageAction(
                        label='Youtube Helper',
                        text='Youtube Helper'
                    ),
                    MessageAction(
                        label='Route Helper',
                        text='Route Helper'
                    ),
                ]
            ),
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


