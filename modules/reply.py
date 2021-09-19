from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction, CarouselTemplate, CarouselColumn, QuickReply, QuickReplyButton, FlexSendMessage
)
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
import time
import os
# https://github.com/line/line-bot-sdk-python

def lowerlize(string):
    return chr(ord(string[0])+32)+string[1:]

class ReplyActions:
    def __init__(self):
        self.user_msg_par = None
        self.actions = {"Search":"Enter keyword (e.g. LINE)",
                        "Wiki": "Enter keyword (e.g. Lionel Messi)",
                        "Wiki_zh": "輸入中文關鍵字 (e.g. 聊天機器人)",
                        "Channel": "Enter YouTube Channel (e.g. Drake)",
                        "Latest":"Enter YouTube Channel to get its latest video (e.g. Drake)",
                        "Location":"Enter a location to find it on Google Maps (e.g. Taipei 101)",
                        "Route":"Enter starting point and destination to find out the route on Google Maps (e.g. Taipei 101-Taipei Main Station)",
                        "Transit":"Enter starting point and destination to find out the fastest transit method (e.g. Taipei 101-Taipei Main Station)"}
    def intro_flex(self):
        return FlexSendMessage(
            alt_text="Not availabe on PC! Please check this on Mobile Device!",
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://insidesmallbusiness.com.au/wp-content/uploads/2019/05/bigstock-Target-Goal-Icon-Marketing-Ta-265891909.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                        "type": "uri",
                        "uri": "http://linecorp.com/"
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Introduction 💡",
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://insidesmallbusiness.com.au/wp-content/uploads/2019/05/bigstock-Target-Goal-Icon-Marketing-Ta-265891909.jpg"
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://insidesmallbusiness.com.au/wp-content/uploads/2019/05/bigstock-Target-Goal-Icon-Marketing-Ta-265891909.jpg"
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://insidesmallbusiness.com.au/wp-content/uploads/2019/05/bigstock-Target-Goal-Icon-Marketing-Ta-265891909.jpg"
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://insidesmallbusiness.com.au/wp-content/uploads/2019/05/bigstock-Target-Goal-Icon-Marketing-Ta-265891909.jpg"
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://insidesmallbusiness.com.au/wp-content/uploads/2019/05/bigstock-Target-Goal-Icon-Marketing-Ta-265891909.jpg"
                                },
                                {
                                    "type": "text",
                                    "text": "100.0",
                                    "size": "sm",
                                    "color": "#999999",
                                    "margin": "md",
                                    "flex": 0
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "What do you want do?",
                                            "wrap": True,
                                            "color": "#6600cc",
                                            "size": "sm"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Search 🔎",
                                "text": "Search"
                            },
                            "color": "#00001a"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Wiki 📃",
                                "text": "Wiki"
                            },
                            "color": "#00001a"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Wiki 中文📜",
                                "text": "Wiki_zh"
                            },
                            "color": "#00001a"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Channel 📺",
                                "text": "Channel"
                            },
                            "color": "#ff1a1a"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Latest ✨",
                                "text": "Latest"
                            },
                            "color": "#ff1a1a"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Location 📍",
                                "text": "Location"
                            },
                            "color": "#6495ED"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Route 🗺",
                                "text": "Route"
                            },
                            "color": "#6495ED"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "Transit ✈",
                                "text": "Transit"
                            },
                            "color": "#6495ED"
                        }
                    ],
                    "flex": 0
                }
            })
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
            text=f"https://en.wikipedia.org/w/index.php?search={self.user_msg_par.replace(' ','+')}&ns0=1"
        )
    def wiki_zh_string(self):
        return TextSendMessage(
            text=f"https://zh.wikipedia.org/w/index.php?search={quote(self.user_msg_par.replace(' ','+'))}&title=Special%3A%E6%90%9C%E7%B4%A2&go=%E5%9F%B7%E8%A1%8C&ns0=1"
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
            text=f"https://www.google.com.tw/maps/search/{self.user_msg_par}".replace(" ","+")
        )
    def route_string(self):
        start,end = self.user_msg_par.split("-")
        return TextSendMessage(
            text=f"https://www.google.com.tw/maps/dir/{quote(start)}/{quote(end)}".replace(" ","+")
        )
    def transit_string(self):
        start, end= self.user_msg_par.split("-")
        travel = self.get_transit(start, end)
        contents = {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "FROM",
                                "color": "#000000",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": start,
                                "color": "#004080",
                                "size": "xl",
                                "flex": 4,
                                "weight": "bold"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "TO",
                                "color": "#000000",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": end,
                                "color": "#004080",
                                "size": "xl",
                                "flex": 4,
                                "weight": "bold"
                            }
                        ]
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": "#cce6ff",
                "spacing": "md",
                "height": "154px",
                "paddingTop": "22px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"Duration: {travel[4]}",
                        "color": "#1aa3ff",
                        "size": "xs"
                    }
                ]
            }
        }

        ind=0
        for i in range(travel[1].count("->")+1):
            temp = ""
            while ind != len(travel[1]) and travel[1][ind] != "->":
                temp += (travel[1][ind] + " ")
                ind+=1
            else:
                ind += 1
            contents["body"]["contents"].extend([{
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "START" if i==0 else " ",
                                "size": "sm",
                                "gravity": "center",
                                "color": "#29a329"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "filler"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [],
                                        "cornerRadius": "30px",
                                        "height": "12px",
                                        "width": "12px",
                                        "borderColor": "#262673",
                                        "borderWidth": "2px"
                                    },
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": start if i==0 else " ",
                                "gravity": "center",
                                "flex": 4,
                                "size": "sm"
                            }
                        ],
                        "spacing": "lg",
                        "cornerRadius": "30px",
                        "margin": "xs"
                    },{
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "flex": 1
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "filler"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [],
                                                "width": "2px",
                                                "backgroundColor": "#3399ff"
                                            },
                                            {
                                                "type": "filler"
                                            }
                                        ],
                                        "flex": 1
                                    }
                                ],
                                "width": "12px"
                            },
                            {
                                "type": "text",
                                "text": f"{temp}",
                                "gravity": "center",
                                "flex": 4,
                                "size": "xs",
                                "color": "#8c8c8c"
                            }
                        ],
                        "spacing": "lg",
                        "height": "64px"
                    }])
        contents["body"]["contents"].append({
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "END",
                                "gravity": "center",
                                "size": "sm",
                                "color": "#ff1a1a"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "filler"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [],
                                        "cornerRadius": "30px",
                                        "width": "12px",
                                        "height": "12px",
                                        "borderColor": "#262673",
                                        "borderWidth": "2px"
                                    },
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": end,
                                "gravity": "center",
                                "flex": 4,
                                "size": "sm"
                            }
                        ],
                        "spacing": "lg",
                        "cornerRadius": "30px"
                    })

        return FlexSendMessage(
            alt_text=f"Transit: {start}->{end}",
            contents=contents
        )
    def get_channel(self,keyword):

        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"),
                                  options=options)
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(options = options)

        url = f"https://www.youtube.com/results?search_query={quote(keyword)}".replace(" ","+")
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
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"),
                                  options=options)
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(options = options)

        url = f"https://www.youtube.com/results?search_query={quote(keyword)}".replace(" ","+")
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
    def get_travel_f(self,start, end):
        user_par = "Transit"
        no_distance = ["Transit", "Flight", '大眾運輸', '飛機']

        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"),
                                  options=options)

        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # driver = webdriver.Chrome(options=options)
        url = f"https://www.google.com.tw/maps/dir/{quote(start)}/{quote(end)}"
        driver.get(url)
        driver.implicitly_wait(30)
        buttons = driver.find_element_by_css_selector("[role~='radiogroup']").find_elements_by_tag_name("button")
        infos = []
        for button in buttons:
            if button.get_attribute("disabled") == "true":
                continue
            travel_type = button.find_element_by_tag_name("img").get_attribute("aria-label")
            try:
                ActionChains(driver).click(button).perform()
                time.sleep(2)
                travel_list = driver.find_elements_by_css_selector(
                    "[class='section-layout']>[class~='section-directions-trip']")
                for method in travel_list:
                    if travel_type == user_par:
                        # scroll to the element
                        driver.execute_script("return arguments[0].scrollIntoView(true);",
                                              method)
                        # travel method
                        way = method.find_element_by_tag_name("img").get_attribute("aria-label").replace(" ", '')
                        # travel path hint
                        description = method.find_element_by_tag_name("h1").text

                        # if transit, find the transportation to take
                        trans_trip = []
                        if way == "Transit" or way == "大眾運輸":
                            steps = method.find_elements_by_css_selector(
                                "[class~='section-directions-trip-renderable-summary']>span")
                            for step in steps:
                                alt_type = step.find_element_by_tag_name("img").get_attribute("alt")
                                # print(step_type,"////", alt_type=="")
                                alt_type = alt_type if alt_type != "" else "->"

                                transit_tools = step.find_elements_by_css_selector("span")
                                transit_choices = []
                                for tool in transit_tools:
                                    transit_choices.append(tool.text)
                                transit_choices = set(transit_choices)
                                transit_choices = list(transit_choices)
                                transit_choices.remove('')
                                transit_choices.insert(0, alt_type)
                                trans_trip += transit_choices
                        # travel distance
                        distance = method.find_element_by_css_selector(
                            "[class~='section-directions-trip-distance']").text \
                            if way not in no_distance else None

                        duration = method.find_element_by_css_selector(
                            "[class~='section-directions-trip-duration']:first-child").text

                        condition = method.find_element_by_css_selector("[class~='section-directions-trip-duration']"). \
                            get_attribute("class").split("-")[-1] if button == 0 else None

                        info = [way, trans_trip, description, distance, duration, condition]

                        for i in range(len(info)):
                            if not info[i] or info[i] == []:
                                info[i] = "N/A"
                        infos.append(info)

            except Exception as e:
                raise e
        driver.close()
        print(infos[0])
        return infos[0]
    def get_transit(self,start, end):
        user_par = "Transit"
        no_distance = ["Transit", "Flight", '大眾運輸', '飛機']

        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"),
                                  options=options)

        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # driver = webdriver.Chrome(options=options)

        url = f"https://www.google.com.tw/maps/dir/{quote(start)}/{quote(end)}".replace(" ","+")
        print(url)
        driver.get(url)

        driver.implicitly_wait(30)
        buttons = driver.find_element_by_css_selector("[role~='radiogroup']").find_elements_by_tag_name("button")
        infos = []
        for button in buttons:
            if button.get_attribute("disabled") == "true":
                continue
            travel_type = button.find_element_by_tag_name("img").get_attribute("aria-label")
            try:
                if button.find_element_by_tag_name("img").get_attribute("aria-label")=="Transit":
                    ActionChains(driver).click(button).perform()
                time.sleep(2)
                travel_list = driver.find_elements_by_css_selector(
                    "[class='section-layout']>[class~='section-directions-trip']")
                for method in travel_list:
                    if travel_type == user_par:
                        # scroll to the element
                        driver.execute_script("return arguments[0].scrollIntoView(true);",
                                              method)
                        # travel method
                        way = method.find_element_by_tag_name("img").get_attribute("aria-label").replace(" ", '')
                        # travel path hint
                        description = method.find_element_by_tag_name("h1").text

                        # if transit, find the transportation to take
                        trans_trip = []
                        if way == "Transit" or way == "大眾運輸":
                            steps = method.find_elements_by_css_selector(
                                "[class~='section-directions-trip-renderable-summary']>span")
                            for step in steps:
                                alt_type = step.find_element_by_tag_name("img").get_attribute("alt")
                                # print(step_type,"////", alt_type=="")
                                alt_type = alt_type if alt_type != "" else "->"

                                transit_tools = step.find_elements_by_css_selector("span")
                                transit_choices = []
                                for tool in transit_tools:
                                    transit_choices.append(tool.text)
                                transit_choices = set(transit_choices)
                                transit_choices = list(transit_choices)
                                transit_choices.remove('')
                                transit_choices.insert(0, alt_type)
                                trans_trip += transit_choices
                        # travel distance
                        distance = method.find_element_by_css_selector(
                            "[class~='section-directions-trip-distance']").text \
                            if way not in no_distance else None

                        duration = method.find_element_by_css_selector(
                            "[class~='section-directions-trip-duration']:first-child").text

                        condition = method.find_element_by_css_selector("[class~='section-directions-trip-duration']"). \
                            get_attribute("class").split("-")[-1] if button == 0 else None

                        info = [way, trans_trip, description, distance, duration, condition]
                        for i in range(len(info)):
                            if not info[i] or info[i] == []:
                                info[i] = "N/A"
                        infos.append(info)
                        break
            except Exception as e:
                raise e
        driver.close()
        return infos[0]


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
