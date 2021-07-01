from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from io import BytesIO
import io
import functools
from PIL import Image

# speedy log
print = functools.partial(print, flush=True)


def fanSarvice(accountName):

    # selenium parametor
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1080,1920')
    options.binary_location = '/usr/bin/google-chrome'
    driver = webdriver.Chrome('chromedriver', options=options)
    # profile
    profile = f'https://twitter.com/{accountName}'
    # popular reply
    searchMore = f'https://twitter.com/search?q=to%3A{accountName}&src=typed_query'
    # recent reply
    recentSearch = f'https://twitter.com/search?q=to%3A{accountName}&src=typed_query&f=live'
    # iamge
    withImagesTweet = f'https://twitter.com/search?q=from%3A{accountName}%20filter%3Aimages&src=typed_query&f=live'
    getSereenShotList = [profile, searchMore, recentSearch, withImagesTweet]
    print(f'list is {getSereenShotList}')
    byteioR = []

    for i in getSereenShotList:
        driver.get(i)
        time.sleep(10)
        im = Image.open(BytesIO(driver.get_screenshot_as_png()))
        crpim = im.crop((120, 0, 740, 1920))
        img = io.BytesIO()
        crpim.save(img, "PNG")
        crpim = img.getvalue()
        byteioR.append(BytesIO(crpim))
        print(f'captured {i}')

    driver.quit()

    return byteioR
