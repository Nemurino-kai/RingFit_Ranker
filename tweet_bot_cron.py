# -*- coding: utf-8 -*-
import utils
import traceback
from tweet_func import *

def tweet():

    ## Tableが無ければ作成する
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    cur.execute(
        "create table if not exists Exercise ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "time_stamp TEXT NOT NULL DEFAULT (DATETIME('now', '+9 hours')),"
        "tweeted_time TEXT NOT NULL,"
        "kcal INTEGER NOT NULL ,"
        "user_name TEXT NOT NULL ,"
        "user_screen_name TEXT NOT NULL ,"
        "tweet_id NUMERIC NOT NULL UNIQUE)"
    )
    conn.commit()

    api = auth_twitter()

    print("画像を検索")
    search_exercise_data(api, max_number=100, interrupt=False)

if __name__ == '__main__':
    try:
        tweet()
    except (Exception,tweepy.error.TweepError) as e:
        traceback.print_exc()
        utils.send_mail("An error has occurred.",  traceback.format_exc())
        raise e
    except:
        traceback.print_exc()
        utils.send_mail("An error has occurred.",  traceback.format_exc())