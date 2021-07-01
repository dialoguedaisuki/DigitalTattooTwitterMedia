from tweetUtil import listToCsvMulti, csvToList, simple_tweet_search_j, auth_api, auth_api2, uploadVideo, csvToListMulti, urlReplyRemove, listToCsv
from args import args
from pprint import pprint
import functools


# speedy log
print = functools.partial(print, flush=True)
# get args
search_words, envName, slugid = args()
# Twiter Auth
api = auth_api(envName)
api2 = auth_api2(envName)


def main():
    csvname = envName + "_tweeted_movie.csv"
    uidName = envName + "_user_id_tweeted_movie.csv"
    # Extracting text and original URL
    copyIdAndImege = []
    rawJsonList = simple_tweet_search_j(search_words, envName)
    print("---------------------search target")
    # Exclude already been posted and
    tweetedIdList = csvToListMulti(csvname)
    tweetedIdList = list(map(lambda x: int(x[0]), tweetedIdList))
    uidList = csvToList(uidName)
    meId = api.me().screen_name
    followerIdsInt = api.followers_ids(meId)
    followerIds = [str(i) for i in followerIdsInt]
    print("----------------------------------------------------------------Exclusion target (posted)")
    print(tweetedIdList)
    print("----------------------------------------------------------------Exclusion target (follower))")
    print(followerIds)
    print("----------------------------------------------------------------Exclusion target (uid)")
    print(uidList)
    copyIdAndImege = []
    dailyPostedUID = []
    postedIdStr = []
    # create post list
    for i in rawJsonList:
        if i['id_str'] not in tweetedIdList and i['user']['id_str']not in uidList \
                and i['user']['id_str'] not in meId and i['user']['id_str'] not in followerIds:
            ret = urlReplyRemove(i['text'])[0:60]
            sN = i['user']['screen_name']
            twId = i['id_str']
            ret += f'\nhttps://twitter.com/{sN}/status/{twId}'
            ret += f'\nhttps://twitter.com/{sN}'
            try:
                url = max([i['url'] for i in i['extended_entities']['media'][0]['video_info']
                            ['variants'] if i['content_type'] != 'application/x-mpegURL'])
                copyIdAndImege.append([ret, url])
                dailyPostedUID.append(i['user']['id_str'])
                postedIdStr.append([i['id_str'], i['user']['screen_name']])
            except Exception as e:
                print(f'{twId} is {e}')
    pprint(copyIdAndImege)
    # Upload and make post list
    for i in copyIdAndImege:
        try:
            uploadVideo(envName, i[1], i[0])
        except Exception as e:
            print(f'{i} is {e}')
    # Record posted ID
    listToCsvMulti(csvname, postedIdStr)
    # Record posted users
    listToCsv(uidName, dailyPostedUID)


if __name__ == "__main__":
    main()
