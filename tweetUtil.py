import tweepy
import configparser
from pprint import pprint
from io import BytesIO
import requests
import twitter
import time


def auth_api(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    print("envName is " + envName)
    consumer_key = config.get(envName, 'consumer_key')
    consumer_secret = config.get(envName, 'consumer_secret')
    access_key = config.get(envName, 'access_key')
    access_secret = config.get(envName, 'access_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api


def auth_api2(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    consumer_key = config.get(envName, 'consumer_key')
    consumer_secret = config.get(envName, 'consumer_secret')
    access_key = config.get(envName, 'access_key')
    access_secret = config.get(envName, 'access_secret')
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_key,
                      access_token_secret=access_secret)
    return api


def uploadVideo(envName, movieUrl, text):
    text = text
    ioimg = requests.get(movieUrl)
    upimg = BytesIO(ioimg.content)
    upimg.mode = 'rb'
    upimg.name = 'mobie.mp4'
    api2 = auth_api2(envName)
    mediaId = api2.UploadMediaChunked(
        media=upimg, media_category="tweet_video")
    print(f'mediaId is {mediaId}')
    time.sleep(10)  # https://github.com/bear/python-twitter/issues/654
    if mediaId != "" and text != "":
        postTweet = api2.PostUpdate(status=text, media=mediaId)
        pprint(postTweet)


def simple_tweet_search(search_words, envName):
    api = auth_api(envName)
    set_count = 100
    results = api.search(q=search_words, count=set_count, result_type="mixed")
    # results = api.search(q=word, count=set_count, result_type="recent")
    resultIds = []
    exIds = []
    # blocked user exclusion
    blocks = api.blocks()
    print("---block user list---")
    for i in blocks:
        print([i.id, i.screen_name])
        exIds.append(i.id)
    print("-----Search Result-----")
    meId = api.me().id
    for result in results:
        if result.user.id not in exIds and result.user.id != meId and "RT" not in result.text:
            print([result.id, result.user.screen_name,
                   result.text.replace('\n', ''), result.created_at])
            resultIds.append(result.id)
    return resultIds
