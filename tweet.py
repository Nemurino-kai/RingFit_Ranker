# -*- coding: utf-8 -*-
import tweepy
import datetime
import re
import config
import time
import urllib
import ringfitter
import operator

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



def tweet():

    api = authTwitter()
    end_tweet_id = 0
    exercise_data_list=[]
    # --------------------------------------------------------------
    ID_LIST = []
    first_time = True

    while True:
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
                #mediaがなければ飛ばす
                if not hasattr(status,'extended_entities') :continue
                #mediaを保存する
                media_url = status.extended_entities['media'][0]['media_url']
                try:
                    urllib.request.urlretrieve(media_url+':orig', 'temp.jpg')
                except IOError:
                    #保存に失敗したら飛ばす
                    print ("save miss")
                    continue
                print("reply")
                # 運動結果の画像でなければ飛ばす
                if not ringfitter.isResultImage():continue
                try:
                    # いいねする
                    # api.create_favorite(status.id)

                    # 画像から運動記録を読み取る
                    exercise_data = ringfitter.ImageToData()

                    # リストに運動記録を追加
                    exercise_data_list.append(exercise_data)

                    # リストを時間順でソート
                    exercise_data_list = sorted(exercise_data_list, key=lambda e: e.exercise_time,reverse=True)

                    # 運動時間の順位を計算する
                    time_ranking = exercise_data_list.index(exercise_data)

                    tweet = "@" + str(status.user.screen_name) +'\n'
                    tweet += str(exercise_data.exercise_time) + " いい汗かいたね！お疲れ様！\n"
                    tweet += f"{time_ranking+1}位/{len(exercise_data_list)}人中"
                    api.update_status(status=tweet, in_reply_to_status_id=status.id)
                except tweepy.error.TweepError:
                    import traceback
                    traceback.print_exc()

        time.sleep(60)
        print("1分経過")

tweet()
