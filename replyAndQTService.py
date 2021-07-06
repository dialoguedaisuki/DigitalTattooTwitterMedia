from tweetUtil import auth_api, screenShotAndUpload, urlReplyRemove, listToCsvMulti, csvToListMulti
from pprint import pprint
from args import args


def main():
    """
    please setting $hashTagStr
    """
    hashTagStr = ""
    # get args
    search_words, envName, slugid = args()
    # Twitter auth
    api = auth_api(envName)
    # search query
    userName = api.me().screen_name
    word = "twitter.com/" + userName + ' /-from:' + userName
    # record csv name
    csvname = envName + "_quotedIds.csv"
    removeIdsList = csvToListMulti(csvname)
    removeIdsList = list(map(lambda x: x[1], removeIdsList))
    # search
    set_count = "100"
    results = api.search(q=word, count=set_count)
    results += api.mentions_timeline()
    attckIdList = []
    for i in results:
        if i.text not in userName and i.text not in "RT"  \
                and i.user.screen_name not in removeIdsList and i.user.screen_name not in userName:
            print([i.id_str, i.user.screen_name, i.text])
            attckIdList.append([i.user.screen_name, i.id, i.user.name,
                                urlReplyRemove(i.user.description), i.user.statuses_count])
    pprint(attckIdList)
    # create tweet and bynary upload
    print("----------------------------------------------------------------upload")
    uploadList = screenShotAndUpload(attckIdList, envName, hashTagStr)
    print("----------------------------------------------------------------post")
    # post
    for i in uploadList:
        if i[0] != [] or i[1] != []:
            try:
                post = api.update_status(status=i[0], media_ids=i[1])
                print([post.created_at, post.text])
            except Exception as e:
                print(f'{i} is {e}')
    pprint(uploadList)
    # record baka
    recordList = list(map(lambda x: [x[1], x[0]], attckIdList))
    listToCsvMulti(csvname, recordList)


if __name__ == "__main__":
    main()
