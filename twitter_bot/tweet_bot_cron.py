# -*- coding: utf-8 -*-
import sys
import utils
import traceback
from tweet_func import *

def tweet():

    api = auth_twitter()

    args = sys.argv
    if len(args) == 1:
        print("画像を検索")
        search_exercise_data(api, max_number=100, interrupt=False)
    elif len(args) == 2:
        print("指定したクエリで検索")
        search_exercise_data(api, max_number=500, interrupt=False,query=str(args[1]))
    else:
        print("wrong usage")

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