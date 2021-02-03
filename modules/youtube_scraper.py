from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
import time

def get_channel(keyword):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    url = f"https://www.youtube.com/results?search_query={quote(keyword)}"
    print(url)
    driver.get(url)
    driver.implicitly_wait(30)
    target = driver.find_elements_by_class_name("ytd-channel-renderer")
    channel_link = None
    for elem in target:
        if elem.get_attribute("href"):
            channel_link = elem.get_attribute("href")
            break

    driver.close()
    return channel_link



def get_newest(keyword):

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

    channel_videos = channel_link+"/videos"
    driver.get(channel_videos)
    links = driver.find_elements_by_id("video-title")

    return links[0].get_attribute("href")


def get_route(start, end, user_par):

    no_distance = ["Transit","Flight",'大眾運輸','飛機']

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    url = f"https://www.google.com.tw/maps/dir/{quote(start)}/{quote(end)}"
    print(url)
    driver.get(url)
    driver.implicitly_wait(30)
    buttons = driver.find_element_by_css_selector("[role~='radiogroup']").find_elements_by_tag_name("button")
    for button in buttons:
        if button.get_attribute("disabled") == "true":
            continue
        travel_type = button.find_element_by_tag_name("img").get_attribute("aria-label")
        try:
            ActionChains(driver).click(button).perform()
            time.sleep(2)
            travel_list = driver.find_elements_by_css_selector("[class='section-layout']>[class~='section-directions-trip']")
            for method in travel_list:
                if travel_type == user_par:
                    # scroll to the element
                    driver.execute_script("return arguments[0].scrollIntoView(true);",
                                          method)
                    # travel method
                    way = method.find_element_by_tag_name("img").get_attribute("aria-label").replace(" ",'')
                    # travel path hint
                    description = method.find_element_by_tag_name("h1").text
                    # if transit, find the transportation to take
                    if way=="Transit" or way=="大眾運輸":
                        steps = method.find_elements_by_css_selector("[class~='section-directions-trip-renderable-summary']>span")
                        time.sleep(3)
                        for step in steps:
                            transit_tool = step.text
                            print(transit_tool[:len(transit_tool/2)-1])
                            alt_type = step.find_element_by_tag_name("img").get_attribute("alt")
                            # print(step_type,"////", alt_type=="")
                            print(alt_type if alt_type!="" else "->", transit_tool, end=" ")
                            # print(trans_type[step_type],end=" ")
                    # travel distance
                    distance = method.find_element_by_css_selector("[class~='section-directions-trip-distance']").text \
                        if way not in no_distance else None

                    duration = method.find_element_by_css_selector("[class~='section-directions-trip-duration']:first-child").text

                    condition = method.find_element_by_css_selector("[class~='section-directions-trip-duration']").\
                        get_attribute("class").split("-")[-1] if button==0 else None

                    info = [way, description, distance, duration, condition]
                    for attr in info:
                        if attr:
                            print(attr, end="/")
                    print()
        except Exception as e:
            continue
    driver.close()


get_route("SOGO復興館", "松山圖書館", "Transit")
