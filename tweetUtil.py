import tweepy
import configparser
from pprint import pprint
from io import BytesIO
import requests
import twitter
import time
import csv
import re
import sys
from datetime import datetime
from fanScreenShot import fanSarvice


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


def auth_api_wait(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    print("envName is " + envName)
    consumer_key = config.get(envName, 'consumer_key')
    consumer_secret = config.get(envName, 'consumer_secret')
    access_key = config.get(envName, 'access_key')
    access_secret = config.get(envName, 'access_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
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


def simple_tweet_search_j(search_words, envName):
    api = auth_api(envName)
    set_count = 100
    results = api.search(q=search_words, count=set_count, result_type="mixed")
    # results = api.search(q=word, count=set_count, result_type="recent")
    resultIds = []
    print("-----Search Result-----")
    meId = api.me().id
    for result in results:
        if "RT @" not in result.text and result.user.id != meId:
            print([result.id, result.user.screen_name,
                   result.text.replace('\n', ''), result.created_at])
            resultIds.append(result._json)
    return resultIds


def listToCsv(fileName, listName):
    writeIds = [[i] for i in listName]
    with open(fileName, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(writeIds)
    pass


def csvToList(csvname):
    noTweetIds = []
    with open(csvname) as f:
        noTweetIds = [str(s.strip()) for s in f.readlines()]
    return noTweetIds


def multiImgUpload(targetList, envName):
    api = auth_api(envName)
    uploadList = []
    for i in targetList:
        mediaIds = []
        for j in i[1]:
            try:
                getMedia = requests.get(j).content
                streamMedia = BytesIO(getMedia)
                mediaIds.append(api.media_upload(filename='upload.png',
                                                 file=streamMedia).media_id_string)
                print(f'{j} is upload')
            except Exception as e:
                print(f'{i} is {e}')
        uploadList.append([i[0], mediaIds])
    return uploadList


def user_in_list(userlist, slugid, envName):
    api = auth_api(envName)
    if slugid == "":
        sys.exit()
    print("-----User List-----")
    print(userlist)
    s_userlist = list(set(userlist))
    print("-----Seted User List-----")
    print(s_userlist)
    # add lists
    for usr in s_userlist:
        if api.get_user(usr).screen_name != api.me().screen_name:
            try:
                api.add_list_member(user_id=usr, slug=slugid,
                                    owner_screen_name=api.me().screen_name)
                print(api.get_user(usr).screen_name + " is join!!!")
            except Exception as e:
                print(e)


def listToCsv(fileName, listName):
    writeIds = [[i] for i in listName]
    with open(fileName, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(writeIds)
    pass


def listToCsvMulti(fileName, listName):
    with open(fileName, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(listName)
    pass


def listToCsvDaily(envName, listName):
    now = datetime.now()
    dt = now.strftime('%Y%m%d')
    filename = f'./csv/{envName}_{dt}.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(listName)
    pass


def csvToList(csvname):
    noTweetIds = []
    with open(csvname) as f:
        noTweetIds = [str(s.strip()) for s in f.readlines()]
    return noTweetIds


def csvToListMulti(csvname):
    listName = []
    with open(csvname) as f:
        reader = csv.reader(f)
        for r in reader:
            listName.append(r)
    return listName


def urlReplyRemove(target):
    removedTarget = ""
    try:
        removedTarget = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)",
                               "", target).replace('@', '').replace('\n', '').replace('\r', '')
    except Exception as e:
        print(f'{target} is {e}')
    return removedTarget


def screenShotAndUpload(targetList, envName, hashTagStr):
    api = auth_api(envName)
    uploadList = []
    for i in targetList:
        ret = f'#{hashTagStr}\n'
        ret += f'name:{i[2]}\n'
        ret += f'tweets:{i[4]}\n'
        ret += f'bio: {i[3]}\n'
        ret = ret[0:70]
        ret += f' https://twitter.com/{i[0]}/status/{i[1]}\n'
        try:
            uploadList.append([ret, [api.media_upload(
                filename='upload.png', file=i).media_id_string for i in fanSarvice(i[0])]])
        except Exception as e:
            print(f'{i} is {e}')
    return uploadList


def blockUser(envName, listName):
    api = auth_api(envName)
    for i in listName:
        try:
            api.create_block(i)
        except Exception as e:
            print(f'{i}' is {e})


def listToCsvDaily(envName, listName):
    now = datetime.now()
    dt = now.strftime('%Y%m%d')
    filename = f'./csv/{envName}_{dt}.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(listName)
    pass
