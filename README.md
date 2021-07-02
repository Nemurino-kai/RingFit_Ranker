# RingFit_Ranker
[![Netlify Status](https://api.netlify.com/api/v1/badges/2bd9f8b4-7b47-4709-a83a-e709afeff1f6/deploy-status)](https://app.netlify.com/sites/ringfit/deploys)
[![Twitter URL](https://img.shields.io/twitter/follow/RingFitRanker?style=social)](https://twitter.com/RingFitRanker)

Twitter上の <b>#リングフィットアドベンチャー</b> の画像を収集し、順位を呟くbotです<br>
https://twitter.com/RingFitRanker で運営中

現在、[サーバレス版](https://github.com/Nemurino-kai/RingFit_Ranker_Serverless)の開発も行っています。

## 機能１
- アカウントをフォローしたうえで、<b>#リングフィットアドベンチャー</b> タグを付けて運動結果をツイートすると、順位をリプライします。

![moto](https://user-images.githubusercontent.com/40136659/95277065-ddd0fc00-0887-11eb-9ece-bee6b76955fe.jpg)
![mame](https://user-images.githubusercontent.com/40136659/95277166-196bc600-0888-11eb-8666-43365546de63.jpg)

## 機能２
- 毎日4時に順位を集計し、12時頃に消費カロリー数ランキング Top10を画像で呟きます。

![top10](https://user-images.githubusercontent.com/40136659/84641755-78eb4200-af36-11ea-802d-18bb9300c749.png)

## 機能３
- https://ringfit.work から、全員分の順位が見れます。
- 過去の日付の順位を見ることも可能です。ページネーションに対応しています。
![rank](https://user-images.githubusercontent.com/40136659/103138235-d0ebd800-4713-11eb-8a1e-607b83daa477.png)

## 機能４
- https://ringfit.work/#/user/ から、Twitterの@ユーザ名を入力することで、いままでの運動記録と、消費カロリーのグラフを見ることができます。
![graph2](https://user-images.githubusercontent.com/40136659/95273961-7020d200-087f-11eb-87d0-e8b76e266791.png)

## 開発者向けのメッセージ
### システム構成図
![system](https://user-images.githubusercontent.com/40136659/103154913-74092400-47de-11eb-848c-a9a63798805b.png)


### 使用方法
dockerServerディレクトリ上で、`docker-compose build`および`docker-compose up`を行うことで、サーバ側の環境が構築されます。
dockerServerディレクトリには、.envファイルを以下のように設定し、置いてください。

```.env
CONSUMER_KEY=ここに
CONSUMER_SECRET=Twitterの
ACCESS_TOKEN=Tokenを
ACCESS_TOKEN_SECRET=いれる
TO_ADDR=障害発生時の報告メール送信先
FROM_ADDR=障害発生時の報告メール送信元
MAIL_PASS=Googleのアプリパスワード
TWITTER_ID=RingFitRanker(呟くアカウントのTwitter_ID)
DATABASE_DIR=運動記録を保存するデータベースを保存するディレクトリ
DATABASE_NAME=データベースの名前
RANKING_FONT=ランキング画像のユーザ名に用いるフォント
KCAL_FONT=ランキング画像の消費カロリーに用いるフォント
```

dockerServer/twitter_bot/tweet_bot_cron.py は、<b>#リングフィットアドベンチャー</b> の画像を検索・集計し、順位をリプライします。cronにより、5分に一回実行されます。<br>
dockerServer/twitter_bot/ranking_bot_cron.py は、前日4時から当日3時59分59秒までのランキングベスト10をツイートします。cronにより、毎日正午に実行されます。<br>
dockerServer/flask_webapp/info_pages.py は、Flaskにより作られたサーバサイドアプリケーションです。消費カロリーの順位などを取得できる、APIが実装されています。

vuejs_frontend ディレクトリは、Vue CLIにより作成されたSPAのプロジェクトです。Flaskで作成したAPIにアクセスすることで動作します。
