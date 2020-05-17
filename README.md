# RingFit_Ranker
Twitter上の <b>#リングフィットアドベンチャー</b> の画像を収集し、順位を呟くbotです
https://twitter.com/RingFitRanker で運営中

## 機能１
- アカウントをフォローしたうえで、<b>#リングフィットアドベンチャー</b> タグを付けて運動結果をツイートすると、順位をリプライします。

![image1](https://user-images.githubusercontent.com/40136659/82156108-2e819180-98b4-11ea-9bab-dbfe2e5b1b84.jpg)
![image2](https://user-images.githubusercontent.com/40136659/82156109-304b5500-98b4-11ea-852a-880a3031e7db.jpg)

## 機能2
- 毎日0時頃に、消費カロリー数ランキング Top3を呟きます。

![C14](https://user-images.githubusercontent.com/40136659/82156678-9dacb500-98b7-11ea-9423-aba5b48f124c.png)

## 近く実装予定
- 全員分の順位が見れるページを製作中です

![ta](https://user-images.githubusercontent.com/40136659/82156594-f62f8280-98b6-11ea-83dd-6f7272fa24e2.png)

## 開発者向けのメッセージ
Sqlite3により、DBにデータを保持しています。<br>
bot_deamon.py を実行することで、常駐させることが可能です。
config.py にTwitterのAPI Tokenを記入し、他ファイルと同じディレクトリに置いてください。
