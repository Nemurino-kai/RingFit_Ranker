# -*- coding: utf-8 -*-
import time
import utils
import traceback
from tweet_func import *

# タイムゾーン指定
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

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

    # ランキングを呟いた日時を記録する変数
    last_data_update_time = datetime.datetime.now(JST)
    # --------------------------------------------------------------

    while True:

        print("画像を検索")
        search_exercise_data(api)

        # 前回のデータ更新から1時間が経っているかつ、12時台なら
        if datetime.datetime.now(JST) - last_data_update_time > datetime.timedelta(hours=1) and datetime.datetime.now(
                JST).hour == 12:
            last_data_update_time = datetime.datetime.now(JST)
            # ランキングを呟く
            tweet_ranking(api)

        print("5分sleep")
        time.sleep(300)


if __name__ == '__main__':
    try:
        utils.send_mail("Started.", "プログラムを起動しました。")
        tweet()
    except Exception as e:
        utils.send_mail("An error has occurred.",  traceback.format_exc())
    except tweepy.error.TweepError as e:
        utils.send_mail("An error has occurred.",  traceback.format_exc())
