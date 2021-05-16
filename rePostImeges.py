from tweetUtil import simple_tweet_search, auth_api
from args import args
from pprint import pprint
import re
from io import BytesIO
import requests

# get args
search_words, envName = args()
# Twiter Auth
api = auth_api(envName)


def main():
    csvname = envName + "_tweeted.csv"
    # Extracting text and original URL
    copyIdAndImege = []
    idList = simple_tweet_search(search_words, envName)
    print("---------------------target")
    print(idList)
    print("---------------------excluded")
    with open(csvname) as f:
        noTweetIds = [int(s.strip()) for s in f.readlines()]
    print(noTweetIds)
    for id in idList:
        if id not in noTweetIds:
            try:
                tweet = api.get_status(id)
            except Exception as e:
                print(e)
            ret = re.sub(
                r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "", tweet.text).replace('@', '')[0:100]
            # ret += f'\by {tweet.user.screen_name}'
            ret += f'\n by ttps://twitter.com/{tweet.user.screen_name}'
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
                print("---------------------------------------------------------------post")
                pprint([post._json['created_at'], post._json['text']])
            except Exception as e:
                print(e)
    # Record what you have already posted
    strList = [str(i) for i in idList]
    strId = '\n'.join(strList)
    with open(csvname, 'wt') as f:
        f.write(strId)


if __name__ == "__main__":
    main()
