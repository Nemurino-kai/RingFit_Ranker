# -*- coding: utf-8 -*-
import tweepy
import datetime
import re
import config
import time
import urllib
import ringfitter
import operator

import numpy as np
import matplotlib.pyplot as plt

# TwitterのAPI_TOKEN
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
AS = config.ACCESS_TOKEN_SECRET

# TwitterAPI認証用関数
def authTwitter():
  auth = tweepy.OAuthHandler(CK, CS)
  auth.set_access_token(AT, AS)
  api = tweepy.API(auth, wait_on_rate_limit = True) # API利用制限にかかった場合、解除まで待機する
  return(api)

# 運動記録をツイッター上から検索し、データベースに追加する
def search_exercise_data(api,exercise_data_list,max_number=10):
    for tweet in tweepy.Cursor(api.search, q='#リングフィットアドベンチャー').items(10000):
        print(tweet.text)
        if not fetch_image(tweet): continue
        try:
            # 画像から運動記録を読み取る
            exercise_data = ringfitter.ImageToData(tweet.user.screen_name)
            # リストに運動記録を追加
            exercise_data_list.append(exercise_data)
            if len(exercise_data_list) >= max_number: return
        except tweepy.error.TweepError:
            import traceback
            traceback.print_exc()

# 運動記録のランキングをツイートする
def tweet_ranking(api,exercise_data_list):
    # リストを消費カロリー順でソート
    exercise_data_list = sorted(exercise_data_list, key=lambda e: e.exercise_cal, reverse=True)
    tweet = "今日のランキング発表！\n"
    for i,exercise_data in enumerate(exercise_data_list):
        tweet += f"{i+1}位 {exercise_data.user_name} {exercise_data.cal}kcal"
        if i+1 >= 3:break
    print(tweet)
    api.update_with_media(status=tweet)

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
    if not ringfitter.isResultImage(): return False
    return True

def tweet():

    api = authTwitter()
    end_tweet_id = 0
    exercise_data_list=[]


    #最初にデータを検索、保存する
    search_exercise_data(api,exercise_data_list)
    #データを検索した日時を記録
    last_data_update_time = datetime.datetime.now()
    # --------------------------------------------------------------
    ID_LIST = []
    first_time = True

    while True:

        # 前回のデータ更新から1日が経っているなら、
        if datetime.datetime.now() - last_data_update_time > datetime.timedelta(days=1):
            # データを更新する
            search_exercise_data(api, exercise_data_list)
            print("data updated")
            # ランキングを呟く
            tweet_ranking(api,exercise_data_list)

        # タイムラインを取得する
        public_tweets = api.home_timeline()

        renew = False
        for tweet in public_tweets:
            if renew == False:
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
            #「リングフィット」をtweet内に含む
            if "リングフィット" in str(status.text):
                if not fetch_image(status): continue
                try:
                    # いいねする
                    # api.create_favorite(status.id)

                    # 画像から運動記録を読み取る
                    exercise_data = ringfitter.ImageToData(status.user.name)

                    # リストに運動記録を追加
                    exercise_data_list.append(exercise_data)

                    # リストを消費カロリー順でソート
                    exercise_data_list = sorted(exercise_data_list, key=lambda e: e.exercise_cal,reverse=True)

                    # 消費カロリーの順位を計算する
                    cal_ranking = exercise_data_list.index(exercise_data)

                    tweet = "@" + str(status.user.screen_name) +'\n'
                    tweet += str(exercise_data.exercise_cal) + "kcal消費！ いい汗かいたね！お疲れ様！\n"
                    tweet += f"今日の順位 {cal_ranking+1}位/{len(exercise_data_list)}人中"
                    ringfitter.DataListToHistgram(ringfitter.CovertDatalistToCallist(exercise_data_list),cal_ranking)
                    api.update_with_media(status=tweet, in_reply_to_status_id=status.id,filename='./hist.jpg')
                except tweepy.error.TweepError:
                    import traceback
                    traceback.print_exc()

        time.sleep(60)
        print("1分経過")

tweet()
