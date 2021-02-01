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


def get_route(start, end):
    options = webdriver.ChromeOptions()
    options.add_argument('--kiosk')
    driver = webdriver.Chrome(options=options)
    driver.get("chrome://settings/")
    driver.execute_script("chrome.settingsPrivate.setDefaultZoom(0.8);")
    driver.implicitly_wait(30)
    url = f"https://www.google.com.tw/maps/dir/{quote(start)}/{quote(end)}"
    print(url)
    driver.get(url)
    driver.implicitly_wait(30)
    buttons = driver.find_elements_by_css_selector("[role~='radiogroup']")
    for button in buttons:
        method = button.find_element_by_tag_name("img").get_attribute("aria-label")
        print(method)
        try:
            ActionChains(driver).click(button).perform()
            time.sleep(2)
            methods = driver.find_elements_by_class_name("section-directions-trip")
            for method in methods:
                distance = method.find_element_by_css_selector("[class~='section-directions-trip-distance']").text
                duration = method.find_element_by_css_selector("[class~='section-directions-trip-duration']:first-child").text
                condition = method.find_element_by_css_selector("[class~='section-directions-trip-duration']").\
                    get_attribute("class").split("-")[-1] if button==0 else None
                info = [distance, condition, duration]
                for attr in info:
                    if attr:
                        print(attr, end=" ")
                print()
        except Exception as e:
            raise e
            # continue
    driver.close()


get_route("松山圖書館", "台北101")