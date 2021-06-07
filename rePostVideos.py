from tweetUtil import simple_tweet_search, auth_api, auth_api2, uploadVideo
from args import args
from pprint import pprint
import re
import csv

# get args
search_words, envName, listone = args()
# Twiter Auth
api = auth_api(envName)
api2 = auth_api2(envName)


def main():
    csvname = envName + "_tweeted_movie.csv"
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
    twIds = [i for i in idList if i not in noTweetIds]
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
        ret += f' https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'
        # ret += f'\n by https://twitter.com/{tweet.user.screen_name}'
        if tweet.user.id not in followerIds:
            try:
                url = max([i['url'] for i in tweet.extended_entities['media'][0]['video_info']
                            ['variants'] if i['content_type'] != 'application/x-mpegURL'])
                copyIdAndImege.append(
                    [ret, url])
            except Exception as e:
                print(e)
    pprint(copyIdAndImege)
    # Upload and make post list
    for i in copyIdAndImege:
        try:
            uploadVideo(envName, i[1], i[0])
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
