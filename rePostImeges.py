from tweetUtil import simple_tweet_search_j, auth_api, csvToList, urlReplyRemove, multiImgUpload, listToCsv
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
    tweetedIdList = csvToList(csvname)
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
    PostedIdStr = []
    # json to post raw data
    for i in rawJsonList:
        if i['user']['id_str'] not in tweetedIdList and i['user']['id_str'] not in uidList and i['user']['id_str'] not in meId and i['user']['id_str'] not in followerIds:
            ret = urlReplyRemove(i['text'])[0:60]
            sN = i['user']['screen_name']
            twId = i['id_str']
            ret += f'\nhttps://twitter.com/{sN}/status/{twId}'
            ret += f'\nhttps://twitter.com/{sN}'
            try:
                copyIdAndImege.append([ret, [i['media_url']
                                             for i in i['extended_entities']['media'] if i['type'] != 'video']])
                dailyPostedUID.append(i['user']['id_str'])
                PostedIdStr.append(i['id_str'])
            except Exception as e:
                print(f'{i} is {e}')
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
    listToCsv(csvname, PostedIdStr)
    # Record posted users
    listToCsv(uidName, dailyPostedUID)


if __name__ == "__main__":
    main()
