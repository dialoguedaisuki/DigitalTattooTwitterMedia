from tweetUtil import auth_api, simple_tweet_search_j, user_in_list, urlReplyRemove
from args import args
from fanScreenShot import fanSarvice
from pprint import pprint
import csv

# get args
search_words, envName, slugid = args()
# Twiter Auth
api = auth_api(envName)


def main():
    """
    Please specify a fan word.
    """
    fanWord = ""
    csvname = envName + "_faned.csv"
    # text and url Extraction
    print(search_words)
    idList = simple_tweet_search_j(search_words, envName)
    gomikasu = simple_tweet_search_j(fanWord, envName)
    # Exclude if you already have fan service
    with open(csvname) as f:
        fanId = [str(s.strip()) for s in f.readlines()]
    # Exclude yourself and followers
    meId = api.me().id_str
    followerIdsInt = api.followers_ids(meId)
    followerIds = [str(i) for i in followerIdsInt]
    fanSarviceExec = []
    print("----------------------------------------------------------------fans")
    for i in gomikasu:
        if fanWord in i['text'] and i['user']['id_str'] not in meId and i['user']['id_str'] not in followerIds and i['user']['id_str'] not in fanId:
            print(i['user']['screen_name'])
            fanSarviceExec.append(
                [i['user']['screen_name'], i['id'], i['user']['name'], urlReplyRemove(i['user']['description']), i['user']['statuses_count'], i['user']['id_str']])
    print("----------------------------------------------------------------fool fan")
    kusoFan = [i['user']['screen_name'] for i in idList]
    dup = [x for x in set(kusoFan)
           if kusoFan.count(x) > 1]
    for i in idList:
        if i['user']['screen_name'] in dup and i['user']['id_str'] not in meId and i['user']['id_str'] not in followerIds and i['user']['id_str'] not in fanId:
            print(i['user']['screen_name'])
            fanSarviceExec.append(
                [i['user']['screen_name'], i['id'], i['user']['name'], urlReplyRemove(i['user']['description']), i['user']['statuses_count'], i['user']['id_str']])
    print("----------------------------------------------------------------target")
    pprint(fanSarviceExec)
    # create post data
    print("----------------------------------------------------------------get screen shot and upload")
    uploadList = []
    for i in fanSarviceExec:
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
    pprint(uploadList)
    print("----------------------------------------------------------------post")
    for i in uploadList:
        if i[0] != [] or i[1] != []:
            try:
                post = api.update_status(status=i[0], media_ids=i[1])
                pprint([post._json['id_str'], post._json['text']])
            except Exception as e:
                print(e)
    # record posted
    writeIds = [[i[5]] for i in fanSarviceExec]
    listInList = [i[5] for i in fanSarviceExec]
    with open(csvname, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(writeIds)
    pass
    # create fan list
    user_in_list(listInList, slugid, envName)


if __name__ == "__main__":
    main()
