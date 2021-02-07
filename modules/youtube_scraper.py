from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
import time


def traveling(start, end):
    user_par = "Transit"
    no_distance = ["Transit","Flight",'大眾運輸','飛機']

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    url = f"https://www.google.com.tw/maps/dir/{quote(start)}/{quote(end)}"
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
                    trans_trip = []
                    if way=="Transit" or way=="大眾運輸":
                        steps = method.find_elements_by_css_selector("[class~='section-directions-trip-renderable-summary']>span")
                        for step in steps:
                            alt_type = step.find_element_by_tag_name("img").get_attribute("alt")
                            # print(step_type,"////", alt_type=="")
                            alt_type =  alt_type if alt_type!="" else "->"

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
                    distance = method.find_element_by_css_selector("[class~='section-directions-trip-distance']").text \
                        if way not in no_distance else None

                    duration = method.find_element_by_css_selector("[class~='section-directions-trip-duration']:first-child").text

                    condition = method.find_element_by_css_selector("[class~='section-directions-trip-duration']").\
                        get_attribute("class").split("-")[-1] if button==0 else None

                    info = [way, trans_trip, description, distance, duration, condition]

                    for i in range(len(info)):
                        if not info[i] or info[i]==[]:
                            info[i]="N/A"
                    infos.append(info)

        except Exception as e:
            raise e
    driver.close()
    return infos[0]



all_list = traveling("SOGO復興館", "松山圖書館")
print(all_list)