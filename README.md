# RingFit_Ranker
リングフィットアドベンチャーの画像を収集し、消費カロリーをTesseractで読み取り、順位を呟くbot<br>
FF内の相手が #リングフィットアドベンチャー タグをつけて画像をツイートすると、順位をリプライします。

![EURqlAXU0AI-QHw](https://user-images.githubusercontent.com/40136659/82156108-2e819180-98b4-11ea-9bab-dbfe2e5b1b84.jpg)
![EURqlzlU8AAKDcX](https://user-images.githubusercontent.com/40136659/82156109-304b5500-98b4-11ea-852a-880a3031e7db.jpg)

Sqlite3により、DBにデータを保持しています。

bot_deamon.py を実行することで、常駐させることが可能です。
config.py にTwitterのAPI Tokenを記入し、他ファイルと同じディレクトリに置いてください。
