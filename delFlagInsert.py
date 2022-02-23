from pprint import pprint
from tweetUtil import auth_api
from dbUtil import get_connection
import sys


def getQueryResult(db_env):
    with get_connection(db_env) as conn:
        with conn.cursor() as cur:
            cur.execute('select * from info WHERE delflag IS NULL')
            queryLs = [i for i in cur]
    return queryLs


def insflag(flag, twId, db_env):
    with get_connection(db_env) as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE info SET delflag = %s WHERE id = %s RETURNING id, delflag',
                        (flag, twId))
            queryLs = [i for i in cur]
    return queryLs


def urlCreate(scName, id):
    return f'https://twitter.com/{scName}/status/{id}'


api = auth_api(sys.argv[1])
db_env = sys.argv[2]
scLs = getQueryResult(db_env)
scLs = [[i[0], i[2]] for i in scLs]
pprint(scLs)

for i, j in scLs:
    try:
        res = api.get_status(i)._json
    except Exception as e:
        print(f'{urlCreate(j, i)} is delete')
        dbRes = insflag(True, i, db_env)
        print(dbRes)
    else:
        print(f'{urlCreate(j, i)} is not delete')
        dbRes = insflag(False, i, db_env)
        print(dbRes)
