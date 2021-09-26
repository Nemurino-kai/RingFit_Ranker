# -*- coding: utf-8 -*-
import tweepy
import datetime
import urllib
import info_convert
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import random
import sys
import os
import sentry_sdk
from sql_alchemy.models import Exercise, session_scope
from sql_alchemy.controller import insert_exercise_result, get_one_day_player_list, get_one_day_ranking_of_followers, \
    get_daily_ranking, delete_exercise_result_by_tweet_id
from dotenv import load_dotenv
load_dotenv()

# TwitterのAPI_TOKEN
CK = os.environ['CONSUMER_KEY']
CS = os.environ['CONSUMER_SECRET']
AT = os.environ['ACCESS_TOKEN']
AS = os.environ['ACCESS_TOKEN_SECRET']

TWITTER_ID = os.environ['TWITTER_ID']

# タイムゾーン指定
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

# カレントディレクトリを実行ファイルのパスに張り替え
tmp = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# リプライ用のメッセージを読み込み
lines = [line.rstrip('\n') for line in open(
    './talking_list.txt', encoding="utf-8")]


# TwitterAPI認証用関数


def auth_twitter():
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth, wait_on_rate_limit=True)  # API利用制限にかかった場合、解除まで待機する
    return api


# 運動記録をツイッター上から検索し、データベースに追加する, フォローしてくれている人にはリプライする。
def search_exercise_data(api, max_number=300, interrupt=True,
                         query='#リングフィットアドベンチャー OR #RingFitAdventure -filter:retweets filter:images -@tos',
                         api_method_name='search_tweets'):
    # フォローしてくれている人を取得
    follower_id = api.get_follower_ids()

    api_func = getattr(api, api_method_name)

    for tweet in tweepy.Cursor(api_func, q=query, tweet_mode="extended").items(max_number):
        print(tweet.id)
        # idが重複していたら、すでにそこまで検索してあるので中断
        with session_scope() as session:
            same_id_rows = session.query(Exercise).filter(
                Exercise.tweet_id == tweet.id).all()

        if same_id_rows:
            if interrupt:
                return
            else:
                continue
        # imgがリングフィットのものでなければcontinue
        image_type = fetch_image(tweet)
        if image_type is None:
            continue
        try:
            # 画像から運動記録を読み取る
            exercise_data = info_convert.image_to_data(image_type)
            # DBに運動記録を追加
            tweet.created_at = tweet.created_at + datetime.timedelta(hours=9)
            # もし"#昨日の分"と書かれていたら、日付を昨日に変える
            if '#昨日の分' in tweet.full_text:
                tweet.created_at = tweet.created_at - \
                    datetime.timedelta(days=1)
            print(tweet.created_at)
            print(tweet)
            with session_scope() as session:
                insert_exercise_result(session=session, kcal=exercise_data.cal, user_name=tweet.user.name,
                                       user_screen_name=tweet.user.screen_name, tweet_id=tweet.id,
                                       tweeted_time=tweet.created_at)
            # もしフォローしてくれている人なら、順位を呟く
            if tweet.user.id in follower_id:
                print(tweet.user.screen_name, " さんにお返事します")
                reply_exercise_result(api, exercise_data, tweet)

        except (ValueError, tweepy.TweepyException) as err:
            sentry_sdk.capture_exception(err)


# @{TWITTER_ID}へのリプに対し、順位を返信する。
# TODO:開発中/まだ使えません
def reply_ranking(api, item_num=100):
    for tweet in tweepy.Cursor(api.search_tweets, q=f'@{TWITTER_ID}', tweet_mode="extended").items(item_num):
        print(tweet.full_text)
        # ツイートに順位 が含まれているなら、順位をリプライする
        if not "順位" in tweet.full_text:
            return
        conn = sqlite3.connect(os.environ['DATABASE_NAME'])
        cur = conn.cursor()

        now = datetime.datetime.now(JST)
        ranking_timestamp = now - datetime.timedelta(hours=4)

        params = (tweet.user.id, ranking_timestamp)

        # user_idからカロリーを抽出
        cur.execute(
            "SELECT kcal FROM Exercise WHERE user_id == ? AND exercise_day==?", params)


def make_ranking_picture(exercise_data_list):
    # ベース画像を読み込む
    im = Image.open('templates/ranking_template.png')
    draw = ImageDraw.Draw(im)

    # 枠幅
    W_song = 390

    # ユーザ名のフォントサイズとフォント種類
    font_size_ranking = 35
    font_ranking = ImageFont.truetype(
        os.environ['RANKING_FONT'], font_size_ranking)
    # 消費カロリーのフォントサイズとフォント種類
    font_size_point = 25
    font_point = ImageFont.truetype(os.environ['KCAL_FONT'], font_size_point)

    # 標準のフォントカラー
    font_color = (200, 0, 0)
    # 消費カロリー用のフォントカラー
    font_color_point = (150, 0, 0)

    # ランキング
    for i, exercise_data in enumerate(exercise_data_list):
        user_name = exercise_data.user_name
        kcal = f"{exercise_data.kcal}kcal"

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
            draw.font = ImageFont.truetype(
                os.environ['RANKING_FONT'], font_size)
            w_song_n, h_song_n = draw.textsize(user_name)
            draw.text(
                (85 + w_pos_s, 165 + 97 * h_pos +
                 (h_song - h_song_n) * h_song_n / h_song * 1.1),
                user_name, font_color)
        else:
            draw.text((85 + w_pos_s, 165 + 97 * h_pos), user_name, font_color)

    im.save("ranking_picture.png")


# idのリストからユーザ情報のリストを返す関数
def lookup_user_list(user_id_list, api):
    full_users = []
    users_count = len(user_id_list)
    try:
        for i in range((users_count - 1) // 100 + 1):
            full_users.extend(api.lookup_users(
                user_id=user_id_list[i * 100:min((i + 1) * 100, users_count)]))
        return full_users
    except tweepy.TweepyException as err:
        sentry_sdk.capture_exception(err)
        print('Something went wrong, quitting...')


# 運動記録のランキングをツイートする
def tweet_ranking(api):
    # フォローしてくれている人を取得
    follower_ids = api.get_follower_ids()
    print(follower_ids)
    # idからscreen_nameに変換
    follower_names = [
        user.screen_name for user in lookup_user_list(follower_ids, api)]

    # DBから前日分の運動結果を抽出し、消費カロリーの多い順でソート
    # 昨日の04:00:00 から 今日の03:59:59まで
    now = datetime.datetime.now(JST)
    yesterday = (now - datetime.timedelta(days=1)).date()

    with session_scope() as session:
        yesterday_player_list = get_one_day_player_list(session, yesterday)
    # フォロワー中、昨日運動した人だけを取り出し
    follow_players = list(set(yesterday_player_list) & set(follower_names))

    with session_scope() as session:
        exercise_data_list = get_one_day_ranking_of_followers(
            session, yesterday, follow_players)
    print(exercise_data_list)
    make_ranking_picture(exercise_data_list)

    tweet = "今日のランキング発表！\n"
    for i, exercise_data in enumerate(exercise_data_list[:3]):
        tweet += f"{i + 1}位 {exercise_data.user_name} {exercise_data.kcal}kcal\n"

    print(tweet)
    api.update_status_with_media(
        status=tweet, filename='./ranking_picture.png')


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


def reply_exercise_result(api, exercise_data, status):
    ranking_datetime = (status.created_at - datetime.timedelta(hours=4)).date()
    today_datetime = datetime.datetime.now(JST).date()
    if ranking_datetime == today_datetime:
        prefix = "今日"
    else:
        prefix = ranking_datetime.strftime("%Y-%m-%d")

    with session_scope() as session:
        exercise_data_list = get_daily_ranking(session, ranking_datetime)

    # 消費カロリーの順位を計算する
    cal_ranking = sum(e.kcal > exercise_data.cal for e in exercise_data_list)
    print(cal_ranking)

    tweet = "@" + str(status.user.screen_name) + '\n'
    tweet += str(exercise_data.cal) + "kcal消費 " + get_reply_message() + "\n"
    tweet += f"{prefix}の順位 {cal_ranking + 1}位/{len(exercise_data_list)}人中"

    info_convert.datalist_to_histogram(
        [e.kcal for e in exercise_data_list], cal_ranking)
    api.update_status_with_media(
        status=tweet, in_reply_to_status_id=status.id, filename='./hist.png')


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print("wrong usage")
        exit()
    api = auth_twitter()

    # フォローしてくれている人を取得
    follower_id = api.followers_ids()
    tweet = api.get_status(int(args[1]), tweet_mode='extended')

    # idが重複していたら、消去してよいか確認
    with session_scope() as session:
        same_id_rows = session.query(Exercise).filter(
            Exercise.tweet_id == tweet.id).all()
    if same_id_rows:
        delete_flag = input(
            "Data is already exist in DB. Do you want to delete? (y or n):")
        if delete_flag != "y":
            exit()
        else:
            with session_scope() as session:
                delete_exercise_result_by_tweet_id(session, tweet.id)

    # imgがリングフィットのものでなければ、手動でkcalを入力
    image_type = fetch_image(tweet)

    if image_type is None:
        execute_flag = input(
            "Image type is None. Do you continue yet? (y or n):")
        if execute_flag != "y":
            exit()
        else:
            set_cal = int(input("please input cal.:"))
            exercise_data = info_convert.ExerciseData(
                datetime.time(second=0), set_cal, 0)
    else:
        # 画像から運動記録を読み取る
        exercise_data = info_convert.image_to_data(image_type)
        print(f"{exercise_data.cal}kcal と予測しました。")
        kcal_flag = input(
            "If cal is wrong, enter cal. If cal is correct, enter y.(y or number):")
        if kcal_flag != "y":
            exercise_data.cal = int(kcal_flag)

    tweet.created_at = tweet.created_at + datetime.timedelta(hours=9)
    # もし"#昨日の分"と書かれていたら、日付を昨日に変える
    if '#昨日の分' in tweet.full_text:
        tweet.created_at = tweet.created_at - datetime.timedelta(days=1)

    with session_scope() as session:
        insert_exercise_result(session, kcal=exercise_data.cal, user_name=tweet.user.name,
                               user_screen_name=tweet.user.screen_name, tweet_id=tweet.id,
                               tweeted_time=tweet.created_at)

    # もしフォローしてくれている人なら、順位を呟く
    if tweet.user.id in follower_id:
        reply_flag = input(f"{tweet.user.screen_name}さんにお返事しますか？(y or n):")
        if reply_flag != "y":
            exit()
        reply_exercise_result(api, exercise_data, tweet)
