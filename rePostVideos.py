from tweetUtil import simple_tweet_search, auth_api, auth_api2, uploadVideo
from args import args
from pprint import pprint
import re

# get args
search_words, envName = args()
# Twiter Auth
api = auth_api(envName)
api2 = auth_api2(envName)


def main():
    csvname = envName + "_tweeted_movie.csv"
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
            # ret += f'\n by @{tweet.user.screen_name}'
            ret += f'\n by https://twitter.com/{tweet.user.screen_name}'
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
    strList = [str(i) for i in idList]
    strId = '\n'.join(strList)
    with open(csvname, 'wt') as f:
        f.write(strId)


if __name__ == "__main__":
    main()
