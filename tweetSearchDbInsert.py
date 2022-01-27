from tweetUtil import *
from pprint import pprint
from dbUtil import *
from tweetUtil import *
import sys

# get args
envName = sys.argv[1]
search_words = sys.argv[2]
db_envName = sys.argv[3]

# Twiter Auth
api = auth_api(envName)


def main():
    csvname = envName + "_tweeted.csv"
    uidName = envName + "_user_id_tweeted.csv"
    # Extract text and original URL
    print(search_words)
    rawJsonList = simple_tweet_search(search_words, envName)
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
    preInsertDatals = []
    postedIdStr = []
    print("----------------------------------------------------------------target")
    for r in rawJsonList:
        if r.id_str not in tweetedIdList and \
            r.user.id_str not in uidList and \
                r.user.id_str not in meId and \
                r.user.id_str not in followerIds:
            # print([r.id, r.user.screen_name,
            #        r.text.replace('\n', ''), r.created_at])
            twId = r.id_str
            screen_name = r.user.screen_name
            tw_text = urlReplyRemove(r.text)
            bio = r.user.description.replace('\n', '')
            created_at = r.created_at
            rawJ = r._json
            try:
                urls = [rawJ['media_url'] for rawJ in rawJ['extended_entities']
                        ['media'] if rawJ['type'] != 'video']
                byteas = urlToByteIO(urls)
                preInsertDatals.append(
                    [twId, created_at, screen_name, tw_text, bio, rawJ, byteas])
            except Exception as e:
                print(f'https://twitter.com/i/web/status/{r.id_str} is {e}')
            else:
                postedIdStr.append([r.id_str, r.user.screen_name])
    # 格納対象
    for i in preInsertDatals:
        print(i[0], i[1], i[2], i[3], i[4], len(i[5]), len(i[6]))
    # db insert
    with get_connection(db_envName) as conn:
        with conn.cursor() as cur:
            for i in preInsertDatals:
                # info table insert
                cur.execute('INSERT INTO info (id, create_at, screen_name, tweet_text, bio, raw_json) VALUES (%s, %s, %s, %s, %s, %s)',
                            (i[0], i[1], i[2], i[3], i[4], str(i[5])))
                # byte insert
                for x, y in enumerate(i[6]):
                    cur.execute('INSERT INTO image (id, num, image) VALUES (%s, %s, %s)',
                                (i[0], x, y))
        conn.commit()
    listToCsvMulti(csvname, postedIdStr)


if __name__ == "__main__":
    main()
