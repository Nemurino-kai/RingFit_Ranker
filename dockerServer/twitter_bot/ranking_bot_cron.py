# -*- coding: utf-8 -*-
from tweet_func import *
import sentry_sdk


def tweet():

    api = auth_twitter()

    print("画像を検索")
    tweet_ranking(api)


if __name__ == '__main__':
    sentry_sdk.init(os.environ['SENTRY_DSN'])
    tweet()
