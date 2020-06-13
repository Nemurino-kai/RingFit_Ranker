# RingFit_Ranker
Twitter上の <b>#リングフィットアドベンチャー</b> の画像を収集し、順位を呟くbotです<br>
https://twitter.com/RingFitRanker で運営中

## 機能１
- アカウントをフォローしたうえで、<b>#リングフィットアドベンチャー</b> タグを付けて運動結果をツイートすると、順位をリプライします。

![image1](https://user-images.githubusercontent.com/40136659/82156108-2e819180-98b4-11ea-9bab-dbfe2e5b1b84.jpg)
![image2](https://user-images.githubusercontent.com/40136659/82156109-304b5500-98b4-11ea-852a-880a3031e7db.jpg)

## 機能２
- 毎日4時に順位を集計し、12時頃に消費カロリー数ランキング Top3を呟きます。

![C14](https://user-images.githubusercontent.com/40136659/82156678-9dacb500-98b7-11ea-9423-aba5b48f124c.png)

## 機能３
- https://ringfit.work から、全員分の順位が見れます。
- 過去の日付の順位を見ることも可能です。ページネーションに対応しています。
![C42](https://user-images.githubusercontent.com/40136659/83976183-6c158f80-a933-11ea-826c-5eafd284278b.png)

## 開発者向けのメッセージ
### システム構成図
![ranker](https://user-images.githubusercontent.com/40136659/82590990-977d4800-9bd9-11ea-898a-369598a34226.png)

### 使用方法
npm のforeverコマンドを用いるなどして、tweet_bot.py を常駐させてください。<br>
例：``` forever start -c python3 tweet_bot.py  ```<br>
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
```

uwsgiについては、``` uwsgi --ini uwsgi_config.ini ``` で立ち上げられます。
