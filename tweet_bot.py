# -*- coding: utf-8 -*-
import tweepy
import datetime
import config
import time
import urllib
import info_convert
import sqlite3
from tqdm import tqdm

# TwitterのAPI_TOKEN
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
AS = config.ACCESS_TOKEN_SECRET

TWITTER_ID = config.TWITTER_ID

# タイムゾーン指定
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


# TwitterAPI認証用関数
def auth_twitter():
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth, wait_on_rate_limit=True)  # API利用制限にかかった場合、解除まで待機する
    return api


# 運動記録をツイッター上から検索し、データベースに追加する, フォローしてくれている人にはリプライする。
def search_exercise_data(api, max_number=100):
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    player_num=0
    # フォローしてくれている人を取得
    follower_id = api.followers_ids()
    for tweet in tweepy.Cursor(api.search, q=f'#リングフィットアドベンチャー -filter:retweets filter:images OR @{TWITTER_ID}'
    f' OR #リングフィットランカー -filter:retweets filter:images -from:{TWITTER_ID}').items(max_number * 10):
        print(tweet.text)
        # idが重複していたら、すでにそこまで検索してあるので中断
        cur.execute("select count(*) from Exercise where tweet_id == ?", (tweet.id,))
        if int(cur.fetchone()[0]): return
        # imgがリングフィットのものでなければcontinue
        if not fetch_image(tweet): continue
        try:
            # 画像から運動記録を読み取る
            exercise_data = info_convert.image_to_data(tweet.user.name)
            print(exercise_data.exercise_cal)
            # DBに運動記録を追加
            params = (exercise_data.exercise_cal,tweet.user.name,tweet.user.screen_name,tweet.id,tweet.created_at+ datetime.timedelta(hours=9))
            cur.execute(
                "insert into Exercise (kcal,user_name,user_screen_name,tweet_id,tweeted_time) "
                "values (?,?,?,?,?) ",params
            )
            conn.commit()

            # もしフォローしてくれている人なら、順位を呟く
            if tweet.user.id in follower_id:
                print(tweet.user.screen_name," さんにお返事します")
                reply_exercise_result(api,cur,exercise_data,tweet)

            player_num = player_num+1

            if player_num >= max_number:
                return
        except tweepy.error.TweepError:
            import traceback
            traceback.print_exc()



# 運動記録のランキングをツイートする
def tweet_ranking(api):
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    # DBから前日分の運動結果を抽出し、消費カロリーの多い順でソート
    # +9hours-24hours=15hours(時差-24時間分で前日のdataを取得)
    cur.execute("select user_name,kcal from Exercise "
                "WHERE date(time_stamp) == date('now', '-15 hours') ORDER BY kcal DESC ;")
    exerise_data_list = cur.fetchall()
    tweet = "今日のランキング発表！\n"
    for i, exercise_data in enumerate(exerise_data_list):
        tweet += f"{i + 1}位 {exercise_data[0]} {exercise_data[1]}kcal\n"
        if i + 1 >= 3: break
    print(tweet)
    api.update_status(status=tweet)


# 運動結果の画像を取得出来たらtrue,できなかったらfalseを返す
def fetch_image(status):
    # mediaがなければ飛ばす
    if not hasattr(status, 'extended_entities'): return False
    # mediaを保存する
    media_url = status.extended_entities['media'][0]['media_url']
    try:
        urllib.request.urlretrieve(media_url + ':orig', 'temp.jpg')
    except IOError:
        # 保存に失敗したら飛ばす
        print("save miss")
        return False
    # 運動結果の画像でなければ飛ばす
    if not info_convert.is_result_image(): return False
    return True

def reply_exercise_result(api,cur,exercise_data,status):
    # DBから今日の分のデータを抽出し、消費カロリー順でソート
    cur.execute("select kcal from Exercise "
                "WHERE date(time_stamp) == date('now', '+9 hours') ORDER BY kcal DESC ;")
    exercise_data_list = cur.fetchall()
    print(exercise_data)

    # 消費カロリーの順位を計算する
    # tuple にするためカンマをつけている
    params = (exercise_data.exercise_cal,)
    cur.execute("select count(*) from Exercise WHERE Exercise.kcal > ? "
                "AND date(time_stamp) == date('now', '+9 hours')", params)
    cal_ranking = int(cur.fetchone()[0])
    print(cal_ranking)

    tweet = "@" + str(status.user.screen_name) + '\n'
    tweet += str(exercise_data.exercise_cal) + "kcal消費 いい汗かいたね！お疲れ様！\n"
    tweet += f"今日の順位 {cal_ranking + 1}位/{len(exercise_data_list)}人中"
    print(exercise_data_list)
    info_convert.datalist_to_histogram(info_convert.convert_datatuple_to_callist(exercise_data_list),
                                       cal_ranking)
    api.update_with_media(status=tweet, in_reply_to_status_id=status.id, filename='./hist.png')


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

    # データを検索した日時を記録
    last_data_update_time = datetime.datetime.now(JST)
    # --------------------------------------------------------------

    while True:

        print("画像を検索")
        search_exercise_data(api)

        # 前回のデータ更新から2時間が経っているかつ、0時台なら
        if datetime.datetime.now(JST) - last_data_update_time > datetime.timedelta(hours=2) and datetime.datetime.now(
                JST).hour == 0:
            last_data_update_time = datetime.datetime.now(JST)
            # ランキングを呟く
            tweet_ranking(api)

        print("5分sleep")
        [time.sleep(10) for i in tqdm(range(30))]


if __name__ == '__main__':
    tweet()
