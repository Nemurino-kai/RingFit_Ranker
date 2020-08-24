# -*- coding: utf-8 -*-
import tweepy
import datetime
import config
import urllib
import info_convert
import sqlite3
import traceback
import utils
from PIL import Image, ImageDraw, ImageFont
import random
import sys


# TwitterのAPI_TOKEN
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
AS = config.ACCESS_TOKEN_SECRET

TWITTER_ID = config.TWITTER_ID

# タイムゾーン指定
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

# リプライ用のメッセージを読み込み
lines = [line.rstrip('\n') for line in open('talking_list.txt',encoding="utf-8")]

# TwitterAPI認証用関数
def auth_twitter():
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth, wait_on_rate_limit=True)  # API利用制限にかかった場合、解除まで待機する
    return api


# 運動記録をツイッター上から検索し、データベースに追加する, フォローしてくれている人にはリプライする。
def search_exercise_data(api, max_number=300,interrupt=True):
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    # フォローしてくれている人を取得
    follower_id = api.followers_ids()

    for tweet in tweepy.Cursor(api.search, q=f'#リングフィットアドベンチャー -filter:retweets filter:images',tweet_mode="extended").items(max_number):
        print(tweet.full_text)
        # idが重複していたら、すでにそこまで検索してあるので中断
        cur.execute("select count(*) from Exercise where tweet_id == ?", (tweet.id,))
        if int(cur.fetchone()[0]) :
            if interrupt: return
            else: continue
        # imgがリングフィットのものでなければcontinue
        image_type = fetch_image(tweet)
        if image_type is None: continue
        try:
            # 画像から運動記録を読み取る
            exercise_data = info_convert.image_to_data(image_type)
            print(exercise_data.cal)
            # DBに運動記録を追加
            params = (exercise_data.cal,tweet.user.name,tweet.user.screen_name,tweet.id,tweet.created_at+ datetime.timedelta(hours=9))
            cur.execute(
                "insert into Exercise (kcal,user_name,user_screen_name,tweet_id,tweeted_time) "
                "values (?,?,?,?,?) ",params
            )
            conn.commit()

            # もしフォローしてくれている人なら、順位を呟く
            if tweet.user.id in follower_id:
                print(tweet.user.screen_name," さんにお返事します")
                reply_exercise_result(api,cur,exercise_data,tweet)

        except tweepy.error.TweepError:
            traceback.print_exc()
            utils.send_mail("Tweepy has occurred.", traceback.format_exc())


# @{TWITTER_ID}へのリプに対し、順位を返信する。
# TODO:開発中/まだ使えません
def reply_ranking(api,item_num=100):
    for tweet in tweepy.Cursor(api.search, q=f'@{TWITTER_ID}',tweet_mode="extended").items(item_num):
        print(tweet.full_text)
        # ツイートに順位 が含まれているなら、順位をリプライする
        if not "順位" in tweet.full_text:
            return
        conn = sqlite3.connect(config.DATABASE_NAME)
        cur = conn.cursor()

        now = datetime.datetime.now(JST)
        ranking_timestamp = now - datetime.timedelta(hours=4)

        params = (tweet.user.id,ranking_timestamp)

        # user_idからカロリーを抽出
        cur.execute("SELECT kcal FROM Exercise WHERE user_id == ? AND date(datetime(time_stamp,'-4 hours'))==?",params)


def make_ranking_picture(exercise_data_list):
    # ベース画像を読み込む
    im = Image.open('ranking_template.png')
    draw = ImageDraw.Draw(im)

    # 枠幅
    W_song = 390

    # ユーザ名のフォントサイズとフォント種類
    font_size_ranking = 35
    font_ranking = ImageFont.truetype(config.RANKING_FONT,font_size_ranking)
    # 消費カロリーのフォントサイズとフォント種類
    font_size_point = 25
    font_point = ImageFont.truetype(config.KCAL_FONT,font_size_point)

    # 標準のフォントカラー
    font_color = (200, 0, 0)
    # 消費カロリー用のフォントカラー
    font_color_point = (150, 0, 0)

    # ランキング
    for i, exercise_data in enumerate(exercise_data_list):
        user_name = exercise_data[0]
        kcal = f"{exercise_data[1]}kcal"

        # 1位から5位、6位から10位でポジションを変更
        w_pos_s = 15 if i < 5 else 610
        w_pos_p = 0 if i < 5 else 605
        h_pos = i if i < 5 else i - 5

        # 消費カロリーを描画
        draw.font = font_point
        draw.text((490 + w_pos_p, 170 + 99 * h_pos),
                  kcal, font_color_point)

        # ユーザ名を描画
        draw.font = font_ranking
        w_song, h_song = draw.textsize(user_name)
        # 枠をはみ出す場合は縮小する。
        if w_song > W_song:
            font_size = int(font_size_ranking * W_song / w_song)
            draw.font = ImageFont.truetype(config.RANKING_FONT,font_size)
            w_song_n, h_song_n = draw.textsize(user_name)
            draw.text(
                (85 + w_pos_s, 165 + 97 * h_pos +
                 (h_song - h_song_n) * h_song_n / h_song * 1.1),
                user_name, font_color)
        else:
            draw.text((85 + w_pos_s, 165 + 97 * h_pos), user_name, font_color)

    im.save("ranking_picture.png")

# 運動記録のランキングをツイートする
def tweet_ranking(api):
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    # DBから前日分の運動結果を抽出し、消費カロリーの多い順でソート
    # 昨日の04:00:00 から 今日の03:59:59まで
    now = datetime.datetime.now(JST)
    yesterday = now - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    params = (yesterday, )

    cur.execute("SELECT user_name,kcal "
                "FROM (SELECT *, RANK() OVER(PARTITION BY user_screen_name ORDER BY kcal DESC, tweeted_time ASC) AS rnk FROM Exercise WHERE  date(datetime(time_stamp,'-4 hours')) == ?) tmp "
                "WHERE rnk = 1 ORDER BY kcal DESC, tweeted_time ASC  LIMIT 10;",params)


    exercise_data_list = cur.fetchall()
    make_ranking_picture(exercise_data_list)
    tweet = "今日のランキング発表！\n"
    for i, exercise_data in enumerate(exercise_data_list):
        tweet += f"{i + 1}位 {exercise_data[0]} {exercise_data[1]}kcal\n"
        if i + 1 >= 3: break
    print(tweet)
    api.update_with_media(status=tweet, filename='./ranking_picture.png')


# 運動結果の画像を取得出来たらimagetype,できなかったらNoneを返す
def fetch_image(status):
    # mediaがなければ飛ばす
    if not hasattr(status, 'extended_entities'):
        print("Media not found.")
        return None
    for i in range(len(status.extended_entities['media'])):
        # mediaを保存する
        media_url = status.extended_entities['media'][i]['media_url']
        try:
            urllib.request.urlretrieve(media_url + ':orig', 'temp.jpg')
        except IOError:
            # 保存に失敗したら飛ばす
            print("save miss")
            continue
        # 運動結果の画像でなければ飛ばす
        image_type = info_convert.is_result_image()
        if image_type is None:
            print("Media is not exercise image.")
            continue
        else:
            return image_type
    return None

def get_reply_message():
    return random.choice(lines)

def reply_exercise_result(api,cur,exercise_data,status):

    now = datetime.datetime.now(JST)
    ranking_datetime = now - datetime.timedelta(hours=4)
    ranking_datetime = ranking_datetime.strftime("%Y-%m-%d")
    params=(ranking_datetime,)

    # DBから今日の順位分のデータを抽出し、消費カロリー順でソート

    cur.execute("select kcal from Exercise "
                "WHERE date(datetime(time_stamp,'-4 hours'))==? ORDER BY kcal DESC ;",params)
    exercise_data_list = cur.fetchall()
    print(exercise_data)

    # 消費カロリーの順位を計算する
    params = (exercise_data.cal,ranking_datetime)
    cur.execute("select count(*) from Exercise WHERE Exercise.kcal > ? "
                "AND date(datetime(time_stamp,'-4 hours'))==?", params)
    cal_ranking = int(cur.fetchone()[0])
    print(cal_ranking)

    tweet = "@" + str(status.user.screen_name) + '\n'
    tweet += str(exercise_data.cal) + "kcal消費 "+ get_reply_message() + "\n"
    tweet += f"今日の順位 {cal_ranking + 1}位/{len(exercise_data_list)}人中"
    print(exercise_data_list)
    info_convert.datalist_to_histogram(info_convert.convert_datatuple_to_list(exercise_data_list),
                                       cal_ranking)
    api.update_with_media(status=tweet, in_reply_to_status_id=status.id, filename='./hist.png')

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print("wrong usage")
        exit()
    api = auth_twitter()
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    # フォローしてくれている人を取得
    follower_id = api.followers_ids()
    tweet = api.get_status(int(args[1]))

    # idが重複していたら、消去してよいか確認
    cur.execute("select count(*) from Exercise where tweet_id == ?", (tweet.id,))
    if int(cur.fetchone()[0]) :
        delete_flag=input("Data is already exist in DB. Do you want to delete? (y or n):")
        if delete_flag != "y": exit()
        else: cur.execute("delete from Exercise where tweet_id == ?", (tweet.id,))

    # imgがリングフィットのものでなければ、手動でkcalを入力
    image_type = fetch_image(tweet)
    if image_type is None:
        execute_flag=input("Image type is None. Do you continue yet? (y or n):")
        if execute_flag != "y":exit()
        else:
            set_cal = int(input("please input cal.:"))
            exercise_data = info_convert.ExerciseData(datetime.time(second=0), set_cal, 0)
    else:
        # 画像から運動記録を読み取る
        exercise_data = info_convert.image_to_data(image_type)
        print(f"{exercise_data.cal}kcal と予測しました。")
        kcal_flag=input("If cal is wrong, enter cal. If cal is correct, enter y.(y or number):")
        if kcal_flag != "y": exercise_data.cal = int(kcal_flag)
    params = (exercise_data.cal,tweet.user.name,tweet.user.screen_name,tweet.id,tweet.created_at+ datetime.timedelta(hours=9))
    cur.execute(
                    "insert into Exercise (kcal,user_name,user_screen_name,tweet_id,tweeted_time) "
                    "values (?,?,?,?,?) ",params
    )
    conn.commit()

    # もしフォローしてくれている人なら、順位を呟く
    if tweet.user.id in follower_id:
        reply_flag = input(f"{tweet.user.screen_name}さんにお返事しますか？(y or n):")
        if reply_flag != "y": exit()
        reply_exercise_result(api,cur,exercise_data,tweet)