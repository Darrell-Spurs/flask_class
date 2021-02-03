import os
from selenium import webdriver

def sel_test():
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"),
                              options=options)
    driver.get("www.google.com")
    return driver.page_source