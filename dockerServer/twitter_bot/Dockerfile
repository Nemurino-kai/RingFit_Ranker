# ベースイメージ
FROM python:3.9

# sqlite3のアップデート(仮想列に対応したバージョンにアップデート)
RUN mkdir /sqlite
WORKDIR /sqlite
RUN wget https://www.sqlite.org/2020/sqlite-autoconf-3310100.tar.gz && \
tar zxvf sqlite-autoconf-3310100.tar.gz && \
mv sqlite-autoconf-3310100 sqlite-3.31.01 && \
./sqlite-3.31.01/configure && \
make
ENV LD_LIBRARY_PATH /sqlite/.libs

RUN mkdir /opt/bot
WORKDIR /opt/bot

# 依存Pythonライブラリ一覧コピー
COPY requirements.txt ./
# 依存Pythonライブラリインストール
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install python3-opencv -y && apt-get install busybox-static -y
# 日本語フォントのインストール
RUN apt-get install fonts-noto-cjk

# crontabファイルをコピー
COPY crontab /var/spool/cron/crontabs/root

# DBが無ければ、作成する（あれば作成しない）
# dockerのvolumeはbuild中に中身を参照できない。そのため、RUNでなくCMDを用いる。
CMD ["bash", "-c", "if [ ! -e /opt/bot/shared_file/result.db ]; then \
        /sqlite/sqlite3 /opt/bot/shared_file/result.db < /opt/bot/sql/create_exercise_table.sql; \
fi && busybox crond -f -L /dev/stderr"]