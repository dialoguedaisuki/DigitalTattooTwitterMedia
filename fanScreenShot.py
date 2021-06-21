from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from io import BytesIO


def fanSarvice(accountName):

    options = Options()

    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,1024')

    driver = webdriver.Chrome('chromedriver', options=options)

    # profile
    profile = f'https://twitter.com/{accountName}'
    # mixed
    searchMore = f'https://twitter.com/search?q=to%3A{accountName}&src=typed_query'
    # recent
    recentSearch = f'https://twitter.com/search?q=to%3A{accountName}&src=typed_query&f=live'
    # img
    withImagesTweet = f'https://twitter.com/search?q=to%3A{accountName}&src=typed_query&f=image'
    getSereenShotList = [profile, searchMore, recentSearch, withImagesTweet]
    filename = range(4)
    print(getSereenShotList)
    byteioR = []

    for i in getSereenShotList:
        driver.get(i)
        time.sleep(10)
        byteioR.append(BytesIO(driver.get_screenshot_as_png()))
        print(i)

    driver.quit()

    return byteioR
