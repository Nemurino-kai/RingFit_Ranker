# -*- coding: utf-8 -*-
import os
from tweet_func import auth_twitter, tweet_ranking
import sentry_sdk


def tweet():

    api = auth_twitter()

    print("画像を検索")
    tweet_ranking(api)


if __name__ == '__main__':
    sentry_sdk.init(os.environ['SENTRY_DSN'])
    tweet()
