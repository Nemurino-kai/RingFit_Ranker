# -*- coding: utf-8 -*-
import tweepy
import datetime
import config
import time
import urllib
import info_convert
import sqlite3

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


# 運動記録をツイッター上から検索し、データベースに追加する
def search_exercise_data(api, exercise_data_list, max_number=30):
    for tweet in tweepy.Cursor(api.search, q='#リングフィットアドベンチャー -filter:retweets filter:images').items(max_number * 10):
        print(tweet.text)
        if not fetch_image(tweet): continue
        try:
            # 画像から運動記録を読み取る
            exercise_data = info_convert.image_to_data(tweet.user.name)
            # リストに運動記録を追加
            exercise_data_list.append(exercise_data)
            if len(exercise_data_list) >= max_number: return
        except tweepy.error.TweepError:
            import traceback
            traceback.print_exc()


# 運動記録のランキングをツイートする
def tweet_ranking(api, exercise_data_list):
    # リストを消費カロリー順でソート
    exercise_data_list = sorted(exercise_data_list, key=lambda e: e.exercise_cal, reverse=True)
    tweet = "今日のランキング発表！\n"
    for i, exercise_data in enumerate(exercise_data_list):
        tweet += f"{i + 1}位 {exercise_data.user_name} {exercise_data.exercise_cal}kcal\n"
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


def tweet():

    ## Tableが無ければ作成する
    conn = sqlite3.connect('result.db')
    cur = conn.cursor()
    cur.execute(
        'create table if not exists Excercise (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,kcal REAL,username TEXT,tweet_id TEXT)'
    )

    api = auth_twitter()
    end_tweet_id = 0
    exercise_data_list = []

    # 最初にデータを検索、保存する
    search_exercise_data(api, exercise_data_list)
    # データを検索した日時を記録
    last_data_update_time = datetime.datetime.now(JST)
    # --------------------------------------------------------------
    ID_LIST = []
    first_time = True

    while True:

        print(datetime.datetime.now(JST).hour)
        # 前回のデータ更新から2時間が経っているかつ、0時台なら
        if datetime.datetime.now(JST) - last_data_update_time > datetime.timedelta(hours=2) and datetime.datetime.now(
                JST).hour == 0:
            last_data_update_time = datetime.datetime.now(JST)
            # ランキングを呟く
            tweet_ranking(api, exercise_data_list)
            # データを更新する
            exercise_data_list = []
            search_exercise_data(api, exercise_data_list)
            print("data updated")

        # TWITTER_IDに対しての@コメントか、「#リングフィットランカー」のタグを含むツイートを取得する(RT除く)
        public_tweets = api.search(q=f"@{TWITTER_ID} OR #リングフィットランカー -filter:retweets filter:images -from:{TWITTER_ID}")

        TMP=0

        renew = False
        for tweet in public_tweets:
            if not renew:
                TMP = tweet.id
                renew = True

            if tweet.id > end_tweet_id and first_time == False:
                ID_LIST.append(tweet.id)
                print(tweet.id),
                print(":"),
                print(tweet.text)
            else:
                break

        end_tweet_id = TMP
        first_time = False
        print("Latest tweet ID>>"),
        print(end_tweet_id)

        print("今回のTweet_IDリスト"),
        print(ID_LIST)
        while True:
            if ID_LIST == []:
                break
            tweet_ID = ID_LIST.pop()
            status = api.get_status(tweet_ID)
            if not fetch_image(status): continue
            try:
                # 画像から運動記録を読み取る
                exercise_data = info_convert.image_to_data(status.user.name)

                # リストに運動記録を追加
                exercise_data_list.append(exercise_data)

                # リストを消費カロリー順でソート
                exercise_data_list = sorted(exercise_data_list, key=lambda e: e.exercise_cal, reverse=True)

                # 消費カロリーの順位を計算する
                cal_ranking = exercise_data_list.index(exercise_data)

                tweet = "@" + str(status.user.screen_name) + '\n'
                tweet += str(exercise_data.exercise_cal) + "kcal消費 いい汗かいたね！お疲れ様！\n"
                tweet += f"今日の順位 {cal_ranking + 1}位/{len(exercise_data_list)}人中"
                info_convert.datalist_to_histogram(info_convert.convert_datalist_to_callist(exercise_data_list),
                                                   cal_ranking)
                api.update_with_media(status=tweet, in_reply_to_status_id=status.id, filename='./hist.png')
                # tweet_ranking(api, exercise_data_list)
            except tweepy.error.TweepError:
                import traceback
                traceback.print_exc()

        print("5分sleep")
        time.sleep(300)


if __name__ == '__main__':
    tweet()
