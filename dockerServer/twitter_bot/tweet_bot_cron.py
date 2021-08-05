# -*- coding: utf-8 -*-
import sys
import os
from tweet_func import auth_twitter, search_exercise_data
import sentry_sdk


def tweet():

    api = auth_twitter()

    args = sys.argv
    if len(args) == 1:
        print("画像を検索")
        search_exercise_data(api, max_number=100, interrupt=False)
    elif len(args) == 2:
        print("指定したクエリで検索")
        search_exercise_data(api, max_number=500,
                             interrupt=False, query=str(args[1]))
    else:
        print("wrong usage")


if __name__ == '__main__':
    sentry_sdk.init(os.environ['SENTRY_DSN'])
    tweet()
