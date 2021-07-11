from tweetUtil import simple_tweet_search_j, auth_api, csvToList, urlReplyRemove, multiImgUpload, listToCsv, csvToListMulti, listToCsvDaily, blockUser
from args import args
from pprint import pprint

# get args
search_words, envName, slugid = args()
# Twiter Auth
api = auth_api(envName)


def main():
    csvname = envName + "_tweeted.csv"
    uidName = envName + "_user_id_tweeted.csv"
    # Extract text and original URL
    print(search_words)
    rawJsonList = simple_tweet_search_j(search_words, envName)
    # print(rawJsonList)
    # Exclude images that have already been posted
    tweetedIdList = csvToListMulti(csvname)
    tweetedIdList = list(map(lambda x: x[0], tweetedIdList))
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
    # json to post raw data
    for i in rawJsonList:
        if i['id_str'] not in tweetedIdList and i['user']['id_str'] not in uidList and i['user']['id_str'] not in meId and i['user']['id_str'] not in followerIds:
            ret = urlReplyRemove(i['text'])[0:60]
            sN = i['user']['screen_name']
            twId = i['id_str']
            ret += f'\nhttps://twitter.com/{sN}/status/{twId}'
            ret += f'\nby https://twitter.com/{sN}'
            try:
                copyIdAndImege.append([ret, [i['media_url']
                                             for i in i['extended_entities']['media'] if i['type'] != 'video']])
            except Exception as e:
                print(f'{twId} is {e}')
            else:
                dailyPostedUID.append(i['user']['id_str'])
                postedIdStr.append([i['id_str'], i['user']['screen_name']])
    print("----------------------------------------------------------------target")
    pprint(copyIdAndImege)
    print("----------------------------------------------------------------Exclusion target (uid) addition")
    print(dailyPostedUID)
    print("----------------------------------------------------------------Upload process")
    uploadList = multiImgUpload(copyIdAndImege, envName)
    print("----------------------------------------------------------------Uploaded")
    pprint(uploadList)
    print("----------------------------------------------------------------post")
    for i in uploadList:
        if i[1] != []:
            try:
                post = api.update_status(status=i[0], media_ids=i[1])
                print([post.id, post.text])
            except Exception as e:
                print(f'{i} is {e}')
    # Record posted ID
    listToCsv(csvname, postedIdStr)
    # Record posted users
    listToCsv(uidName, dailyPostedUID)
    # Search attck usera
    listToCsvDaily(envName, postedIdStr)
    # block
    blockUserList = [i[1] for i in postedIdStr]
    blockUserList = blockUser(envName, blockUserList)
    print("----------------------------------------------------------------block")
    print(blockUserList)


if __name__ == "__main__":
    main()
