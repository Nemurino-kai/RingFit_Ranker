# -*- coding: utf-8 -*-
import utils
import traceback
from tweet_func import *


def tweet():

    api = auth_twitter()

    print("画像を検索")
    tweet_ranking(api)


if __name__ == '__main__':
    try:
        tweet()
    except (Exception, tweepy.error.TweepError) as e:
        traceback.print_exc()
        utils.send_mail("An error has occurred.",  traceback.format_exc())
        raise e
    except:
        traceback.print_exc()
        utils.send_mail("An error has occurred.",  traceback.format_exc())
