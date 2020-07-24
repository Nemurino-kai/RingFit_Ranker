# RingFit_Ranker
Twitter上の <b>#リングフィットアドベンチャー</b> の画像を収集し、順位を呟くbotです<br>
https://twitter.com/RingFitRanker で運営中

現在、[サーバレス版](https://github.com/Nemurino-kai/RingFit_Ranker_Serverless)を開発しています、将来的に移行予定です。

## 機能１
- アカウントをフォローしたうえで、<b>#リングフィットアドベンチャー</b> タグを付けて運動結果をツイートすると、順位をリプライします。

![image1](https://user-images.githubusercontent.com/40136659/82156108-2e819180-98b4-11ea-9bab-dbfe2e5b1b84.jpg)
![image2](https://user-images.githubusercontent.com/40136659/82156109-304b5500-98b4-11ea-852a-880a3031e7db.jpg)

## 機能２
- 毎日4時に順位を集計し、12時頃に消費カロリー数ランキング Top10を画像で呟きます。

![top10](https://user-images.githubusercontent.com/40136659/84641755-78eb4200-af36-11ea-802d-18bb9300c749.png)

## 機能３
- https://ringfit.work から、全員分の順位が見れます。
- 過去の日付の順位を見ることも可能です。ページネーションに対応しています。
![all](https://user-images.githubusercontent.com/40136659/83976183-6c158f80-a933-11ea-826c-5eafd284278b.png)

## 機能４
- https://ringfit.work/user から、Twitterの@ユーザ名を入力することで、いままでの運動記録を見ることができます。
![user](https://user-images.githubusercontent.com/40136659/85702894-cecf9f00-b719-11ea-9124-abbf45b68860.jpg)

## 開発者向けのメッセージ
### システム構成図
![ranker](https://user-images.githubusercontent.com/40136659/82590990-977d4800-9bd9-11ea-898a-369598a34226.png)

### 使用方法
tweet_bot_cron.py を実行すると、<b>#リングフィットアドベンチャー</b> の画像を検索・集計し、順位をリプライします。<br>
ranking_bot_cron.py を実行すると、前日4時から当日3時59分59秒までのランキングベスト10をツイートします。<br>
cronを用いるなどして、定期的に実行してください。

config.pyは以下の通り設定し、他ファイルと同じディレクトリに置いてください。

```python
CONSUMER_KEY = "ここに"
CONSUMER_SECRET = "Twitterの"
ACCESS_TOKEN = "Tokenを"
ACCESS_TOKEN_SECRET = "いれる"
TO_ADDR = '障害発生時の報告メール送信先'
FROM_ADDR = '障害発生時の報告メール送信元'
MAIL_PASS = 'Googleのアプリパスワード'
TWITTER_ID = "RingFitRanker(呟くアカウントのTwitter_ID)"
DATABASE_NAME = "運動記録を保存するデータベースの名前"
RANKING_FONT = "ランキング画像のユーザ名に用いるフォント"
KCAL_FONT = "ランキング画像の消費カロリーに用いるフォント"
```

info_pages.py は、flaskにより作られたWebアプリです。消費カロリーの順位などを見ることができます。
