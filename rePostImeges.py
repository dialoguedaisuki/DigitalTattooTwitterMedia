from tweetUtil import simple_tweet_search, auth_api
from args import args
from pprint import pprint
import re
from io import BytesIO
import requests
import csv

# get args
search_words, envName = args()
# Twiter Auth
api = auth_api(envName)


def main():
    csvname = envName + "_tweeted.csv"
    # Extracting text and original URL
    copyIdAndImege = []
    idList = simple_tweet_search(search_words, envName)
    print("---------------------search target")
    print(idList)
    # Exclude already been posted and
    print("---------------------noTweetIds")
    with open(csvname) as f:
        noTweetIds = [int(s.strip()) for s in f.readlines()]
    print(noTweetIds)
    # Exclude images of followers
    meId = api.me().screen_name
    followerIds = api.followers_ids(meId)
    print("---------------------followerIds")
    print(followerIds)
    twIds = [i for i in idList if i not in noTweetIds and i not in followerIds]
    print("---------------------execution targets")
    print(twIds)
    # create post list
    for id in twIds:
        try:
            tweet = api.get_status(id)
        except Exception as e:
            print(e)
        ret = re.sub(
            r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "", tweet.text).replace('@', '')[0:100]
        ret += f'\n by https://twitter.com/{tweet.user.screen_name}'
        try:
            copyIdAndImege.append([ret, [i['media_url']
                                         for i in tweet.extended_entities['media'] if i['type'] != 'video']])
        except Exception as e:
            print(e)
    pprint(copyIdAndImege)
    # Upload and make post list
    uploadList = []
    for i in copyIdAndImege:
        try:
            uploadList.append([i[0], [api.media_upload(filename='upload.png', file=BytesIO(
                requests.get(z).content)).media_id_string for z in i[1]]])
        except Exception as e:
            print(e)
    print("----------------upload list")
    pprint(uploadList)
    # post
    for i in uploadList:
        if i[1] != []:
            try:
                post = api.update_status(status=i[0], media_ids=i[1])
                print(
                    "---------------------------------------------------------------post")
                pprint([post._json['created_at'], post._json['text']])
            except Exception as e:
                print(e)
    # Record what you have already posted
    writeIds = [[i] for i in twIds]
    with open(csvname, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(writeIds)
    pass


if __name__ == "__main__":
    main()
