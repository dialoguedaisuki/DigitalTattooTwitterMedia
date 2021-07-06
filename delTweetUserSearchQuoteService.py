from tweetUtil import csvToListMulti, auth_api_wait, urlReplyRemove, screenShotAndUpload, listToCsvMulti, blockUser
from args import args
from pprint import pprint
from datetime import datetime, timedelta

# speedly log
import functools
print = functools.partial(print, flush=True)
# get args
search_words, envName, slugid = args()
# Twiter Auth
api = auth_api_wait(envName)


def main():
    """
    please setting $hashTagStr
    """
    hashTagStr = ""
    plusQueryWord = search_words
    # remove posted user
    recordCsvName = f'{envName}_del_tweeted_fans.csv'
    removeIdsList = csvToListMulti(recordCsvName)
    removeIdsList = list(map(lambda x: x[0], removeIdsList))
    # daily target(yestarday file)
    yesterday = datetime.now() - timedelta(days=1)
    dt = yesterday.strftime('%Y%m%d')
    csvname = f'csv/{envName}_{dt}.csv'
    tweetedIdList = csvToListMulti(csvname)
    print("----------------------------------------------------------------daily user")
    print(tweetedIdList)
    print("----------------------------------------------------------------remove user")
    print(removeIdsList)
    searchTweetIds = []
    print("----------------------------------------------------------------status check")
    # search delete tweet
    for i in tweetedIdList:
        try:
            e = api.get_status(i[0])
            print(f'{i} is {e.id}')
        except Exception as e:
            print(f'{i} is {e}')
            searchTweetIds.append(i[1])
    # search and filter user
    print(searchTweetIds)
    set_count = 100
    targetList = []
    for i in searchTweetIds:
        queryWord = f'{i} {plusQueryWord}'
        searchTarget = api.search(
            q=queryWord, count=set_count, result_type="mixed")
        if searchTarget != []:
            filterearchTarget = [
                j for j in searchTarget
                if searchTarget != [] and '@' not in j.text and 'RT' not in j.text
                and j.user.screen_name not in removeIdsList]
            if filterearchTarget != []:
                for i in filterearchTarget:
                    targetList.append(
                        [i.user.screen_name, i.id, i.user.name,
                         urlReplyRemove(i.user.description), i.user.statuses_count])
        queryWord = ""
    print("----------------------------------------------------------------target")
    pprint(targetList)
    # create tweet and bynary upload
    print("----------------------------------------------------------------upload")
    hashTagStr = ""
    uploadList = screenShotAndUpload(targetList, envName, hashTagStr)
    pprint(uploadList)
    print("----------------------------------------------------------------post")
    for i in uploadList:
        if i[0] != [] or i[1] != []:
            try:
                post = api.update_status(status=i[0], media_ids=i[1])
                print([post.created_at, post.text])
            except Exception as e:
                print(e)
    # record screen_name and id
    targetList = list(map(lambda x: [x[0], x[1]], targetList))
    listToCsvMulti(recordCsvName, targetList)
    print("----------------------------------------------------------------block")
    blockUserList = [i[0] for i in targetList]
    blockUser(envName, blockUserList)


if __name__ == "__main__":
    main()
